import base64
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jsonschema import Draft202012Validator
from project_q.release_gate import (
    SCHEMA_PATH,
    approval_signature_payload,
    canonical_digest,
    evaluate_release,
)


NOW = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)
TEST_PRIVATE_KEY = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
TEST_PUBLIC_KEY = TEST_PRIVATE_KEY.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)
TRUSTED_TEST_KEYS = {"test-approver-01": TEST_PUBLIC_KEY}


def sign_record(record):
    record["approval"]["artifact_digest"] = canonical_digest(record)
    record["approval"]["key_id"] = "test-approver-01"
    record["approval"]["signature"] = base64.b64encode(
        TEST_PRIVATE_KEY.sign(approval_signature_payload(canonical_digest(record), record["approval"]))
    ).decode("ascii")
    return record


def valid_record():
    record = {
        "registry_id": "PQ-0001",
        "registry_version": "1.0.0",
        "project_id": "PROJECT-Z",
        "component_id": "SYNTHETIC-PILOT",
        "record_type": "pilot-evidence",
        "classification": "VEF",
        "title": "Synthetic pilot acceptance fixture",
        "description": "Non-sensitive synthetic record for policy tests.",
        "source_records": ["fixture://synthetic/001"],
        "evidence": {
            "retrieved_at": "2026-10-28T11:00:00Z",
            "verification_status": "verified",
            "verification_method": "deterministic-fixture-check",
            "confidence": 1.0,
            "limitations": []
        },
        "lifecycle": {"status": "verified", "environment": "test", "owner": "test-suite", "dependencies": []},
        "risk": {"level": "low", "risk_register_ids": []},
        "approval": {
            "status": "approved",
            "reference": "TEST-APPROVAL-001",
            "artifact_digest": "",
            "environment": "test",
            "scopes": ["release"],
            "expires_at": "2026-10-29T12:00:00Z",
            "key_id": "test-approver-01",
            "signature": ""
        },
        "recovery": {"required": True, "status": "tested", "plan": "Restore the isolated test fixture."}
    }
    return sign_record(record)


def evaluate(record, **kwargs):
    return evaluate_release(record, trusted_approval_keys=TRUSTED_TEST_KEYS, **kwargs)


class ReleaseGateTests(unittest.TestCase):
    def test_schema_is_valid(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_valid_test_record_allowed(self):
        self.assertTrue(evaluate(valid_record(), now=NOW).allowed)

    def test_proposal_blocked(self):
        record = valid_record()
        record["classification"] = "PRO"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        record = sign_record(record)
        self.assertIn("EVIDENCE_NOT_VERIFIED", evaluate(record, now=NOW).blockers)

    def test_unverified_evidence_blocked(self):
        record = valid_record()
        record["evidence"]["verification_status"] = "unverified"
        record = sign_record(record)
        self.assertIn("VERIFICATION_STATUS_NOT_VERIFIED", evaluate(record, now=NOW).blockers)

    def test_unverified_lifecycle_blocked(self):
        record = valid_record()
        record["lifecycle"]["status"] = "documented"
        record = sign_record(record)
        self.assertIn("LIFECYCLE_NOT_VERIFIED", evaluate(record, now=NOW).blockers)

    def test_high_risk_blocked(self):
        record = valid_record()
        record["risk"]["level"] = "high"
        record = sign_record(record)
        self.assertIn("RISK_NOT_ACCEPTABLE", evaluate(record, now=NOW).blockers)

    def test_missing_approval_scope_blocked(self):
        record = valid_record()
        record["approval"]["scopes"] = []
        record = sign_record(record)
        self.assertIn("REQUIRED_SCOPE_MISSING", evaluate(record, now=NOW).blockers)

    def test_digest_mismatch_blocked(self):
        record = valid_record()
        record["title"] = "Changed after approval"
        self.assertIn("APPROVAL_DIGEST_MISMATCH", evaluate(record, now=NOW).blockers)

    def test_expired_approval_blocked(self):
        record = valid_record()
        record["approval"]["expires_at"] = "2026-10-27T12:00:00Z"
        record = sign_record(record)
        self.assertIn("APPROVAL_EXPIRED", evaluate(record, now=NOW).blockers)

    def test_recovery_not_tested_blocked(self):
        record = valid_record()
        record["recovery"]["status"] = "untested"
        record = sign_record(record)
        self.assertIn("RECOVERY_NOT_TESTED_OR_PLAN_MISSING", evaluate(record, now=NOW).blockers)

    def test_production_always_blocked_by_reference_gate(self):
        record = valid_record()
        record["lifecycle"]["environment"] = "production"
        record["approval"]["environment"] = "production"
        record = sign_record(record)
        self.assertIn("PRODUCTION_REQUIRES_SEPARATE_RELEASE_WORKFLOW", evaluate(record, now=NOW).blockers)

    def test_invalid_schema_blocked(self):
        record = valid_record()
        del record["risk"]
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_schema_read_failure_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            decision = evaluate(valid_record(), schema_path=missing, now=NOW)
        self.assertFalse(decision.allowed)
        self.assertTrue(any(x.startswith("POLICY_EVALUATION_ERROR:") for x in decision.blockers))

    def test_naive_clock_blocked(self):
        decision = evaluate(valid_record(), now=datetime(2026, 10, 28, 12, 0))
        self.assertIn("EVALUATION_TIME_MUST_BE_TIMEZONE_AWARE", decision.blockers)

    def test_missing_trusted_key_fails_closed(self):
        decision = evaluate_release(valid_record(), now=NOW)
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", decision.blockers)

    def test_tampered_approval_claim_fails_signature(self):
        record = valid_record()
        record["approval"]["expires_at"] = "2027-10-29T12:00:00Z"
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", evaluate(record, now=NOW).blockers)

    def test_tampered_signature_fails_closed(self):
        record = valid_record()
        record["approval"]["signature"] = base64.b64encode(b"x" * 64).decode("ascii")
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", evaluate(record, now=NOW).blockers)


if __name__ == "__main__":
    unittest.main()
