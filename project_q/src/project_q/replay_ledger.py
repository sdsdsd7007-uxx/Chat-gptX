"""Single-node SQLite replay ledger reference.

Non-production only. The caller is responsible for passing a GateDecision
obtained from a successful signature and policy evaluation. A GateDecision
instance is not an authorization token; this helper is not a trust boundary.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import sqlite3

from .release_gate import GateDecision

@dataclass(frozen=True)
class ConsumptionResult:
    consumed: bool
    code: str

def consume_approval(database, *, approval, decision, consumed_at=None):
    if not isinstance(decision, GateDecision) or decision.allowed is not True:
        return ConsumptionResult(False, "PRIOR_POLICY_DECISION_NOT_ALLOWED")
    if not isinstance(approval, dict):
        return ConsumptionResult(False, "APPROVAL_INVALID")
    approval_id = approval.get("approval_id")
    nonce = approval.get("nonce")
    digest = approval.get("artifact_digest")
    version = approval.get("policy_version")
    if digest != decision.record_digest or version != decision.policy_version:
        return ConsumptionResult(False, "POLICY_DECISION_BINDING_MISMATCH")
    if not isinstance(approval_id, str) or not approval_id.strip() or len(approval_id) > 256:
        return ConsumptionResult(False, "APPROVAL_ID_INVALID")
    if not isinstance(nonce, str) or len(nonce) < 16 or len(nonce) > 256 or not nonce.strip():
        return ConsumptionResult(False, "NONCE_INVALID")
    if not isinstance(digest, str) or re.fullmatch(r"[a-f0-9]{64}", digest) is None:
        return ConsumptionResult(False, "RECORD_DIGEST_INVALID")
    if not isinstance(version, str) or len(version.split(".")) != 3 or any(not part.isdigit() for part in version.split(".")):
        return ConsumptionResult(False, "POLICY_VERSION_INVALID")
    stamp = consumed_at or datetime.now(timezone.utc)
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        return ConsumptionResult(False, "CONSUMPTION_TIME_MUST_BE_TIMEZONE_AWARE")
    try:
        path = Path(database)
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path, timeout=10, isolation_level=None) as db:
            db.execute("PRAGMA synchronous=FULL")
            db.execute("CREATE TABLE IF NOT EXISTS consumed_approvals (approval_id TEXT PRIMARY KEY, nonce TEXT NOT NULL UNIQUE, record_digest TEXT NOT NULL, policy_version TEXT NOT NULL, consumed_at TEXT NOT NULL)")
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO consumed_approvals VALUES (?, ?, ?, ?, ?)", (approval_id, nonce, digest, version, stamp.astimezone(timezone.utc).isoformat()))
            db.commit()
        return ConsumptionResult(True, "APPROVAL_CONSUMED")
    except sqlite3.IntegrityError:
        return ConsumptionResult(False, "APPROVAL_OR_NONCE_ALREADY_CONSUMED")
    except (OSError, sqlite3.Error):
        return ConsumptionResult(False, "REPLAY_LEDGER_UNAVAILABLE")
