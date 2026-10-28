# Project Z — Security, Dependency and Performance Review

**Review type:** implementation-author engineering review; not independent assurance  
**Scope:** synthetic telemetry ingestion, deterministic lexical retrieval, offline metrics, CI workflow and development dependencies  
**Environment:** non-production; synthetic fixtures only  
**Disposition:** continue isolated development after CI; do not connect sensitive/production data.

## 1. Executive result

The current Project Z pilot is a small, deterministic lexical baseline. It has no network client, external connector, persistent store, vector database, authorization layer or production ingestion service. The absence of those capabilities limits exposure but also means the pilot is not suitable for real multi-user or sensitive data.

This review identified and addressed three local resource-boundary gaps:
- ingestion previously had a per-line and per-row cap but no aggregate input-byte cap;
- lexical query length was unbounded;
- lexical search did not bound the number of events it would scan.

The code now sets a 16 MiB aggregate JSONL limit, 4,096-character query limit and 100,000-event search-corpus limit. Regression tests cover each boundary. These are conservative engineering defaults for a synthetic pilot, not workload-derived production limits.

## 2. Security findings

| ID | Severity | Finding | Status / required action |
|---|---|---|---|
| PZ-SEC-01 | Medium | A line-count limit multiplied by the per-line limit still permitted a very large aggregate payload and memory pressure. | Addressed in branch: 16 MiB total UTF-8 input cap; stops consuming the iterator at the first over-limit row; regression test added. |
| PZ-SEC-02 | Medium | Query length and search corpus size were not bounded, allowing excessive CPU work for caller-supplied inputs. | Addressed in branch: query cap 4,096 characters and search cap 100,000 events; regression tests added. |
| PZ-SEC-03 | High before real-data use | No authorization or tenant-isolation filter exists in retrieval. | Accepted limitation for synthetic-only scope. Do not ingest real multi-user data until access-control filters are designed, tested and enforced before results are returned. |
| PZ-SEC-04 | High before real-data use | No retention, deletion, legal-hold or privacy lifecycle is implemented. | Accepted limitation for synthetic-only scope. Define data classification, retention, deletion and audit behavior before any authorized non-synthetic data. |
| PZ-SEC-05 | Medium | Timestamp parsing checks timezone awareness but not source authenticity, clock skew, event freshness or allowed future skew. | Open design item. Define source-specific timestamp policy before operational alerting or authorization decisions. |
| PZ-SEC-06 | Medium | The offline evaluation labels are tiny and synthetic; no independent relevance adjudication or hold-out set exists. | Open. Do not make retrieval-quality claims or select vector/hybrid architecture from this fixture. |
| PZ-SEC-07 | Low | Lexical search tokenizes each event at query time and scans the corpus linearly. | Known baseline trade-off. Measure on a frozen representative corpus before adding indexing or vector infrastructure. |

## 3. Dependency review

- Project Z runtime modules currently use the Python standard library only; there is no separate Project Z runtime requirements file.
- The shared Project Q development requirements contain jsonschema[format]>=4.21,<5 and cryptography>=44,<48. These ranges allow compatible updates but are not a reproducible lock and do not pin hashes.
- Weekly Dependabot updates are configured for GitHub Actions and now also for pip under /project_q.
- GitHub Actions in the controlled workflow are pinned to immutable commit SHAs and the workflow has read-only contents: read permission; checkout credentials are not persisted.
- No claim is made that a vulnerability scanner, SBOM generator, lockfile/hash verification or independent supply-chain audit has been run.

**Dependency disposition:** acceptable only for this small non-production test harness with ongoing Dependabot review. Before production, create a tested lock with hashes, generate an SBOM, run a vulnerability audit, document transitive dependency ownership and define patch SLAs.

## 4. Performance review

- Retrieval algorithm: deterministic lexical overlap; linear scan over the supplied corpus. It is not semantic/vector retrieval.
- Current explicit limits: 16 MiB input batch, 10,000 JSONL rows, 65,536 characters per line, 4,096 query characters and 100,000 events per search.
- CI benchmark workload: 500 fabricated events and 30 repetitions. CI smoke-test completion verifies that the benchmark path runs; it is not a representative capacity test.
- Historical run #105 on the prior code head reported combined pipeline median/p95 6.455/6.854 ms, ingestion 5.241/5.595 ms, and lexical search 1.207/1.314 ms. These numbers predate the latest resource-limit changes and must not be used as the current baseline.
- The proposed 150 ms p95 target is not a production SLO and has not been validated on representative hardware, concurrency, corpus sizes or query distributions.
- Current benchmark does not measure memory, CPU saturation, concurrent clients, cold-start behavior, indexing, authorization filters, or p99 at a sufficiently large sample size.

**Performance disposition:** retain the lexical baseline. Freeze corpus/query/qrels, separate warm-up, use pinned hardware/runtime, measure at multiple corpus sizes and concurrency levels, report median/p90/p95/p99 with confidence intervals where sample sizes support them, and compare lexical/dense/hybrid on the same held-out relevance set.

## 5. Test and evidence record

The controlled CI workflow runs:
1. Project Q tests;
2. Project Z telemetry and retrieval-evaluation tests;
3. a 500-event / 30-iteration synthetic benchmark smoke test.

Final verified CI run #157 passed on head b2006fcf291518c9b16a4c0145060e49fcc32b43. Project Z suite: 28 tests passed; Project Q suite: 57 tests passed; total 85 tests passed. The 500-event / 30-repetition benchmark smoke test completed successfully. Exact timing output was not exposed in the inspected run summary, so no new numeric baseline is claimed. A green CI result is not an independent security review, privacy approval, production performance certification or deployment authorization.

## 6. Promotion gates

Before any non-synthetic or production use:
1. independent security review of ingestion, retrieval and CI boundaries;
2. authenticated identity and authorization filters with tenant-isolation tests;
3. privacy classification, retention, deletion and audit policy;
4. dependency lock with hashes, SBOM and vulnerability audit;
5. independently reviewed relevance labels and hold-out evaluation;
6. representative performance/capacity test and operational cost assessment;
7. tested backup/restore and incident response;
8. separate scoped human approval.

## 7. Research references

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Microsoft Research / SIGIR 2026, Evaluation Validity in Information Retrieval: https://www.microsoft.com/en-us/research/publication/evaluation-validity-in-information-retrieval/
- NIST, Computing confidence intervals for common IR measures: https://www.nist.gov/publications/computing-confidence-intervals-common-ir-measures
- IBM Research / ACL 2023, Moving Beyond Downstream Task Accuracy for Information Retrieval Benchmarking: https://research.ibm.com/publications/moving-beyond-downstream-task-accuracy-for-information-retrieval-benchmarking
