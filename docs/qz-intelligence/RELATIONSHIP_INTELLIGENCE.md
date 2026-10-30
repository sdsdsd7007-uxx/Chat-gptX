# Relationship Intelligence & Synchronization
**Proposed engine IDs:** QZ-RIE-001 and QZ-SYNC-001  
**Status:** DESIGN ONLY — not a live service.

## Relationship subunits
| ID | Subunit | Method / guardrail |
|---|---|---|
| RIE-01 | Dependency mapping | Directed graph with evidence for direction and mechanism |
| RIE-02 | Statistical association | Check sample size, lag, confounders and multiple testing |
| RIE-03 | Causal hypothesis testing | Suitable causal design; untested claims remain hypotheses |
| RIE-04 | System dynamics | Feedback, delays, accumulations and validation |
| RIE-05 | Scenario sensitivity | Base/adverse/severe assumptions; not predictions by default |
| RIE-06 | Country comparison | Harmonize units, periods and definitions |
| RIE-07 | Conflict reconciliation | Compare source, date, definition, method and revision |
| RIE-08 | Portfolio prioritization | Transparent benefit/cost/time/risk trade-offs |
| RIE-09 | Outcome feedback | Compare outcomes with preregistered expectations |
| RIE-10 | Independent verification | Reproduce calculations and review counterevidence |

## Example: import-linked procurement relationship map
FX quote and validity ─┐  
Supplier quote/lead time ─┤  
Freight/insurance ────────┼→ LANDED COST → CASH / WORKING CAPITAL  
Taxes and duties ─────────┘  
Forecast demand + approved safety stock + usable stock + confirmed incoming → REPLENISHMENT  
Replenishment → inventory availability → delivery/service → measured customer outcome  
Cash availability → capital capacity → measured outcome  
Measured outcome → reforecast and review → next cycle

This is a candidate relationship map, not verified causal estimates. Populate with authorized data before drawing conclusions.

## Synchronization event contract
Every event should contain: project_id, run_id, version, country_scope, factor_scope, source_references, observation_period, retrieved_at, freshness_status, evidence_status, findings, uncertainty, dependencies, recommendations, KPI references, owner, review_status and next_review. Required fields must be enforced by a versioned schema and CI.

## Reconciliation policy
1. Preserve original findings and source lineage.
2. Detect duplicates using stable source IDs/content digests and metadata.
3. Compare definitions, units, periods, revisions and methodology.
4. If conflict remains, preserve both findings with an unresolved-conflict status.
5. Escalate material conflicts to a named reviewer.
6. Never average conflicting estimates without a defensible method.
7. Publish only reconciled views with lineage to source records.
8. Invalidate dependent recommendations when material inputs change.
9. Keep audit history and a previous validated version.
10. Never copy permissions from a more privileged project during synchronization.

## Bounded scheduling
Trigger on a new/revised source, freshness expiry, schema change, material risk threshold, scheduled review or approved request. Deduplicate events; use idempotency keys; enforce concurrency and cost budgets; support cancellation; record skipped and failed jobs. Continuous eligibility is not unlimited execution.

## Sustainable-value ranking
Record expected benefit and evidence strength; time, capital and effort; downside risk and uncertainty; reversibility; customer/safety/privacy/legal impact; dependencies; measurement plan and owner. Safety, legal and authorization constraints are hard gates, not tradeable score components.
