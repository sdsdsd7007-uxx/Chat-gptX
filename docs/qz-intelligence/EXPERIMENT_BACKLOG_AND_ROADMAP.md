# QZ / ASSD Experiment Backlog, Roadmap & Performance Measurement
**Document ID:** QZ-ROADMAP-003  
**Status:** PROPOSED — phases are an order of operations, not approved calendar dates  
**As of:** 2026-10-29

## 1. Delivery strategy

Use short, independently reviewable experiments. Measure **correctness + evidence quality + safety + latency + resource cost + usability**, rather than optimizing a single speed number. All experiments begin offline or read-only; state-changing tests require authorized staging.

## 2. Proposed 90-day sequence (relative timing)

### Phase A — Foundation (weeks 1–2)
- Reconcile the factor/project registry and PR/branch dependencies.
- Assign accountable product, security, data and operations owners plus an independent reviewer.
- Finish the tool/connector inventory and source-of-truth register.
- Define the task envelope, evidence record, recommendation record and telemetry schema.
- Record a baseline for existing CI and current manual workflows.
**Exit:** defined owners, schemas, permissions, baseline method and test plan; no critical unknown has been relabeled as passed.

### Phase B — Offline verification (weeks 3–4)
- Convert AA-001–AA-014 into executable synthetic tests; preserve QZ-AT-001–023 as a separate acceptance suite.
- Test expired/revoked authority, altered action payload, prompt injection, replay, malformed outputs, budget exhaustion and duplicate event.
- Add reproducible CI latency/result extraction, source freshness and graph checks.
- Harden action pins and run a reviewed dependency-lock pilot in an isolated branch.
**Exit:** exact-head test evidence, independent review of critical controls, no missing dependency class hidden by tooling.

### Phase C — Read-only pilots (weeks 5–8)
- Pilot one official-source Market X brief from public data.
- Pilot one factor unit from the QQQ/StudyCore portfolio.
- If approved, test a read-only Odoo export on synthetic or owner-authorized data.
- Instrument source retrieval, validation, report generation, cost/error counters and end-to-end duration.
- Compare outputs against manual review or a simple baseline.
**Exit:** source-backed output, reproducibility, disclosed missingness, reviewer acceptance and measured usefulness.

### Phase D — Staging and benefits review (weeks 9–12)
- Exercise timeouts, retries, idempotency, cancellation, restore and rollback in authorized staging.
- Run security and privacy review, accessibility checks and a small user-acceptance session.
- Compare observed outcomes against registered baseline and criteria.
- Decide to stop, redesign, extend or consider a limited controlled release.
**Exit:** written decision with evidence, residual risks and rollback proof. Production is not automatic.

## 3. Experiment catalogue

| Experiment | Hypothesis | Method | Metrics | Pass rule |
|---|---|---|---|---|
| EX-01 Claim provenance | Claim-to-source links reduce review friction and unsupported assertions | Double-review representative reports | traceability %, unsupported-claim rate, reviewer disagreements | Threshold predefined by owner; every critical claim traceable |
| EX-02 Freshness/conflict | Explicit freshness/conflict handling prevents false “current” values | Add stale/revised/conflicting source fixtures | stale-detection rate, false-current rate | No known stale critical value silently reported as current |
| EX-03 Authorization boundary | Server-side policy blocks untrusted approval data | Mutation/replay/expiry/wrong-identity fixtures | unauthorized action count, false deny rate | Zero unauthorized writes across required negative tests |
| EX-04 Prompt injection | Untrusted retrieved text cannot expand policy, scope or tools | Synthetic attack strings in pages/comments/docs | policy bypass, data leak, tool scope changes | Zero unauthorized side effects; all deny events auditable |
| EX-05 Safe retries | Retries and duplicate events are idempotent | Timeout, duplicate, out-of-order and partial failure fixtures | duplicate side effects, recovery success | No duplicate external side effects; recovery evidence retained |
| EX-06 CI stability | CI outcomes can be accurately reproduced and categorized | Pull run status/logs for every returned failure/cancellation | exact-head pass rate, classified failures, duration percentiles | Each failure/cancellation has classification or remains UNKNOWN |
| EX-07 Source-backed morning brief | A short report surfaces relevant changes without hiding uncertainty | Compare report with source pages and reviewer checklist | material omission, claim accuracy, freshness, review time | Defined quality bar met; no invented metrics |
| EX-08 Odoo replenishment | Lead-time-based risk adjustment improves decisions over a basic baseline | Historical holdout or synthetic validation before live read-only data | stockout proxy, excess stock proxy, forecast error, input completeness | Improvement must be measured; formula alone is not proof |
| EX-09 Human adoption | Role-specific workflows reduce rework and improve completion | Small supervised pilot and before/after task assessment | completion, rework, time, user-reported clarity | Predefined minimum benefit with no material quality decline |
| EX-10 Model routing | Routing improves cost/latency without reducing quality or security | Same task pack across approved model candidates | quality, citation, safety, p50/p95/p99, cost | Only candidates above quality/safety threshold eligible |
| EX-11 Geographic comparison | Harmonized units/periods prevent invalid rankings | Mixed-country fixtures with incompatible periods/definitions | block rate for invalid comparisons, missed valid comparables | Invalid comparisons blocked and reasons explained |
| EX-12 Rollback | Prior known-good state is restorable under interruption | Authorized staging restore drill | restore time, data loss, recovery success | Meets owner-approved recovery objective; proof retained |

