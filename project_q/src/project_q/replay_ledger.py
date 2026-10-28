"""SQLite-backed one-time approval consumption for isolated non-production use.

The record is evaluated inside this API before the nonce is consumed. The caller
still supplies the trusted key/revocation inputs; this module is not a trust
provider, distributed ledger, deployment mechanism, or production service.
"""
from __future__ import annotations

from collections.abc import Mapping, Set
from dataclasses import dataclass
from datetime import datetime, timezone
import re
import sqlite3
from pathlib import Path
from typing import Any

from .release_gate import SCHEMA_PATH, GateDecision, evaluate_release

_HEX_DIGEST = re.compile(r"^[a-f0-9]{64}$")
_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


@dataclass(frozen=True)
class ConsumptionResult:
    consumed: bool
    code: str
    blockers: tuple[str, ...] = ()
    record_digest: str = "unavailable"


def consume_approval(
    database: str | Path,
    *,
    record: dict[str, Any],
    trusted_approval_keys: Mapping[str, bytes] | None,
    revoked_approval_key_ids: Set[str] | None,
    consumed_at: datetime | None = None,
    schema_path: Path = SCHEMA_PATH,
) -> ConsumptionResult:
    """Evaluate a signed record, then atomically consume its approval ID and nonce.

    A caller cannot pass a fabricated allowed GateDecision: this function invokes
    evaluate_release itself. A durable unique constraint and BEGIN IMMEDIATE
    serialize competing writers. All validation/storage failures fail closed.
    """
    if not isinstance(record, dict):
        return ConsumptionResult(False, "RECORD_INVALID")
    decision: GateDecision = evaluate_release(
        record,
        trusted_approval_keys=trusted_approval_keys,
        revoked_approval_key_ids=revoked_approval_key_ids,
        schema_path=schema_path,
        now=consumed_at,
    )
    if not decision.allowed:
        return ConsumptionResult(False, "POLICY_DECISION_NOT_ALLOWED",
                                 decision.blockers, decision.record_digest)

    approval = record.get("approval")
    if not isinstance(approval, dict):
        return ConsumptionResult(False, "APPROVAL_INVALID", (), decision.record_digest)
    approval_id = approval.get("approval_id")
    nonce = approval.get("nonce")
    record_digest = approval.get("artifact_digest")
    policy_version = approval.get("policy_version")
    if record_digest != decision.record_digest or policy_version != decision.policy_version:
        return ConsumptionResult(False, "POLICY_DECISION_BINDING_MISMATCH", (), decision.record_digest)
    if not isinstance(approval_id, str) or not approval_id.strip() or len(approval_id) > 256:
        return ConsumptionResult(False, "APPROVAL_ID_INVALID", (), decision.record_digest)
    if not isinstance(nonce, str) or len(nonce) < 16 or len(nonce) > 256 or not nonce.strip():
        return ConsumptionResult(False, "NONCE_INVALID", (), decision.record_digest)
    if not isinstance(record_digest, str) or not _HEX_DIGEST.fullmatch(record_digest):
        return ConsumptionResult(False, "RECORD_DIGEST_INVALID", (), decision.record_digest)
    if not isinstance(policy_version, str) or not _SEMVER.fullmatch(policy_version):
        return ConsumptionResult(False, "POLICY_VERSION_INVALID", (), decision.record_digest)

    timestamp = consumed_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        return ConsumptionResult(False, "CONSUMPTION_TIME_MUST_BE_TIMEZONE_AWARE", (), decision.record_digest)
    timestamp_text = timestamp.astimezone(timezone.utc).isoformat()

    try:
        path = Path(database)
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path, timeout=10, isolation_level=None) as connection:
            connection.execute("PRAGMA synchronous=FULL")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS consumed_approvals (
                    approval_id TEXT PRIMARY KEY,
                    nonce TEXT NOT NULL UNIQUE,
                    record_digest TEXT NOT NULL,
                    policy_version TEXT NOT NULL,
                    consumed_at TEXT NOT NULL
                )"""
            )
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """INSERT INTO consumed_approvals
                   (approval_id, nonce, record_digest, policy_version, consumed_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (approval_id, nonce, record_digest, policy_version, timestamp_text),
            )
            connection.commit()
        return ConsumptionResult(True, "APPROVAL_CONSUMED", (), decision.record_digest)
    except sqlite3.IntegrityError:
        return ConsumptionResult(False, "APPROVAL_OR_NONCE_ALREADY_CONSUMED", (), decision.record_digest)
    except (OSError, sqlite3.Error):
        return ConsumptionResult(False, "REPLAY_LEDGER_UNAVAILABLE", (), decision.record_digest)
