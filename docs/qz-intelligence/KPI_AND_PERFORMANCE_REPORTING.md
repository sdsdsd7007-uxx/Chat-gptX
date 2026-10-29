# KPI, Progress-over-Time & Performance Reporting
**Report ID:** QZ-KPI-001  
**Status:** PROPOSED — baseline and telemetry connection required.

## Reporting rules
Every KPI record needs an ID, definition, formula, unit, scope, source, publication time, observation period, retrieval time, freshness SLA, actual, baseline, target, trend window, uncertainty, owner and reviewer.

Status labels: VERIFIED, REPORTED, ESTIMATED, STALE, UNKNOWN, NOT CONNECTED and PROPOSED. Never fill unknown actuals with zero. A target is not an actual; a test pass on one commit does not validate another.

## Core KPI dictionary
| Domain | KPI | Formula / unit | Actual status |
|---|---|---|---|
| Evidence | Claim provenance coverage | Traceable material claims / claims reviewed (%) | UNKNOWN |
| Data | Freshness compliance | Records within freshness SLA / records reviewed (%) | UNKNOWN |
| Synchronization | Contract validation pass rate | Valid events / events tested (%) | UNKNOWN |
| Research | Reproducibility | Independently reproduced analyses / analyses tested (%) | UNKNOWN |
| Relationship | Supported dependency coverage | Evidence-backed edges / edges assessed (%) | UNKNOWN |
| Country | Country acceptance coverage | Accepted country projects / countries in scope (%) | UNKNOWN |
| Recommendation | Traceability | Recommendations linked to evidence, risks and owners / reviewed (%) | UNKNOWN |
| Governance | Independent review coverage | Required reviews completed / reviews required (%) | UNKNOWN |
| Performance | End-to-end task latency | Request to validated result (ms or s) | NOT CONNECTED |
| Efficiency | Cost per verified outcome | Approved resource cost / accepted outcomes | UNKNOWN |
| Quality | Validation pass rate | Checks passed / checks executed (%) | UNKNOWN |
| Reliability | Failure rate | Failed eligible runs / eligible runs (%) | NOT CONNECTED |
| Learning | Verified improvement rate | Changes meeting preregistered criteria / evaluated changes (%) | UNKNOWN |

## Graph policy
Measured actuals, approved targets and forecasts/scenarios must have distinct visual styles. Missing observations remain gaps, never zero. Show date range, unit, source, freshness, denominator/sample count and uncertainty. Latency reports should show p50, p95 and p99. Avoid misleading truncated axes. Every point must trace to source/run evidence.

## Graph A — performance over time (data contract, not measured results)
No connected telemetry series was supplied when this document was created. Therefore no numeric performance curve is plotted here. The reporting implementation should display this empty-state graphic until valid observations exist:

PERFORMANCE ↑  
Target ┄ ┄ ┄ ┄ ┄  (only after approved)  
Actuals: no observations — NOT CONNECTED  
Time → T1   T2   T3   T4   T5

Do not interpret this as zero performance. Replace with a real chart only when source, timestamps, unit, sample count and at least two valid observations are available to support a trend.

## Observed CI pipeline graph snapshot — 2026-10-29 (not production telemetry)

The new [QZ/ASSD performance and progress report](https://github.com/sdsdsd7007-uxx/Chat-gptX/blob/feature/qz-intelligence-subprojects-v1/docs/qz-intelligence/reports/QZ_ASSD_Performance_Progress_Report_2026-10-29.md) contains two source-backed SVGs and the 51-row workflow-run source extract: [duration trend and outcome mix](https://github.com/sdsdsd7007-uxx/Chat-gptX/tree/feature/qz-intelligence-subprojects-v1/docs/qz-intelligence/reports). The observed scope is the GitHub Actions validation workflow on `feature/qz-assd-foundation` only. It records 51 attempts, of which 36 succeeded, 4 failed and 11 were cancelled; among non-cancelled attempts, 36/40 succeeded (90.0%). Run-start-to-final-update latency was p50 11s and p90 15s.

These data measure **CI workflow duration**, not end-to-end agent performance, production request latency, business impact or user outcomes. Production-engine telemetry remains NOT CONNECTED. Preserve the Graph A empty-state rule for any uninstrumented production metric; do not infer production performance from CI timing.

![Observed CI workflow duration](reports/CI_DURATION_TREND.svg)

![Observed CI workflow outcomes](reports/CI_OUTCOME_DISTRIBUTION.svg)

## Graph B — proposed roadmap (planned time, not measured progress)
| Workstream | Planned sequence | Status at report creation |
|---|---|---|
| Registry and ownership | Phase 0, first | PROPOSED |
| Contracts and schema tests | After registry | PROPOSED |
| Factor and Uganda country pilots | After contracts | PROPOSED |
| Relationship/synchronization tests | After pilot contracts | PROPOSED |
| Authorization and threat tests | In parallel after contracts | PROPOSED |
| Controlled staging and recovery | After test readiness | BLOCKED by existing QZ release gates |
| Expansion decision | After accepted pilots | PROPOSED |

This is a dependency plan, not a calendar commitment. Owners must approve dates; report actual start/finish dates from event records.

## Graph C — reporting pipeline
Source and run telemetry → quality/freshness validation → versioned time-series store → latency p50/p95/p99 + quality rate + milestone variance + cost per verified outcome → report with provenance, gaps and uncertainty.

## Acceptance for real graphs
- Source feed and metric owner identified.
- Definition, unit and sampling interval reviewed.
- At least two valid observations before claiming a trend.
- Missingness, revisions and outliers recorded.
- Actuals and targets visually distinct.
- Points trace to source/run evidence.
- Chart generated reproducibly from versioned data.
- Reviewer checks scale, denominator and interpretation.
- Export includes timestamp and freshness status.

## Proposed cadence
Per run: status, blockers, source freshness and errors. Daily: material changes and exceptions. Weekly: time-series, milestone variance, cost and reliability. Monthly: model evaluation, country/factor coverage and governance. Enable scheduled reporting only through explicitly configured, authorized automation.
