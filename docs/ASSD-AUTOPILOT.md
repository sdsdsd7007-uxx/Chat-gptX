# ASSD Autopilot — Study → Evaluate → Propose → Approve → Update

## Purpose

The autopilot coordinates evidence-backed studies across four subsystem engines and generates controlled configuration-update proposals. It is not a production agent and does not execute external operations.

## Engine and subengines

- **ASSD Study Engine:** validates study identity, UTC timestamp, source references and confidence; coordinates subsystem evaluation.
- **MCU — Materiality & Compliance:** reports compliance/materiality signal. Unknown or failed results trigger investigation.
- **CERE — Circular Economy Resource Engine:** reviews resource-flow/circularity signal and supporting evidence.
- **ARRE — Risk & Resilience Engine:** reviews risk/resilience signal. An unknown or failed ARRE signal blocks the cycle.
- **IPSU — Impact-to-P&L Engine:** reviews financial attribution/reconciliation signal; financial claims still require separate source-of-record reconciliation.
- **Engine Update Subengine:** converts a valid recommendation into a proposal against an explicit allowlist of tunable configuration paths.

## State flow

1. `STUDY`: accept a study object and current versioned configuration.
2. `VALIDATE`: require a real UTC timestamp, source references, confidence in [0, 1], and known configuration version.
3. `ASSESS`: evaluate MCU, CERE, ARRE and IPSU. A `pass` signal without evidence is treated as `NOT_VERIFIED`; `unknown` never counts as a pass.
4. `INVESTIGATE`: any failure, unknown signal, missing evidence or low confidence blocks an update.
5. `REVIEW_UPDATE`: if all gates pass and a recommendation is within the safe tuning allowlist, create a `PENDING_APPROVAL` proposal. It is never applied during the study cycle.
6. `APPROVE`: a different reviewer must approve the exact proposal, version and evidence.
7. `APPLY`: only after approved checks succeed, update the configuration version and append an audit record.
8. `VERIFY`: rerun the relevant tests and measure the expected outcome before treating the adjustment as effective.
9. `ROLLBACK`: restore the previous approved configuration version if verification fails; rollback is an operational requirement and is not automated by this starter module.

## Update allowlist

The starter engine only permits bounded numeric changes to:

- `routing.confidenceThreshold`: 0.75–0.99
- `telemetry.maxRetryCount`: integer 0–5
- `kpi.alertTolerancePercent`: 0–25
- `resourceEfficiency.targetPercent`: 0–100

These are example guardrails for code testing, not approved business policies. The module blocks other configuration paths, including security, compliance and approval controls. Bounds must be reviewed for the real operating context before adoption.

## Minimum evidence contract

Each study must include a study ID, UTC study time, one or more source references, confidence score, and one status/evidence object for each subengine. Recommendations must cite source references already attached to the study and include a rationale and measurable expected outcome.

## Current limitations / production gate

- No external connectors, production telemetry ingestion, database/master-register writes, channel failover or autonomous financial/compliance actions are implemented here.
- Subengine signals are supplied to the module; this code does not independently determine whether a real-world compliance or risk claim is true.
- JSON schema and validator code must remain in sync; add contract tests when either changes.
- Production requires independent code review, an approved policy catalogue, real source adapters, permissions/secret review, integration and staging tests, telemetry, deduplication/quarantine, recovery and rollback drills, and signed release approval.

**Release status: HOLD / NOT APPROVED FOR PRODUCTION.**
