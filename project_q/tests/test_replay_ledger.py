import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from project_q.replay_ledger import consume_approval


class ReplayLedgerTests(unittest.TestCase):
    DIGEST = "a" * 64
    NOW = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)

    def consume(self, db, approval_id="approval-1", nonce="0123456789abcdef0123456789abcdef", **kwargs):
        return consume_approval(
            db, approval_id=approval_id, nonce=nonce,
            record_digest=self.DIGEST, policy_version="1.2.0",
            decision_allowed=True, consumed_at=self.NOW, **kwargs
        )

    def test_first_approval_consumes(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.consume(Path(tmp) / "ledger.sqlite")
        self.assertTrue(result.consumed)
        self.assertEqual(result.code, "APPROVAL_CONSUMED")

    def test_same_approval_id_cannot_be_consumed_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "ledger.sqlite"
            self.assertTrue(self.consume(db).consumed)
            result = self.consume(db, nonce="abcdef0123456789abcdef0123456789")
        self.assertFalse(result.consumed)
        self.assertEqual(result.code, "APPROVAL_OR_NONCE_ALREADY_CONSUMED")

    def test_same_nonce_cannot_be_consumed_for_different_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "ledger.sqlite"
            self.assertTrue(self.consume(db).consumed)
            result = self.consume(db, approval_id="approval-2")
        self.assertFalse(result.consumed)

    def test_denied_policy_decision_is_not_consumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = consume_approval(
                Path(tmp) / "ledger.sqlite", approval_id="a", nonce="0123456789abcdef",
                record_digest=self.DIGEST, policy_version="1.2.0",
                decision_allowed=False, consumed_at=self.NOW
            )
        self.assertFalse(result.consumed)
        self.assertEqual(result.code, "PRIOR_POLICY_DECISION_NOT_ALLOWED")

    def test_invalid_digest_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = consume_approval(
                Path(tmp) / "ledger.sqlite", approval_id="a", nonce="0123456789abcdef",
                record_digest="not-a-digest", policy_version="1.2.0",
                decision_allowed=True, consumed_at=self.NOW
            )
        self.assertFalse(result.consumed)
        self.assertEqual(result.code, "RECORD_DIGEST_INVALID")

    def test_naive_consumption_time_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = consume_approval(
                Path(tmp) / "ledger.sqlite", approval_id="a", nonce="0123456789abcdef",
                record_digest=self.DIGEST, policy_version="1.2.0",
                decision_allowed=True, consumed_at=datetime(2026, 10, 28, 12, 0)
            )
        self.assertFalse(result.consumed)
        self.assertEqual(result.code, "CONSUMPTION_TIME_MUST_BE_TIMEZONE_AWARE")

    def test_concurrent_consumption_only_one_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "ledger.sqlite"
            def attempt(i):
                return self.consume(db, approval_id=f"approval-{i}").consumed
            with ThreadPoolExecutor(max_workers=8) as pool:
                outcomes = list(pool.map(attempt, range(8)))
        self.assertEqual(sum(outcomes), 1)

    def test_bad_database_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent_file = Path(tmp) / "not-a-directory"
            parent_file.write_text("x")
            result = consume_approval(
                parent_file / "ledger.sqlite", approval_id="a", nonce="0123456789abcdef",
                record_digest=self.DIGEST, policy_version="1.2.0",
                decision_allowed=True, consumed_at=self.NOW
            )
        self.assertFalse(result.consumed)
        self.assertEqual(result.code, "REPLAY_LEDGER_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
