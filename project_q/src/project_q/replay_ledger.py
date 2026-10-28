"""SQLite-backed, atomic approval replay ledger for isolated non-production use.

This module consumes approval identifiers only after a caller has independently
validated the signed approval and current trust/revocation state. It is not a
trust provider, deployment mechanism, or production authorization service.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
import sqlite3
from pathlib import Path
from collections.abc import Mapping

from .release_gate import GateDecision

_HEX_DIGEST = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True)
class ConsumptionResult:
    consumed: bool
    code: str


def consume_approval(
    database: str | Path,
    *,
    approval: Mapping[str, object],
    decision: GateDecision,
    consumed_at: datetime | None = None,
) -> ConsumptionResult:
    """Atomically consume an approval_id and nonce once in a durable SQLite DB.

    A unique constraint on each identifier plus BEGIN IMMEDIATE serializes
    competing writers. Any duplicate or storage failure fails closed.
    """
    if not isinstance(decision, GateDecision) or not decision.allowed:
        return ConsumptionResult(False, "PRIOR_POLICY_DECISION_NOT_ALLOWED")
    approval_id = approval.get("approval_id")
    nonce = approval.get("nonce")
    record_digest = approval.get("artifact_digest")
    policy_version = approval.get("policy_version")
    if record_digest != decision.record_digest or policy_version != decision.policy_version:
        return ConsumptionResult(False, "POLICY_DECISION_BINDING_MISMATCH")
    if not isinstance(approval_id, str) or not approval_id.strip() or len(approval_id) > 256:
        return ConsumptionResult(False, "APPROVAL_ID_INVALID")
    if not isinstance(nonce, str) or not nonce.strip() or len(nonce) > 256:
        return ConsumptionResult(False, "NONCE_INVALID")
    if not isinstance(record_digest, str) or not _HEX_DIGEST.fullmatch(record_digest):
        return ConsumptionResult(False, "RECORD_DIGEST_INVALID")
    if not isinstance(policy_version, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", policy_version):
        return ConsumptionResult(False, "POLICY_VERSION_INVALID")

    timestamp = consumed_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        return ConsumptionResult(False, "CONSUMPTION_TIME_MUST_BE_TIMEZONE_AWARE")
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
        return ConsumptionResult(True, "APPROVAL_CONSUMED")
    except sqlite3.IntegrityError:
        return ConsumptionResult(False, "APPROVAL_OR_NONCE_ALREADY_CONSUMED")
    except (OSError, sqlite3.Error):
        return ConsumptionResult(False, "REPLAY_LEDGER_UNAVAILABLE")
