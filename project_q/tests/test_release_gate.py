import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from project_q.release_gate import SCHEMA_PATH, canonical_digest, evaluate_release


NOW = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)


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
            "expires_at": "2026-10-29T12:00:00Z"
        },
        "recovery": {"required": True, "status": "tested", "plan": "Restore the isolated test fixture."}
    }
    record["approval"]["artifact_digest"] = canonical_digest(record)
    return record


class ReleaseGateTests(unittest.TestCase):
    def test_schema_is_valid(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_valid_test_record_allowed(self):
        self.assertTrue(evaluate_release(valid_record(), now=NOW).allowed)

    def test_proposal_blocked(self):
        record = valid_record()
        record["classification"] = "PRO"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("EVIDENCE_NOT_VERIFIED", evaluate_release(record, now=NOW).blockers)

    def test_unverified_evidence_blocked(self):
        record = valid_record()
        record["evidence"]["verification_status"] = "unverified"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("VERIFICATION_STATUS_NOT_VERIFIED", evaluate_release(record, now=NOW).blockers)

    def test_unverified_lifecycle_blocked(self):
        record = valid_record()
        record["lifecycle"]["status"] = "documented"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("LIFECYCLE_NOT_VERIFIED", evaluate_release(record, now=NOW).blockers)

    def test_high_risk_blocked(self):
        record = valid_record()
        record["risk"]["level"] = "high"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("RISK_NOT_ACCEPTABLE", evaluate_release(record, now=NOW).blockers)

    def test_missing_approval_scope_blocked(self):
        record = valid_record()
        record["approval"]["scopes"] = []
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("REQUIRED_SCOPE_MISSING", evaluate_release(record, now=NOW).blockers)

    def test_digest_mismatch_blocked(self):
        record = valid_record()
        record["title"] = "Changed after approval"
        self.assertIn("APPROVAL_DIGEST_MISMATCH", evaluate_release(record, now=NOW).blockers)

    def test_expired_approval_blocked(self):
        record = valid_record()
        record["approval"]["expires_at"] = "2026-10-27T12:00:00Z"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("APPROVAL_EXPIRED", evaluate_release(record, now=NOW).blockers)

    def test_recovery_not_tested_blocked(self):
        record = valid_record()
        record["recovery"]["status"] = "untested"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("RECOVERY_NOT_TESTED_OR_PLAN_MISSING", evaluate_release(record, now=NOW).blockers)

    def test_production_always_blocked_by_reference_gate(self):
        record = valid_record()
        record["lifecycle"]["environment"] = "production"
        record["approval"]["environment"] = "production"
        record["approval"]["artifact_digest"] = canonical_digest(record)
        self.assertIn("PRODUCTION_REQUIRES_SEPARATE_RELEASE_WORKFLOW", evaluate_release(record, now=NOW).blockers)

    def test_invalid_schema_blocked(self):
        record = valid_record()
        del record["risk"]
        self.assertFalse(evaluate_release(record, now=NOW).allowed)

    def test_schema_read_failure_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            decision = evaluate_release(valid_record(), schema_path=missing, now=NOW)
        self.assertFalse(decision.allowed)
        self.assertTrue(any(x.startswith("POLICY_EVALUATION_ERROR:") for x in decision.blockers))

    def test_naive_clock_blocked(self):
        decision = evaluate_release(valid_record(), now=datetime(2026, 10, 28, 12, 0))
        self.assertIn("EVALUATION_TIME_MUST_BE_TIMEZONE_AWARE", decision.blockers)


if __name__ == "__main__":
    unittest.main()
