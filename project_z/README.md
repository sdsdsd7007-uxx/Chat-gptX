# Project Z — Synthetic Telemetry Pilot

## Scope and safety
This is an isolated, synthetic-data-only engineering pilot. It performs no network access, persistent writes, account synchronization, external publishing, or production operations. Never place personal, customer, credential, health, or other sensitive data in these fixtures.

## Components
- `src/project_z/telemetry.py`: strict JSONL validation, duplicate-ID rejection, bounded aggregate input and deterministic lexical retrieval baseline.
- `tests/test_telemetry.py`: validation, rejection, resource-bound and search behavior tests.
- `SECURITY_DEPENDENCY_PERFORMANCE_REVIEW.md`: implementation-author review and production promotion gates.
- `fixtures/synthetic-events.jsonl`: tiny, fabricated sample dataset.
- `benchmarks/run_benchmark.py`: reproducible ingestion and lexical-search microbenchmark.
- `src/project_z/evaluation.py`: offline precision@k, recall@k, MRR, and nDCG@k evaluation.
- `fixtures/retrieval-qrels.json`: small fabricated query/relevance labels.

## Run locally
```bash
PYTHONPATH=project_z/src python -m unittest discover -s project_z/tests -v
PYTHONPATH=project_z/src python project_z/benchmarks/run_benchmark.py --events 1000 --iterations 30
```

## Acceptance gates
1. Malformed rows are rejected individually; valid subsequent rows continue.
2. Event IDs are unique within one ingestion batch.
3. Required fields, timezone-aware timestamps, finite numeric values, and string-to-string tags are enforced.
4. Retrieval is deterministic and explicitly lexical; it is not represented as vector or semantic search.
5. Input is bounded to 16 MiB per batch, 10,000 rows and 65,536 characters per line; queries are limited to 4,096 characters and search scans at most 100,000 events.
6. Benchmark output reports median and p95 separately for ingestion and retrieval.
7. The proposed 150 ms p95 objective is a measurement target only. Do not declare it met based on a single shared hosted runner or a tiny fixture. Establish a pinned hardware/runtime baseline, repeated runs, workload mix, and confidence intervals before adopting an SLO.

## Next research/engineering options
- **A — Keep lexical baseline:** simplest, transparent, low operational complexity.
- **B — Add vector retrieval:** only after a labelled relevance dataset and recall@k / nDCG evaluation exist.
- **C — Hybrid retrieval:** lexical + vector with measured fusion; preferred candidate after A has a stable baseline.
- **D — Streaming ingestion:** defer until throughput, ordering, replay, retention, and back-pressure requirements are specified.

Recommended sequence: A now, build evaluation dataset, then compare B and C offline. Do not introduce a vector database before a measurable retrieval need exists.

## Continuous integration
The pull-request workflow runs the Project Q evidence-gate tests, Project Z telemetry tests, and a small synthetic benchmark smoke test. CI success is a correctness check on this fixture workload, not a production performance claim.
