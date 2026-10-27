import json
import math
import unittest

from project_z.telemetry import ingest_jsonl, search_events


def row(event_id="e-1", **overrides):
    value = {
        "event_id": event_id,
        "timestamp": "2026-10-27T12:00:00Z",
        "source": "synthetic-api",
        "metric": "request_latency",
        "value": 42.5,
        "unit": "ms",
        "tags": {"service": "catalog", "environment": "synthetic"},
    }
    value.update(overrides)
    return json.dumps(value)


class TelemetryTests(unittest.TestCase):
    def test_accepts_valid_event(self):
        result = ingest_jsonl([row()])
        self.assertEqual(len(result.accepted), 1)
        self.assertEqual(result.accepted[0].value, 42.5)
        self.assertEqual(result.rejected, ())

    def test_rejects_malformed_json_and_continues(self):
        result = ingest_jsonl(["{bad json", row("e-2")])
        self.assertEqual(len(result.accepted), 1)
        self.assertEqual(result.rejected[0]["line"], 1)

    def test_rejects_duplicate_ids(self):
        result = ingest_jsonl([row(), row()])
        self.assertEqual(len(result.accepted), 1)
        self.assertIn("duplicate event_id", result.rejected[0]["reason"])

    def test_rejects_unknown_fields(self):
        result = ingest_jsonl([row(extra="not-allowed")])
        self.assertEqual(len(result.accepted), 0)

    def test_rejects_missing_required_field(self):
        raw = json.loads(row())
        del raw["metric"]
        result = ingest_jsonl([json.dumps(raw)])
        self.assertEqual(len(result.accepted), 0)

    def test_rejects_naive_timestamp(self):
        result = ingest_jsonl([row(timestamp="2026-10-27T12:00:00")])
        self.assertEqual(len(result.accepted), 0)

    def test_rejects_boolean_numeric_value(self):
        result = ingest_jsonl([row(value=True)])
        self.assertEqual(len(result.accepted), 0)

    def test_rejects_non_finite_value(self):
        raw = row().replace("42.5", "NaN")
        result = ingest_jsonl([raw])
        self.assertEqual(len(result.accepted), 0)

    def test_rejects_invalid_tags(self):
        result = ingest_jsonl([row(tags=["not", "an", "object"])])
        self.assertEqual(len(result.accepted), 0)

    def test_search_matches_metric_and_tags(self):
        events = ingest_jsonl([row("e-1"), row("e-2", metric="queue_depth", tags={"service":"worker"})]).accepted
        results = search_events(events, "request latency catalog")
        self.assertEqual([event.event_id for event in results], ["e-1"])

    def test_search_is_deterministic_for_ties(self):
        events = ingest_jsonl([row("z"), row("a")]).accepted
        self.assertEqual([e.event_id for e in search_events(events, "catalog", limit=2)], ["a", "z"])

    def test_empty_query_returns_no_results(self):
        self.assertEqual(search_events(ingest_jsonl([row()]).accepted, "  "), [])

    def test_invalid_limit_rejected(self):
        with self.assertRaises(ValueError):
            search_events([], "latency", limit=0)


if __name__ == "__main__":
    unittest.main()