All values and thresholds are **to be set before the experiment** by the accountable owner; no thresholds are fabricated here.

## 4. Progress and performance graph contracts

Every time-series point must carry:
- KPI ID, definition version, value and unit.
- Source/run URI, exact commit/config version and environment.
- Start/end/observation timestamp and reporting timezone.
- Sample size, denominator and inclusion/exclusion rule.
- Status: VERIFIED / REPORTED / ESTIMATED / STALE / UNKNOWN / NOT CONNECTED / PROPOSED.
- Error state, freshness and uncertainty where applicable.

### Required graph set
1. **Duration over time:** line chart by run start; show p50/p95/p99 in the accompanying table; do not merge distinct workloads.
2. **Outcome mix:** successful, failed, cancelled, timed out and blocked; cancellation does not equal failure.
3. **Quality vs latency:** only comparable runs; show quality gate and percentiles side-by-side.
4. **Milestone progress vs elapsed time:** show actual start/finish timestamps plus baseline; planned dates remain visibly planned.
5. **Source freshness:** records in SLA vs stale/unknown by domain and time.
6. **Cost per accepted outcome:** only after approved cost accounting and denominator are available.
7. **Risk/control acceptance:** tests proposed, executed, passed, failed, waived; explicit denominator and evidence link.
8. **Benefits realization:** observed before/after metrics with method and limitations; no unsupported savings claims.

Do not chart missing data as zero. Do not claim a trend from one point. Do not use CI run duration as a proxy for production agent, customer or business performance.

## 5. Current measured snapshot (CI only)

A sourced report has been added: [QZ/ASSD Performance & Progress-over-Time Report](reports/QZ_ASSD_Performance_Progress_Report_2026-10-29.md).

- Sample: 51 workflow attempts from `feature/qz-assd-foundation`, 2026-10-28 through 2026-10-29 UTC.
- Outcomes: 36 success, 4 failure, 11 cancelled.
- Success among non-cancelled attempts: 36/40 = 90.0%.
- Observed run-start-to-final-update duration: p50 11 seconds, p90 15 seconds, max 17 seconds.
- Interpretation: these are CI workflow metrics only. Production request latency, end-to-end agent quality, cost, customer satisfaction, source freshness of a live system and savings remain NOT CONNECTED or UNKNOWN.

See [CI_DURATION_TREND.svg](reports/CI_DURATION_TREND.svg), [CI_OUTCOME_DISTRIBUTION.svg](reports/CI_OUTCOME_DISTRIBUTION.svg) and [raw CI run history](reports/CI_RUN_HISTORY_2026-10-29.csv).

## 6. Risk budget and stop rules

- A critical authorization, privacy, prompt-injection or data-integrity failure stops promotion.
- Missing source permission or ambiguous source semantics pauses that integration.
- No independent review means DRAFT / NOT APPROVED.
- Cost/tool/time budget exhausted means stop with a surfaced blocker; do not spawn more workers.
- Rollback unverified means no production promotion.
- A faster response that is less correct, less grounded or less safe is a regression.
- A green test result on one SHA or environment cannot be copied to a new head.
- Any use of external actions must be explicitly scoped, logged and authorized.

## 7. Governance cadence (proposed)

- Per run: outcomes, errors, source freshness, budget and blockers.
- Daily review: material changes, failed/blocked items and stale high-priority sources.
- Weekly: trends, experiments, milestone variance, effort/cost and security findings.
- Monthly: model evaluation, partner value, factor/country expansion and risk appetite.
- Each cycle: record decision, owner, evidence, next action and review date. Cadence is proposed; do not imply these reviews are running unless scheduled and confirmed.
