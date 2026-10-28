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
    record["approval"]["policy_version"] = "1.2.0"
    record["approval"].setdefault("not_before", "2026-10-28T11:00:00Z")
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
            "source_document": "fixture://synthetic/001",
            "source_records": ["fixture://synthetic/001"],
            "retrieved_at": "2026-10-28T11:00:00Z",
            "verified_by": "independent-test-fixture",
            "verified_at": "2026-10-28T11:00:00Z",
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
            "not_before": "2026-10-28T11:00:00Z",
            "policy_version": "1.2.0",
            "key_id": "test-approver-01",
            "signature": ""
        },
        "recovery": {"required": True, "status": "tested", "plan": "Restore the isolated test fixture.", "test_evidence_ref": "fixture://recovery/test-001"}
    }
    return sign_record(record)


def evaluate(record, **kwargs):
    return evaluate_release(record, trusted_approval_keys=TRUSTED_TEST_KEYS, revoked_approval_key_ids=set(), **kwargs)


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
        self.assertIn("RECOVERY_TEST_EVIDENCE_MISSING_OR_UNVERIFIED", evaluate(record, now=NOW).blockers)

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
        decision = evaluate_release(valid_record(), revoked_approval_key_ids=set(), now=NOW)
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", decision.blockers)

    def test_tampered_approval_claim_fails_signature(self):
        record = valid_record()
        record["approval"]["expires_at"] = "2027-10-29T12:00:00Z"
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", evaluate(record, now=NOW).blockers)



    def test_missing_revocation_registry_fails_closed(self):
        decision = evaluate_release(
            valid_record(), trusted_approval_keys=TRUSTED_TEST_KEYS, now=NOW
        )
        self.assertIn("REVOCATION_STATUS_UNAVAILABLE", decision.blockers)

    def test_missing_revocation_status_fails_closed(self):
        decision = evaluate_release(
            valid_record(), trusted_approval_keys=TRUSTED_TEST_KEYS, now=NOW
        )
        self.assertIn("REVOCATION_STATUS_UNAVAILABLE", decision.blockers)
        self.assertFalse(decision.allowed)

    def test_revoked_approval_key_blocked(self):
        decision = evaluate_release(
            valid_record(), trusted_approval_keys=TRUSTED_TEST_KEYS,
            revoked_approval_key_ids={"test-approver-01"}, now=NOW
        )
        self.assertIn("APPROVAL_KEY_REVOKED", decision.blockers)

    def test_approval_not_yet_valid_blocked(self):
        record = valid_record()
        record["approval"]["not_before"] = "2026-10-29T12:00:00Z"
        record = sign_record(record)
        self.assertIn("APPROVAL_NOT_YET_VALID", evaluate(record, now=NOW).blockers)

    def test_policy_version_is_signature_bound(self):
        record = valid_record()
        record["approval"]["policy_version"] = "1.1.0"
        blockers = evaluate(record, now=NOW).blockers
        self.assertIn("APPROVAL_POLICY_VERSION_MISMATCH", blockers)
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", blockers)

    def test_missing_source_provenance_blocked_by_schema(self):
        record = valid_record()
        del record["evidence"]["source_records"]
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_missing_recovery_test_evidence_blocked_by_schema(self):
        record = valid_record()
        del record["recovery"]["test_evidence_ref"]
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_invalid_approval_window_blocked(self):
        record = valid_record()
        record["approval"]["not_before"] = "2026-10-29T12:00:00Z"
        record["approval"]["expires_at"] = "2026-10-28T12:00:00Z"
        record = sign_record(record)
        self.assertIn("APPROVAL_VALIDITY_WINDOW_INVALID", evaluate(record, now=NOW).blockers)

    def test_empty_source_document_rejected_by_schema(self):
        record = valid_record()
        record["evidence"]["source_document"] = ""
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_duplicate_approval_scopes_rejected_by_schema(self):
        record = valid_record()
        record["approval"]["scopes"] = ["release", "release"]
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_unknown_audit_field_rejected_by_schema(self):
        record = valid_record()
        record["audit"] = {"unexpected_admin_override": True}
        self.assertFalse(evaluate(record, now=NOW).allowed)

    def test_digest_stable_for_object_key_order(self):
        record = valid_record()
        reordered = dict(reversed(list(record.items())))
        self.assertEqual(canonical_digest(record), canonical_digest(reordered))

    def test_non_finite_number_fails_closed(self):
        record = valid_record()
        record["description"] = float("nan")
        decision = evaluate(record, now=NOW)
        self.assertFalse(decision.allowed)
        self.assertIn("POLICY_EVALUATION_ERROR:ValueError", decision.blockers)

    def test_mismatched_provenance_records_blocked(self):
        record = valid_record()
        record["source_records"] = ["fixture://synthetic/other"]
        record = sign_record(record)
        self.assertIn("EVIDENCE_SOURCE_RECORDS_MISMATCH", evaluate(record, now=NOW).blockers)

    def test_future_evidence_timestamp_blocked(self):
        record = valid_record()
        record["evidence"]["verified_at"] = "2026-10-29T00:00:00Z"
        record = sign_record(record)
        self.assertIn("EVIDENCE_TIMESTAMP_IN_FUTURE", evaluate(record, now=NOW).blockers)

    def test_tampered_signature_fails_closed(self):
        record = valid_record()
        record["approval"]["signature"] = base64.b64encode(b"x" * 64).decode("ascii")
        self.assertIn("APPROVAL_SIGNATURE_INVALID_OR_UNTRUSTED", evaluate(record, now=NOW).blockers)


if __name__ == "__main__":
    unittest.main()
