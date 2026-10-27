"""Fail-closed release policy for Project Q evidence records.

This module evaluates policy only. It never deploys or changes external systems.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "evidence-record.schema.json"
REQUIRED_SCOPE = "release"


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    blockers: tuple[str, ...]
    policy_version: str
    record_digest: str


def canonical_digest(record: dict[str, Any]) -> str:
    """Hash stable JSON after excluding approval, which contains the hash itself."""
    payload = {key: value for key, value in record.items() if key != "approval"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluate_release(
    record: dict[str, Any],
    *,
    schema_path: Path = SCHEMA_PATH,
    now: datetime | None = None,
) -> GateDecision:
    blockers: list[str] = []
    digest = "unavailable"
    try:
        if not isinstance(record, dict):
            raise TypeError("record must be an object")
        digest = canonical_digest(record)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.path)))
        if errors:
            blockers.extend(f"SCHEMA:{'/'.join(map(str, e.path)) or '<root>'}" for e in errors)
            return GateDecision(False, tuple(blockers), "1.0.0", digest)

        evidence = record["evidence"]
        lifecycle = record["lifecycle"]
        risk = record["risk"]
        approval = record["approval"]
        recovery = record["recovery"]

        if record["classification"] != "VEF":
            blockers.append("EVIDENCE_NOT_VERIFIED")
        if evidence["verification_status"] != "verified":
            blockers.append("VERIFICATION_STATUS_NOT_VERIFIED")
        if lifecycle["status"] != "verified":
            blockers.append("LIFECYCLE_NOT_VERIFIED")
        if risk["level"] in {"critical", "unknown", "high"}:
            blockers.append("RISK_NOT_ACCEPTABLE")
        if approval["status"] != "approved":
            blockers.append("APPROVAL_NOT_APPROVED")
        if not approval["reference"].strip():
            blockers.append("APPROVAL_REFERENCE_MISSING")
        if approval["artifact_digest"] != digest:
            blockers.append("APPROVAL_DIGEST_MISMATCH")
        if approval["environment"] != lifecycle["environment"]:
            blockers.append("APPROVAL_ENVIRONMENT_MISMATCH")
        if REQUIRED_SCOPE not in approval["scopes"]:
            blockers.append("REQUIRED_SCOPE_MISSING")

        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            blockers.append("EVALUATION_TIME_MUST_BE_TIMEZONE_AWARE")
        else:
            expiry = datetime.fromisoformat(approval["expires_at"].replace("Z", "+00:00"))
            if expiry <= current:
                blockers.append("APPROVAL_EXPIRED")

        if recovery["required"] and (recovery["status"] != "tested" or not recovery["plan"].strip()):
            blockers.append("RECOVERY_NOT_TESTED_OR_PLAN_MISSING")

        # This component deliberately never grants production promotion.
        if lifecycle["environment"] == "production":
            blockers.append("PRODUCTION_REQUIRES_SEPARATE_RELEASE_WORKFLOW")

    except Exception as exc:  # fail closed on malformed input, I/O, schema or validator errors
        blockers.append(f"POLICY_EVALUATION_ERROR:{type(exc).__name__}")

    return GateDecision(not blockers, tuple(blockers), "1.0.0", digest)
