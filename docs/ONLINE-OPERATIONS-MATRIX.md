# Project Q & Z — Online Operations Matrix

**Document status:** proposed operating contract; not proof of live connectivity  
**Environment status:** production HOLD / live status UNKNOWN until verified telemetry and infrastructure evidence are available  
**Scope:** Project Q & Z, ASSD, ASREM, Pre-Action, Pro-Action, Post-Action/Learning, R&D, integrations, governance.

## 1. Operating principle
Treat “online,” “active,” “autonomous,” “zero latency,” “fully synchronized,” “self-healing,” and “risk-free” as claims that require direct, timestamped evidence. Never infer runtime status from a design document, dashboard mock-up, scheduled review, repository commit, or prior successful CI run. Zero latency and zero risk are not valid operational acceptance targets; measure bounded latency and residual risk instead.

## 2. Status vocabulary

| Status | Meaning | Minimum evidence |
|---|---|---|
| UNKNOWN | No current, trustworthy observation | Default when telemetry is missing or stale |
| DESIGNED | Requirements/documentation exist | Versioned design and owner |
| IMPLEMENTED | Code/configuration exists | Commit/config reference and review |
| TEST-PASS | Defined test passed | Test report tied to exact version/commit |
| STAGING-VERIFIED | Controlled integration test passed | Timestamped logs, test case, environment, reviewer |
| ONLINE-VERIFIED | Live endpoint and heartbeat confirmed | Authenticated health check, timestamp, freshness limit, monitoring source |
| DEGRADED | Service works below an agreed threshold | Metric breach and incident reference |
| FAILED | Verified failure | Reproducible error or health-check failure |
| HOLD | Not authorized for production/consequential execution | Release gate incomplete or approval missing |

## 3. Engine and sub-engine matrix

| Scope | Proposed engine/node | Required observable signal | Core KPI | Safe action on breach | Release state now |
|---|---|---|---|---|---|
| Live execution | Node-Z1 / Z Execution | Health check, request IDs, execution logs | Success rate; p50/p95/p99 latency | Stop/retry within bounded policy; alert owner | UNKNOWN / HOLD |
| Strategic intelligence | Node-Q1 / Q Intelligence | Source provenance, timestamp, confidence, freshness | Source coverage; stale-data rate; forecast error | Mark insight UNKNOWN/STALE; request refresh | UNKNOWN / HOLD |
| Reverse engineering | ASREM | Input/output references, reproducible analysis trace | Reproducibility; defect detection precision/recall | Quarantine unsupported conclusions | DESIGNED until evidence supplied |
| Pre-action | Pre-Action Engine | Scenario ID, assumptions, risk assessment | Scenario coverage; calibration; false-alarm rate | Require human decision gate for high-impact action | UNKNOWN / HOLD |
| Pro-action | Pro-Action / execution | Authorized action ID, approval, rollback reference | Authorized completion rate; rollback success | Reject unauthorized or unbounded action | UNKNOWN / HOLD |
| Post-action learning | Post-Action & Learning | Outcome labels, evaluation set/version, review log | Measured quality change; regression rate | Do not promote unvalidated model/config updates | UNKNOWN / HOLD |
| R&D / engine update | R&D and sub-engines | Versioned change, rationale, tests, approver | Regression-free change rate; time to recover | Stage, test, and roll back if criteria fail | UNKNOWN / HOLD |
| Integration/sync | Dropbox/Odoo/other adapters | Connector health, cursor/checkpoint, backlog, conflict log | Sync lag; backlog age; conflict rate; retry success | Pause unsafe writes; preserve queue and reconcile | NOT VERIFIED / HOLD |
| Security/resilience | Governance & Assurance | Access logs, alert events, backup and restore evidence | Critical findings; RTO/RPO; restore success | Isolate safely and invoke approved recovery plan | NOT VERIFIED / HOLD |

## 4. Minimum metric contract
Every metric must specify: definition, unit, measurement window, source, last-observed timestamp, freshness threshold, owner, alert threshold, escalation path, and test evidence. Report latency as measured percentiles, not “zero latency.” Report availability over a defined window, not “always online.” Report risks as assessed residual risks, not “risk-free.”

Recommended baseline signals:
- Availability and heartbeat freshness.
- Request success/failure rate and latency p50/p95/p99.
- Sync backlog, oldest pending item, retry outcomes, duplicate/conflict counts.
- Data quality and provenance coverage.
- Prediction quality against a held-out or otherwise independently defined evaluation set.
- Recovery time and recovery point from witnessed restore tests.
- Model/config version, deployment environment, rollback reference, and approver.

## 5. Three decision gates

1. **Data gate:** source is identified, timestamped, fresh enough, schema-valid, and privacy-reviewed. Missing data remains UNKNOWN.
2. **Decision gate:** evidence, confidence, downside, affected parties, and rollback path are documented. High-impact or uncertain decisions require authorized human review.
3. **Execution gate:** correct environment, least-privilege credentials, approved action, bounded retries, audit record, and tested rollback are confirmed. No production writes from this document or from telemetry alone.

## 6. Controlled engine-improvement loop

`OBSERVE → STUDY → VALIDATE PROVENANCE → ASSESS SUB-ENGINES → PROPOSE VERSIONED CHANGE → TEST IN ISOLATION → INDEPENDENT REVIEW → AUTHORIZED STAGING → VERIFY METRICS → PROMOTE OR ROLLBACK → RECORD LESSONS`

A scheduled automation is a periodic review task, not a continuously running online agent. It must not claim it monitored every second or detected a live outage unless an actual monitoring source and corresponding evidence exist.

## 7. Acceptance criteria for “ONLINE-VERIFIED”
- Named service, owner, environment, endpoint, and health-check method.
- Successful authenticated health check and heartbeat within a documented freshness window.
- Logs tied to the current deployed version, with secrets redacted.
- Agreed SLO thresholds and alert/escalation route.
- Failure-mode tests for timeout, stale data, duplicate events, connector outage, and retry exhaustion.
- Recovery/rollback test evidence and independent review.
- No unresolved critical security or data-integrity finding; explicit release authorization.

## 8. Current evidence boundary
The repository contains a validation foundation and documentation. This matrix does not itself connect Node-Z1, Node-Q1, ASREM, Pre/Pro units, Dropbox, or Odoo; does not create real-time telemetry; and does not verify 24/7 operation. Current live status remains **UNKNOWN** until the evidence above is supplied and checked. Production remains **HOLD**.
