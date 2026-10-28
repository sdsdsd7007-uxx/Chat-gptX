# Q & Z Autopilot — Engine and Sub-Engine Operating Protocol

**Status:** controlled review loop; human approval required for consequential changes  
**Scope:** repository `sdsdsd7007-uxx/Chat-gptX`, PR #5, QZ / ASSD validation foundation  
**Review cadence:** daily while enabled, plus user-requested reviews

## Mission
Study current evidence, update the remediation plan and engine register, and report verified progress. This protocol does not imply a continuously running agent or authorize production changes.

## Main Engine
1. **Observe:** inspect PR status, latest CI results, changed files, review comments, and relevant source files.
2. **Study:** compare schema, validator, tests, workflow configuration, and acceptance criteria.
3. **Diagnose:** classify each finding as verified defect, unverified risk, missing evidence, or resolved.
4. **Prioritize:** assign P0/P1/P2, impact, likelihood, owner role, dependency, and due/review date.
5. **Plan:** propose the smallest safe change and tests; keep changes on a feature branch.
6. **Verify:** require real test/CI results; never infer success from file creation or a previous run.
7. **Update:** revise this protocol and the remediation plan only when new evidence supports the change.
8. **Report:** summarize changed items, evidence links, blockers, and next action.

## Sub-Engines
- **Schema & Contract:** keep JSON Schema and runtime validation aligned; test boundaries and nested objects.
- **Data Integrity:** define event identity, idempotency, duplicate/conflict handling, replay behavior, and quarantine.
- **Security & Privacy:** least privilege, secret redaction, access review, dependency checks, and no secrets in telemetry.
- **Integration:** verify Dropbox/Odoo connectors only in controlled staging, with scoped permissions and bounded retries.
- **Resilience:** test backup/restore, rollback, interrupted sync, channel failover, and recovery objectives.
- **Governance & Source of Truth:** maintain record ID, source, version, owner, independent reviewer, status, evidence, last verified, next review.
- **Telemetry & Performance:** measure invalid rate, duplicate rate, p50/p95/p99 latency, retry success, backlog age, quarantine counts, and restore outcomes.
- **Ethical & Human Oversight:** keep consequential decisions and production approvals with authorized humans.

## Evidence and status rules
- `DONE` requires reproducible evidence and acceptance criteria.
- `PASS` applies only to the exact commit and workflow run that passed.
- Missing telemetry means `UNKNOWN`, not success.
- Do not claim deployment, Dropbox/Odoo integration, autonomous recovery, or production readiness without direct evidence.
- Do not merge, deploy, change permissions, access production data, or trigger consequential actions without explicit authorization and required review.
- Never expose or request passwords, API tokens, private keys, or encryption keys.
- If CI fails or results are unavailable, report the blocker and propose a fix; do not mark the task complete.
- Stop and request user input when credentials, approvals, ambiguous ownership, or destructive actions are required.

## Daily review output
1. Current PR and CI status.
2. New findings with severity and evidence.
3. Changes actually made and their commit IDs.
4. Open risks and owners/roles needed.
5. Next safe action.
6. Release decision: HOLD unless all required gates are proven.

## Current release gate
**PRODUCTION HOLD** until schema/validator contract tests pass, idempotency/conflict behavior is demonstrated, staging integrations are verified, recovery/rollback tests pass, and an independent authorized reviewer approves release.
