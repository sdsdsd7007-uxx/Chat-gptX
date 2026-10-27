"""Reproducible synthetic ingestion/search microbenchmark; no production data."""
from __future__ import annotations

import argparse
import json
import statistics
import time

from project_z.telemetry import ingest_jsonl, search_events


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = max(0, min(len(ordered) - 1, int((p / 100) * len(ordered) + 0.999999) - 1))
    return ordered[index]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=int, default=1000)
    parser.add_argument("--iterations", type=int, default=30)
    args = parser.parse_args()
    if args.events < 1 or args.iterations < 2:
        parser.error("--events must be positive and --iterations must be at least 2")

    lines = [
        json.dumps({
            "event_id": f"synthetic-{i:06d}",
            "timestamp": "2026-10-27T12:00:00Z",
            "source": "synthetic-benchmark",
            "metric": "request_latency" if i % 2 == 0 else "queue_depth",
            "value": float((i % 100) + 1),
            "unit": "ms" if i % 2 == 0 else "items",
            "tags": {"service": f"service-{i % 10}", "environment": "synthetic"},
        }, separators=(",", ":"))
        for i in range(args.events)
    ]

    ingest_ms: list[float] = []
    search_ms: list[float] = []
    accepted = 0
    events = ()
    for _ in range(args.iterations):
        start = time.perf_counter()
        result = ingest_jsonl(lines)
        ingest_ms.append((time.perf_counter() - start) * 1000)
        accepted = len(result.accepted)
        events = result.accepted
        start = time.perf_counter()
        search_events(events, "request latency service-3", limit=20)
        search_ms.append((time.perf_counter() - start) * 1000)

    print(json.dumps({
        "dataset": "synthetic-only",
        "events_requested": args.events,
        "events_accepted": accepted,
        "iterations": args.iterations,
        "ingestion_ms": {"median": round(statistics.median(ingest_ms), 3), "p95": round(percentile(ingest_ms, 95), 3)},
        "lexical_search_ms": {"median": round(statistics.median(search_ms), 3), "p95": round(percentile(search_ms, 95), 3)},
        "p95_target_ms": 150,
        "target_met": percentile(ingest_ms + search_ms, 95) < 150,
        "note": "Microbenchmark only; hardware/runtime dependent and not a production SLO.",
    }, indent=2))


if __name__ == "__main__":
    main()
