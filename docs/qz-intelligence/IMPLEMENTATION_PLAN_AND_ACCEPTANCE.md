# Implementation Plan & Acceptance Gates
**Plan ID:** QZ-INTEL-IMPL-001  
**Status:** PROPOSED — owner dates and independent review required.

## Staged delivery
| Phase | Priority | Deliverable | Exit criteria |
|---|---|---|---|
| 0. Registry | P0 | Reconcile QQQ/QZ IDs, counts, PR branches and owners | Canonical registry; conflicts resolved or logged |
| 1. Contracts | P0 | Evidence, intelligence, recommendation, country and sync schemas | Versioned schemas; valid/invalid fixtures; review |
| 2. Factor pilots | P1 | Economics, finance, market, procurement/inventory, data and risk | Source-grounded outputs and repeatable tests |
| 3. Country pilot | P1 | Uganda project and official source register | Dated series, definitions and missingness recorded |
| 4. Relationship engine | P1 | Dependency graph, conflict handling and scenario methods | Reproducible outputs; correlation/causation distinction |
| 5. Reporting | P1 | KPI store and progress/time graphs | Actuals only from connected telemetry; chart checks pass |
| 6. Bounded automation | P1 | Scheduling, idempotency, cancellation, budgets and audit | Negative tests and authorization controls pass in staging |
| 7. Expansion | P2 | Additional factors/countries by evidence-backed priority | Each unit has owner, evaluation, value case and support plan |

## 100-microsecond objective
0.0001 seconds = 100 microseconds. Treat this as an experimental target for selected local operations (e.g. in-memory identifier lookup or deterministic routing) under specified hardware/runtime/workload. Do not apply it to external retrieval, model reasoning, full research or cross-country synthesis.

Benchmark protocol: specify hardware, runtime, workload, concurrency and payload; warm up where relevant; repeat enough for stable percentiles; report p50/p95/p99, throughput, errors and resource use; separate cold start, network, queue, inference and local compute; check correctness/evidence quality alongside latency; retain raw measurements and version metadata; compare only equivalent runs.

## Minimum acceptance test families
- Schema: required fields, invalid enums, unknown values and backward compatibility.
- Evidence: invalid reference, stale source, revision, conflicting claim and missing timestamp.
- Country: invalid ISO key, incomparable units, revised series and jurisdiction caveat.
- Relationships: spurious correlation, lag, confounder, conflicting source and scenario assumptions.
- Synchronization: duplicate event, out-of-order version, idempotency, partial failure and stale dependency.
- Authority: unknown identity, expired/revoked mandate, scope expansion, self-approval, replay and changed action.
- Automation: budget exhaustion, cancellation, retry limit, malformed output and fail-closed behavior.
- Reporting: no data, gaps, actual-vs-target, incorrect units, misleading axis, missing denominator and stale badge.
- Recovery: restore previous validated configuration and verify rollback in authorized staging.
- Performance: percentiles, concurrency, queue delay, failure load and correctness under load.

All tests are PROPOSED — NOT RUN until evidence records include commit, environment, timestamp, logs and reviewer.

## Required roles
Product/strategy owner; domain owner; data/source owner; security/authorization owner; independent reviewer who does not self-approve; operations owner for budgets, observability and recovery. Assign names only after confirmation.

## Risk controls
| Risk | Control |
|---|---|
| Unbounded agent proliferation | Require distinct capability, owner, cost budget and evaluation |
| Hallucinated evidence | Provenance checks, citation validation and independent reproduction |
| Stale indicators | Source-specific freshness SLA and visible observation period |
| Invalid country comparison | Harmonize units, periods, definitions and denominators |
| False causal claims | Separate association from causality; require appropriate design |
| Unsafe automation | Least privilege, authenticated approval, bounded tools and rollback |
| Misleading graphs | No zero-fill; show missing data; separate actuals from plans |
| Latency optimization harms quality | Quality and safety gates before speed optimization |
| Sync conflicts | Immutable source records, versioned contracts and explicit conflict state |

## Release gate
Production remains HOLD until applicable QZ PR #8 controls are independently reviewed and verified, including trusted authorization, branch protections, exact-head CI, workflow dependency inventory, QZ-AT-001–023 staging acceptance, recovery/rollback evidence and explicit release approval. Documentation and proposed tests do not close these gates.

## Completion definitions
DONE 1 — DESIGNED: registry, contracts, architecture and acceptance criteria documented.  
DONE 2 — VERIFIED: implementation, tests, provenance, independent review and recovery proof complete.  
DONE 3 — APPROVED & OPERATIONAL: authorized release, monitored outcomes and verified recovery.

Current proposal status: **documentation created; independent review and implementation validation pending. DONE 2 and DONE 3 are not claimed.**
