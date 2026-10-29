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


## Security review — trust boundary (2026-10-29)

### What the current code proves

- The proposal fingerprint detects accidental or unapproved changes to the material proposal fields **when the recorded fingerprint is retained as trusted data**.
- The apply function checks that the approval names the proposal and the same fingerprint, that the configuration version and base value are current, and that the reviewer ID differs from `requestedBy`.
- These are integrity and consistency checks inside a function; they are not identity authentication.

### Critical limitation: approval records are caller-supplied

`applyApprovedEngineUpdate(config, proposal, approval)` receives the approval object as an ordinary JavaScript object. The module does not authenticate who created it, verify a digital signature, consult a trusted identity provider, or independently establish that the reviewer is authorized. A caller able to construct the object can supply a distinct `reviewerId`, an `approved` status, a timestamp, an evidence-reference string, and a matching fingerprint. Therefore the current module must **not** be treated as a security boundary or as proof of human approval.

Likewise, `sourceReferences` and the subengine status/confidence fields are inputs to the module. The module checks consistency and required fields; it does not prove that referenced evidence exists, is authentic, or supports the supplied claim. A SHA-256 proposal fingerprint is not a signature and does not authenticate the reviewer.

### Required design before any real configuration write

1. Put approval verification in a trusted server-side boundary that ordinary callers cannot replace or bypass.
2. Authenticate the reviewer using the organization’s identity provider; authorize role, scope, separation of duties, and approval expiry.
3. Verify a signed approval envelope or a durable approval record from a trusted service. Bind it to the proposal fingerprint, base config version, repository/environment, expiry, and a unique approval ID.
4. Enforce single use / replay protection and write an append-only audit event. Do not trust a caller-supplied reviewer ID or evidence URL as proof by itself.
5. Resolve evidence references through approved adapters and record provenance, retrieval time, content digest, and validation outcome. Keep secrets and unnecessary personal data out of logs.
6. Apply updates only through a server-side allowlisted operation with optimistic concurrency, independent post-change verification, and a tested rollback path.
7. Add negative tests for forged approvals, expired/replayed approvals, unauthorized roles, evidence substitution, stale config, and attempted approval-service bypass. Run these in staging with a documented test record.

### Workflow supply-chain finding

The current validation workflow references `actions/checkout@v7` and `actions/setup-node@v7` by version tags. Tags are mutable references. GitHub announced workflow dependency lockfiles as generally available on 2026-10-28; the recommended next step is to install and run the official `gh actions-lock` extension in a controlled development environment, review the generated dependency commits and full diff, then commit the generated lockfile. Do **not** hand-write lockfile hashes or enforce the policy before all relevant workflows have been onboarded and verified.

A lockfile improves reproducibility; it does not prove that an action is safe. Continue source review and use Dependabot or another reviewed update process.

### Review disposition

- Proposal tamper-detection regression tests: present; latest CI passed on the current feature-branch head.
- Trusted reviewer authentication / signed approval: **NOT IMPLEMENTED**.
- Evidence authenticity and provenance verification: **NOT IMPLEMENTED**.
- Workflow dependency lockfile: **NOT IMPLEMENTED**.
- Staging acceptance tests QZ-AT-001–023: **NOT RUN**.
- Production release: **HOLD / NOT APPROVED**.

This review is a code-level assessment, not an independent security audit or a claim that the repository has been penetrated.
