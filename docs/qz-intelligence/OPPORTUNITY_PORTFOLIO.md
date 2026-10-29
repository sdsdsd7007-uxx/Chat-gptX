# QZ / ASSD / QQQ / Market X — Opportunity Portfolio
**Portfolio ID:** QZ-IDEA-PORTFOLIO-001  
**As of:** 2026-10-29  
**Status:** PROPOSED — discovery and prioritization register, not a claim of implementation  
**Scope:** Technical and nontechnical ideas that extend the existing Project Q, Project Z, QZ, ASSD/ASD/SD, QQQ, StudyCore, DIIP and Market X work.

## Decision summary

Build a **small, governed evidence-and-decision platform first**, not dozens of independent autonomous agents. Each proposed project must have an accountable owner, a defined decision/user, permitted sources, measurable acceptance tests, operating cost/budget, failure behavior, and a support plan. Split an idea into a separate subproject only when its boundary, data, evaluation, risk or owner genuinely differs.

### Priority convention

- **P0 — foundation:** required to make later work safe and trustworthy.
- **P1 — pilot candidate:** useful after P0 contracts and ownership are in place.
- **P2 — explore:** option with value potential but more uncertainty or dependencies.
- **P3 — watchlist:** retain for horizon scanning; do not build until evidence supports it.

Priorities below are *qualitative portfolio judgments*, not measured ROI or approved commitments. No cost, demand, savings, partnership, deployment or production KPI is implied.

## A. Trust, evidence and governance projects

| ID | Proposed subproject / engine | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| GOV-01 | Agent Identity & Delegation Engine | P0 | Cryptographically attributable agent identity; bounded, expiring, revocable delegated mandates | Unknown, expired, revoked, replayed or over-scoped request is denied and audited |
| GOV-02 | Deterministic Policy Decision Point | P0 | Separate policy/permission decisions from model prose and generated plans | Same request + same policy version gives same allow/deny outcome; model wording cannot bypass it |
| GOV-03 | Human Approval & Change Control | P0 | Risk-tiered approval, exact proposal binding, two-person approval for critical actions where warranted | Altered proposal, wrong approver, stale approval and self-approval fail closed |
| EVD-01 | Evidence Provenance & Claim Graph | P0 | Link claims, source fragments, timestamps, transformations, reviewer and output version | Material claims are traceable; missing or invalid provenance remains UNKNOWN |
| EVD-02 | Source Freshness & Conflict Resolver | P0 | Source-specific freshness SLA, revision handling, conflict detection, authoritative-source ranking | Stale/conflicting values are flagged, not silently averaged or treated as current |
| GOV-04 | Tamper-Evident Audit Ledger | P0 | Append-only decision events with request, policy, approval, tool and outcome IDs | Mutation/reordering/replay is detected; restore evidence is retained |
| GOV-05 | Privacy, Retention & Data Boundary | P0 | Data classification, minimization, redaction, consent/permission, retention and deletion workflows | Synthetic sensitive records do not leak into logs, traces or exports |
| QA-01 | Evaluation & Red-Team Lab | P0 | Offline regression, adversarial, prompt-injection, tool-misuse, refusal and output-quality tests | Every release candidate has a versioned test pack, retained logs and independent review |
| QA-02 | Model / Tool Change Impact Testing | P1 | Compare candidates against the same representative task/evidence set | No candidate promoted solely on speed; quality, safety, cost and latency compared together |

## B. Shared intelligence and strategy engines

