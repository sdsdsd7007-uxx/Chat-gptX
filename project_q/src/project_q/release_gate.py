"""Fail-closed Project Q policy evaluator; this module never deploys or writes externally."""
from __future__ import annotations

import base64
from collections.abc import Mapping, Set
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "evidence-record.schema.json"
POLICY_VERSION = "1.2.0"
REQUIRED_SCOPE = "release"


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    blockers: tuple[str, ...]
    policy_version: str
    record_digest: str


def canonical_digest(record: dict[str, Any]) -> str:
    """SHA-256 over the record excluding its separately signed approval envelope."""
    payload = {key: value for key, value in record.items() if key != "approval"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def approval_signature_payload(record_digest: str, approval: dict[str, Any]) -> bytes:
    """Bind every approval claim (including policy version and validity window) to the digest."""
    payload = {
        "record_digest": record_digest,
        "approval": {key: value for key, value in approval.items() if key != "signature"},
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def verify_approval_signature(
    record_digest: str,
    approval: dict[str, Any],
    trusted_approval_keys: Mapping[str, bytes] | None,
) -> bool:
    """Verify Ed25519 against an externally provisioned trusted public-key registry."""
    if not isinstance(approval, Mapping) or not isinstance(trusted_approval_keys, Mapping):
        return False
    key_id = approval.get("key_id")
    encoded_signature = approval.get("signature")
    if not isinstance(key_id, str) or not key_id or not isinstance(encoded_signature, str):
        return False
    try:
        public_key_bytes = trusted_approval_keys.get(key_id)
        if not isinstance(public_key_bytes, bytes) or len(public_key_bytes) != 32:
            return False
        signature = base64.b64decode(encoded_signature, validate=True)
        if len(signature) != 64:
            return False
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, approval_signature_payload(record_digest, dict(approval)))
        return True
    except Exception:
        # This helper is fail-closed even when called outside evaluate_release.
        return False


def _parse_aware_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone offset")
    return parsed


def evaluate_release(
    record: dict[str, Any],
    *,
    trusted_approval_keys: Mapping[str, bytes] | None = None,
    revoked_approval_key_ids: Set[str] | None = None,
    schema_path: Path = SCHEMA_PATH,
    now: datetime | None = None,
) -> GateDecision:
    """Evaluate a signed evidence record. Missing trust/revocation inputs fail closed."""
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
            return GateDecision(False, tuple(blockers), POLICY_VERSION, digest)

        evidence = record["evidence"]
        lifecycle = record["lifecycle"]
        risk = record["risk"]
        approval = record["approval"]
        recovery = record["recovery"]

        if record["classification"] != "VEF":
            blockers.append("EVIDENCE_NOT_VERIFIED")
        if evidence["verification_status"] != "verified":
            blockers.append("VERIFICATION_STATUS_NOT_VERIFIED")
        if not evidence["source_records"] or not evidence["verified_by"].strip():
            blockers.append("EVIDENCE_PROVENANCE_INCOMPLETE")
        if set(record["source_records"]) != set(evidence["source_records"]):
            blockers.append("EVIDENCE_SOURCE_RECORDS_MISMATCH")
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
        if approval["policy_version"] != POLICY_VERSION:
            blockers.append("APPROVAL_POLICY_VERSION_MISMATCH")
        if revoked_approval_key_ids is None:
            blockers.append("REVOCATION_STATUS_UNAVAILABLE")
        elif approval["key_id"] in revoked_approval_key_ids:
            blockers.append("APPROVAL_KEY_REVOKED")
        if not verify_approval_signature(digest, approval, trusted_approval_keys):
            blockers.append("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED")
        if approval["environment"] != lifecycle["environment"]:
            blockers.append("APPROVAL_ENVIRONMENT_MISMATCH")
        if REQUIRED_SCOPE not in approval["scopes"]:
            blockers.append("REQUIRED_SCOPE_MISSING")

        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None or current.utcoffset() is None:
            blockers.append("EVALUATION_TIME_MUST_BE_TIMEZONE_AWARE")
        else:
            not_before = _parse_aware_datetime(approval["not_before"])
            expires_at = _parse_aware_datetime(approval["expires_at"])
            current_utc = current.astimezone(timezone.utc)
            if not_before > current_utc:
                blockers.append("APPROVAL_NOT_YET_VALID")
            if expires_at <= current_utc:
                blockers.append("APPROVAL_EXPIRED")
            if expires_at <= not_before:
                blockers.append("APPROVAL_VALIDITY_WINDOW_INVALID")
            verified_at = _parse_aware_datetime(evidence["verified_at"])
            retrieved_at = _parse_aware_datetime(evidence["retrieved_at"])
            if verified_at > current_utc or retrieved_at > current_utc:
                blockers.append("EVIDENCE_TIMESTAMP_IN_FUTURE")

        if recovery["required"] and (
            recovery["status"] != "tested"
            or not recovery["plan"].strip()
            or not recovery["test_evidence_ref"].strip()
        ):
            blockers.append("RECOVERY_TEST_EVIDENCE_MISSING_OR_UNVERIFIED")

        # This reference evaluator never grants production promotion.
        if lifecycle["environment"] == "production":
            blockers.append("PRODUCTION_REQUIRES_SEPARATE_RELEASE_WORKFLOW")

    except Exception as exc:  # fail closed for malformed input, schema, I/O and policy errors
        blockers.append(f"POLICY_EVALUATION_ERROR:{type(exc).__name__}")

    return GateDecision(not blockers, tuple(blockers), POLICY_VERSION, digest)
