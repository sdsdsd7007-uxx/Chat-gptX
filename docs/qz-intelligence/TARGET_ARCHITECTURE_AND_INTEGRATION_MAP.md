# QZ / ASSD Target Architecture, Integration Contracts & Rules
**Document ID:** QZ-ARCH-002  
**Status:** PROPOSED — design blueprint only, not deployed  
**As of:** 2026-10-29

## 1. Architecture principle

Use a governed platform with modular capability units rather than an unbounded swarm of autonomous agents. Complexity is justified only when separation improves ownership, isolation, evaluation, reuse or fault containment.

`INTENT → SCOPE → AUTHENTICATED IDENTITY → POLICY → PERMITTED DATA → EVIDENCE → ANALYSIS → OPTIONS → APPROVAL → BOUNDED ACTION → VERIFICATION → LEARNING`

The intelligence layer must not grant itself privileges, approve its own high-impact proposal, treat retrieved text as policy, or convert a recommendation into an external side effect without explicit authorization.

## 2. Reference architecture layers

| Layer | Components | Trust boundary / design rule |
|---|---|---|
| 0. Human & governance | User roles, product owner, independent reviewer, decision forum, escalation path | Human rights, decision rights and approval thresholds are explicit |
| 1. Identity & mandate | Workload identity, human principal, token lifecycle, delegated scope, expiry/revocation | Every action is attributable to an identity + environment + policy version |
| 2. Policy control plane | Deterministic policy decision point, capability registry, risk classifier, budget and rate policy | Deny by default; model output is an input to policy, never the authority itself |
| 3. Intake & orchestration | Task router, queue, idempotency keys, deadline, cancellation, bounded planner | Every job has a unique task ID, budget, deadline and recovery behavior |
| 4. Tools & integrations | Allowlisted connectors, API gateway, file/CSV adapters, MCP servers where appropriate | Read/write scopes explicit; no unrestricted shell, network or connector access |
| 5. Evidence & knowledge | Source register, retrieval index, evidence graph, versioned artifacts, conflict/freshness engine | Evidence has origin, timestamp, revision, transformation and permission scope |
| 6. Intelligence modules | Factor units, StudyCore, DIIP, relationship engine, country projects, Market X | Modules are replaceable and evaluated against a shared task set plus domain tests |
| 7. Recommendation & execution | Options comparator, decision record, human approval gate, bounded executor | Approval binds exact action payload, source/evidence version, environment and expiry |
| 8. Telemetry & learning | Traces, logs, metrics, audit ledger, quality evaluation, incident response | Telemetry is observable without disclosing secrets; events preserve lineage |
| 9. Reporting & oversight | Dashboard, source-backed reports, KPI trends, exceptions and review packets | Actual, target, forecast and synthetic examples are visually distinct |

## 3. Core contracts

### 3.1 Task envelope
Minimum fields: `task_id`, `parent_task_id`, `requester_id`, `agent_workload_id`, `purpose`, `scope`, `environment`, `policy_version`, `created_at`, `deadline`, `budget`, `data_classification`, `allowed_tools`, `approval_requirement`, `idempotency_key`, `status`.

### 3.2 Evidence record
Minimum fields: `evidence_id`, `claim_id`, `source_uri`, `source_owner`, `retrieved_at`, `published_at`, `observation_period`, `source_revision_or_hash`, `quoted_or_extracted_span`, `transformation`, `freshness_status`, `confidence`, `permission_basis`, `reviewer`.

Never fill missing source fields with invented values. If a public source does not expose a revision/hash or publication time, record that limitation explicitly.

### 3.3 Recommendation record
Minimum fields: `recommendation_id`, `decision_owner`, `options`, `supporting_evidence_ids`, `assumptions`, `expected_benefit`, `effort`, `risk`, `reversibility`, `confidence`, `affected_systems`, `proposed_action_hash`, `approval_state`, `expiry`, `success_criteria`, `rollback_plan`.

### 3.4 Telemetry event
Minimum fields: `event_id`, `trace_id`, `span_id`, `task_id`, `module_id`, `run_id`, `commit_sha`, `config_version`, `event_time`, `observed_at`, `event_type`, `status`, `duration_ms`, `input_size`, `output_size`, `cost_units`, `error_class`, `source_freshness`, `evidence_quality`.

Avoid secrets, credentials, raw sensitive user content and unnecessary personal data in the telemetry payload.

## 4. Synchronization and consistency rules