| ID | Proposed subproject / engine | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| INT-01 | StudyCore Knowledge Ledger | P1 | Structured study notes, citations, concepts, assumptions, confidence and application checks | Each decision-relevant statement links to evidence and distinguishes fact vs interpretation |
| INT-02 | DIIP Research & Synthesis Pipeline | P1 | Define question → retrieve → validate → compare → synthesize → review → publish | Repeat run can reproduce source set and material conclusions, or explain changes |
| INT-03 | Factor Intelligence Units | P1 | Independent domain modules with common contracts but domain-specific metrics | Each unit has owner, evidence pack, test pack, scope and explicit unsupported cases |
| INT-04 | Relationship Intelligence Engine | P1 | Dependency graphs, competing explanations, lead/lag, scenario sensitivity and confounders | Associations are not labeled causal without an appropriate design/evidence |
| STR-01 | SD / ASD Strategy Development Loop | P1 | Scan → analyze → scenarios → choose → plan → budget → align → execute → measure → review → adapt | Every strategic action has assumption, owner, KPI, time horizon and review trigger |
| STR-02 | Decision Journal & Benefits Realization | P1 | Record options, reasons, forecast, confidence, owner, expected outcome and later outcome | Forecasts and outcomes can be compared without rewriting the original rationale |
| STR-03 | Scenario & Early-Warning Engine | P1 | Green/red/as-is and alternative plausible futures, indicators and response triggers | Scenario assumptions are visible; alerts specify evidence, uncertainty and action owner |
| STR-04 | Risk-Adjusted Prioritization Engine | P1 | Rank by expected benefit, effort, reversibility, evidence confidence and downside | Priority is reproducible and does not hide hard safety/compliance gates |

## C. Market X, country and sector intelligence

| ID | Proposed subproject / engine | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| MX-01 | Market X Evidence Dashboard | P1 | One-picture view of sources, KPIs, risks, changes, decisions and freshness | Each displayed metric has timestamp, unit, source and freshness indicator |
| MX-02 | Uganda Country Intelligence Pilot | P1 | Official macroeconomic, sector, business and public-data register with definitions | Periods, units, revisions and source URLs verified before comparison |
| MX-03 | Geo-Sector Segmentation | P2 | Country → region → district → sector → segment; only at available/authorized granularity | Geographic coverage and missingness displayed; no invented subnational data |
| MX-04 | Market Signal & Demand Engine | P2 | Demand signals, competitors, customer behavior and leading indicators | Back-test on historical data; compare to a simple baseline; show uncertainty |
| MX-05 | Country Comparability Engine | P2 | Harmonize definitions, currencies, periods and denominators across countries | Blocks invalid apples-to-oranges comparisons instead of forcing a rank |
| MX-06 | Strategic Morning Brief Generator | P1 | Summarize material changes, top risks, decisions due and sources in one image/report | Each recommendation traces to evidence; “no material change” differs from missing data |

## D. Operations, procurement and enterprise systems

| ID | Proposed subproject / engine | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| OPS-01 | Odoo Read-Only Integration Adapter | P1 | Import approved product, vendor, stock, PO, receipt and bill data | Reconciled row counts and totals; credentials read-only; no writes |
| OPS-02 | Risk-Adjusted Replenishment Engine | P1 | Forecast demand over lead-time + review period, usable stock, confirmed inbound, safety stock | Historical back-test vs simple reorder baseline; stockout/overstock trade-offs measured |
| OPS-03 | Supplier & Lead-Time Intelligence | P2 | Supplier performance, lead-time variability, quality, concentration and resilience | Source-backed scorecard with sample count and missing-data flags |
| OPS-04 | Purchase-to-Pay Reconciliation | P2 | PO ↔ receipt ↔ vendor bill, duplicate detection and exception queue | Discrepancies surfaced for human review; no autonomous payment execution |
| OPS-05 | Inventory Expiry / Quality / Waste Watch | P2 | Ageing stock, expiry, returns, QC and waste reasons | Alerts tied to lot/item, source and owner; thresholds approved by operators |
| OPS-06 | Operations Bottleneck & Time Study | P2 | Activity → queue → delay → rework → output analysis | Baseline method is documented; interventions compared against baseline |

## E. Engineering, integration and performance

