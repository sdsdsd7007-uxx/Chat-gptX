# QQQ-SP1 — Integration Vanguard
**Parent:** QQQ Master Framework v53.0  
**Status:** planned pilot; production remains HOLD  
**Date:** 2026-10-28

## Purpose
QQQ-SP1 is the first bounded sub-project beneath QQQ. It proves that component definitions, event contracts, local reporting, test results and release decisions can be tracked with reproducible evidence. Its existence as a plan does not imply that QQQ engines are online or connected to external services.

## Work packages
1. **SP1-01 — Component register:** stable ID, purpose, version, dependency, status, owner role, reviewer role, evidence and next review.
2. **SP1-02 — Event contract:** align schema, validator and regression tests; record malformed, boundary and nested-field cases.
3. **SP1-03 — Data consistency:** specify event identity, duplicates, replay, conflict handling and quarantine.
4. **SP1-04 — Local dashboard:** searchable engine registry, scenario viewer, CSV/JSON exports and print view; demo data must be clearly labelled.
5. **SP1-05 — Scenario test harness:** baseline, dependency interruption, data-quality exception, recovery and controlled improvement.
6. **SP1-06 — Staging readiness:** document access scope, data handling, test environment, audit records and approval requirements before any connector is enabled.
7. **SP1-07 — Release evidence:** test report, recovery/rollback evidence, open-risk list and independent acceptance.

## Controlled workflow
`STUDY → INVENTORY → SPECIFY → PLAN → AUDIT THE PLAN → BUILD IN ISOLATION → TEST → REVIEW → STAGING → VERIFY → ACCEPT OR ROLLBACK`

Each action must name its input/source, output, environment, time/resource bounds, owner, reviewer, success criteria and rollback. Parallel tasks must have bounded concurrency and must not silently modify the same record. A queued or scheduled task is not complete until its acceptance evidence is available.

## Status vocabulary
- **UNKNOWN:** current state cannot be verified.
- **DESIGNED:** a reviewed specification exists.
- **IMPLEMENTED:** a versioned artifact exists.
- **TEST-PASS:** a defined test passed on an identified version.
- **STAGING-VERIFIED:** a controlled integration test passed.
- **ONLINE-VERIFIED:** a current live health check and heartbeat are evidenced.
- **HOLD:** a required test, owner, approval or risk acceptance is missing.

## Acceptance criteria
- Every in-scope component is registered and has accountable owner/reviewer roles.
- Schema and validator behavior match and regression tests are tied to the exact commit.
- Duplicate/replay/conflict handling is defined and tested.
- Dashboard search, filters, exports and demo-state labels work as described.
- Each scenario has assumptions, expected result, measurable pass/fail criteria and a rollback path.
- Staging tests, recovery evidence and independent review are recorded before a release request.
- No task claims live connection or production status without current, direct evidence.

## Indicative schedule
| Phase | Estimate | Exit evidence |
|---|---|---|
| 0 — Study & inventory | 0–2 days | scope, component register, owners, dependencies |
| 1 — Contract & prototype | 3–7 days | validator tests, dashboard behavior tests |
| 2 — Data consistency | 1–2 weeks | duplicate, replay and conflict test results |
| 3 — Staging readiness | 2–4 weeks | reviewed permissions and recorded staging tests |
| 4 — Recovery & acceptance | 4–6 weeks | restore/rollback results, independent review and explicit release decision |

These are planning bands, not delivery guarantees; access, owners and test environments can change them.

## DONE definition
QQQ-SP1 is done only when all agreed acceptance tests pass on a known version, supporting evidence is linked, unresolved risks are disclosed, rollback is available where applicable and an authorized reviewer records the decision. Until then, status remains **IN PROGRESS / HOLD**.