1. Use stable identifiers and versioned schemas. Define compatible changes and migration windows.
2. Separate event time from observation/retrieval time. Late or revised source data must be visible.
3. Use idempotency keys for retried writes; deduplicate on the server or integration gateway.
4. Never silently overwrite a conflict. Preserve both source versions and record the resolution rule and reviewer.
5. Use explicit state transitions: `PROPOSED → VALIDATED → REVIEW_REQUIRED → APPROVED → EXECUTED → VERIFIED` or `REJECTED / EXPIRED / REVOKED / ROLLED_BACK`.
6. A successful CI run is valid only for its checked commit and environment. Do not transfer a pass label to a different head without new evidence.
7. Every automated task has timeout, retry ceiling, cost/tool budget, cancellation path and escalation behavior.

## 5. Connector integration pattern

- **Read-only before write:** prove the value and data quality with pull-only integrations. Write scopes are a separate risk decision.
- **Contract adapter:** keep vendor payloads outside the canonical domain model; normalize into versioned internal records.
- **Reconciliation:** compare source counts/totals, timestamps and revisions. Show gaps before using data in a KPI.
- **Credential handling:** short-lived scoped credentials where supported; store outside source code; redact from logs; revoke on incident.
- **Approval boundary:** a permission to read a system never implies permission to change it, create orders, send payments, email third parties or deploy software.
- **Failure behavior:** unknown schema, stale critical input, duplicate command, permission failure or broken lineage blocks high-impact execution.

## 6. Recommended technology evaluation (not a vendor mandate)

| Capability | Candidate pattern / standard | Evaluate for | Main caveat |
|---|---|---|---|
| Agentic repo tasks | GitHub Agentic Workflows (gh-aw), generally available announcement 2026-10-28 | Read-only issue triage, CI failure summaries, documentation/report generation in a sandbox | Evaluate current released version and security advisories first; retain normal PR review and CI gates |
| CI dependency integrity | Full-SHA pins; GitHub Actions workflow dependency lockfiles | Detect mutable action refs and drift | Locking doesn't prove safety; remote reusable workflows require separate verification/pinning because of reported coverage gap |
| Observability | OpenTelemetry traces/metrics/logs where supported | Correlate tool/model steps, costs, errors and latency | Add data minimization, cardinality control and redaction; do not log secrets |
| AI risk management | NIST AI RMF; NIST GenAI Profile; ISO/IEC 42001 management system principles | Governed risk inventory, accountability, impact assessment and continual improvement | Tailor to context; standards alignment is not certification |
| Agent identity | NIST's 2026 agent identity tenets and conventional IAM controls | Distinct workload identity, delegation, expiry, revocation, scope attenuation | Mature implementation needs an actual trusted identity/authorization service |
| Agent security evaluation | OWASP Top 10 for Agentic Applications 2026 / Agent Control resources | Threat-to-test mapping, red-team regression, tool misuse checks | Threat list is a starting point, not a complete custom threat model |
| Data interchange | Versioned JSON/CSV/API contracts with schemas; event envelope and idempotency | Interoperability among spreadsheet, ERP, research and reporting data | Validate business semantics, units and provenance, not syntax alone |
| Enterprise operations | Odoo read-only API/export adapter first | Purchasing, inventory, supplier and PO/receipt/bill analysis | Verify ERP version, permissions, field semantics and data owner before connecting |
| Reporting | Google Sheets plus source-linked Markdown/SVG as interim evidence store | Small controlled operational register and trend reports | For high-volume telemetry, consider an approved database/time-series store; spreadsheets are not the authorization ledger |

## 7. Fail-safe rules

- Missing evidence is UNKNOWN, never zero.
- Source freshness beyond an approved SLA means STALE, not current.
- Untrusted retrieved instructions never alter policy, scope, privileges or approval.
- If authorization service is unavailable, deny high-impact writes; allow only explicitly approved safe read-only behavior.
- If an event is replayed or action hash differs from approval, deny and preserve evidence.
- If budget/deadline/retry limit is reached, stop and report rather than spawning more agents.
- If rollback cannot be verified, do not graduate to production.
- If no independent reviewer is available, retain DRAFT/NOT APPROVED.

## 8. Release ladder

**Level 0 — Design:** architecture, threat model, data inventory, owner, evaluation plan.  
**Level 1 — Offline:** synthetic fixtures, mocks, no production credentials, repeatable tests.  
**Level 2 — Read-only pilot:** approved data sources, bounded access, audit and freshness checks.  
**Level 3 — Controlled staging:** test identity, explicit allowlist, human approval, retry budget, restore drill.  
**Level 4 — Limited production:** written approval, monitoring, incident owner, rollback, time-limited authorization.  
**Level 5 — Expanded scope:** only after measured benefit, independent evaluation and re-approved controls.

No level is passed merely by writing documentation, charting synthetic data or achieving a low runtime number.