| ID | Proposed subproject / engine | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| ENG-01 | Tool / Connector Registry | P0 | Inventory every connector, actions, data scopes, write capabilities, owner and risk | Unknown connector/tool denied by default; schema and permissions reviewed |
| ENG-02 | Integration Gateway | P1 | Versioned API/CSV/event adapters, idempotency, retry budgets and rate limits | Duplicate/out-of-order events handled without duplicate side effects |
| ENG-03 | Observability & Time-Series Store | P0 | Correlation IDs, traces, metrics, logs, cost and source freshness | Per-run trace joins request, model/tool step, policy decision and final outcome |
| ENG-04 | Performance Benchmark Harness | P1 | p50/p95/p99, throughput, errors, concurrency, resource cost and correctness | Benchmarks are reproducible across pinned workloads/runtime/hardware |
| ENG-05 | CI Supply-Chain Hardening | P0 | Reviewed full-SHA action pins or carefully piloted lockfiles; transitive dependency review | Coverage check does not silently omit dependency classes; PR gate passes |
| ENG-06 | Data Contract & Schema Registry | P0 | Versioned event, evidence, recommendation, country and relationship schemas | Valid, invalid, old-version and partial payload fixtures tested |
| ENG-07 | Safe Retry / Idempotency / Recovery Engine | P0 | Bounded retry, cancellation, dead-letter queue, backup, restore and rollback | Replayed request does not duplicate external side effects; recovery is demonstrated |
| ENG-08 | Multi-Model Routing & Cost Guard | P2 | Route tasks by evaluation outcome, data handling, capability, latency and budget | Chosen model passes quality/security threshold; spend limit fails closed |
| ENG-09 | Retrieval / RAG Quality Engine | P2 | Citation coverage, retrieval recall, source ranking, stale-source detection and abstention | Benchmark evaluates both retrieval and grounded final answers |
| ENG-10 | Release Evidence Pack Builder | P1 | Collect commit, environment, tests, reviewer, source and restore evidence | Release packet generated reproducibly; missing mandatory evidence blocks release |

## F. People, adoption, learning and sustainable value

| ID | Proposed program | Priority | Intended capability | First measurable acceptance |
|---|---|---:|---|---|
| ORG-01 | Product Owner & Decision Forum | P0 | Clear decision rights, priorities, exceptions and escalation | Every P0 initiative has named accountable owner and independent reviewer |
| ORG-02 | Change Adoption & Skills Program | P1 | Role-based training, SOPs, feedback loops and practical assessments | Adoption measured by successful task completion, not attendance alone |
| ORG-03 | Partner & Stakeholder Discovery | P1 | Structured partner map, problem interview, data permission and pilot criteria | No partnership reported until counterpart approves and agreement is documented |
| ORG-04 | Benefits & Public Value Ledger | P1 | Record expected vs observed time saved, quality, service, cost and stakeholder outcomes | At least one reviewed before/after comparison before claiming impact |
| ORG-05 | Ethical, Accessible & Inclusive Design | P1 | Accessibility, appeals, explanations, language support and human alternatives | Representative user checks and documented remediation |
| ORG-06 | Sustainability & Resource Efficiency | P2 | Measure compute/resource use where feasible, reuse/cache policy, model right-sizing | Resource measurements accompany quality and latency, not replace them |
| ORG-07 | Learning & Knowledge Transfer | P1 | Runbooks, decision records, training notes, succession and handover | Another authorized maintainer can operate and restore the pilot from docs |

## Recommended first portfolio slice

1. **P0 foundation:** identity/delegation, deterministic policy, evidence graph, source freshness, tool inventory, audit, schema registry, observability and release evidence.
2. **P1 controlled pilot:** CI reporting, StudyCore/DIIP, Market X source-backed briefing, Uganda official-source pilot and Odoo read-only reconciliation only if the required data owner approves access.
3. **P1 operational validation:** benchmark harness, negative tests, staged recovery, independent review and benefits baseline.
4. **P2 expansion:** demand forecasts, geographic segmentation, multi-model routing, broader countries/sectors and partner-led pilots only after the first pilot passes acceptance.

## Portfolio rule

Do not create a new “engine” merely to rename a feature. Every subproject must answer: (1) whose decision improves; (2) what evidence it consumes; (3) what it may not do; (4) how quality is measured; (5) who owns it; (6) how it fails safely; and (7) what would justify stopping it.
