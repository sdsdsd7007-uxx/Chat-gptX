import unittest

from project_z.evaluation import evaluate_queries
from project_z.telemetry import ingest_jsonl


def line(event_id, metric, service):
    import json
    return json.dumps({
        "event_id": event_id,
        "timestamp": "2026-10-27T12:00:00Z",
        "source": "synthetic",
        "metric": metric,
        "value": 1,
        "unit": "count",
        "tags": {"service": service, "environment": "synthetic"},
    })


class RetrievalEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.events = ingest_jsonl([
            line("e1", "request_latency", "catalog"),
            line("e2", "queue_depth", "worker"),
            line("e3", "error_count", "catalog"),
        ]).accepted

    def test_perfect_top_one_metrics(self):
        result = evaluate_queries(self.events, [{"query": "request latency", "relevant_event_ids": ["e1"]}], k=1)
        self.assertEqual(result["precision_at_1"], 1.0)
        self.assertEqual(result["recall_at_1"], 1.0)
        self.assertEqual(result["mrr"], 1.0)
        self.assertEqual(result["ndcg_at_1"], 1.0)

    def test_macro_metrics_for_two_queries(self):
        result = evaluate_queries(self.events, [
            {"query": "request latency", "relevant_event_ids": ["e1"]},
            {"query": "queue depth", "relevant_event_ids": ["e2"]},
        ], k=1)
        self.assertEqual(result["query_count"], 2)
        self.assertEqual(result["recall_at_1"], 1.0)

    def test_empty_qrels_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_queries(self.events, [])

    def test_missing_relevant_ids_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_queries(self.events, [{"query": "latency", "relevant_event_ids": []}])

    def test_invalid_k_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_queries(self.events, [{"query": "latency", "relevant_event_ids": ["e1"]}], k=0)


if __name__ == "__main__":
    unittest.main()
