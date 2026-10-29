# QZ / ASSD Innovation Opportunity Backlog — Research Snapshot

**Document ID:** QZ-INNOVATION-BACKLOG-2026-10-29-01  
**Review date:** 2026-10-29  
**Status:** RESEARCH / PROPOSED — no new service, integration, partnership, automation or production capability is asserted as active.  
**Parent:** QZ Intelligence subprojects; align with PR #8 master-control register and PR #9 proposal before adoption.  
**Release posture:** PRODUCTION HOLD remains unchanged.

## 1. Executive recommendation

Do not create dozens of disconnected engines immediately. First build a reusable **Evidence-to-Action Control Plane**: an authoritative inventory, source/provenance register, deterministic policy gate, evaluation harness, bounded connector catalogue, audit trail, and outcome dashboard. Add domain engines only when a named use case, owner, data permission, measurable benefit, acceptance test and support plan exist.

The strongest opportunity is to combine agent identity and governance, AI testing/evaluation/verification/validation (TEVV), AI observability, and workflow supply-chain controls into one verifiable operating model. These are complementary layers, not competing products.

## 2. New subprojects and engines to consider

Priority is qualitative (P0/P1/P2), not a measured score. Effort is a planning estimate to refine after discovery.

| Priority | Proposed module / program | Why it matters | First bounded deliverable | Main success measure | Key dependency / risk |
|---|---|---|---|---|---|
| P0 | **Source-of-Truth & Asset Registry** | Resolves conflicting project/domain counts and duplicate aliases | Versioned inventory of projects, subprojects, workflows, datasets, connectors, owners and lifecycle states | Share of in-scope records with canonical ID, owner, evidence link and state | Owner confirmation; do not infer canonical counts |
| P0 | **Evidence Provenance & Freshness Engine** | Prevents stale, unsupported or misattributed facts from silently becoming decisions | Common evidence record: source, timestamp, retrieval time, scope, license/permission, confidence label, expiry rule and hash where appropriate | Traceability coverage; stale-source detection; correction rate | Source access, data rights and freshness policy |
| P0 | **Agent Identity & Authority Gate** | Separates a model’s suggestion from authenticated permission to act | Threat model and test matrix for identity, delegated scope, expiry, revocation, replay, changed payload and human escalation | Negative tests reject unauthorized, expired or altered actions | Independent security review; trusted identity service |
| P0 | **TEVV / Evaluation Harness** | Makes claims testable and repeatable before release | Versioned test cases, held-out cases, deterministic checks, human calibration and reproducible result format | Pass rate by test family; critical-failure count; regression rate | Tests must be independently reviewed and actually run |
| P0 | **AI & Workflow Observability** | Distinguishes model quality, tool behavior, system latency and CI timing | Correlation IDs and structured events for source retrieval, policy decisions, tool calls, errors, latency and outcome | Trace completeness; failure classification; p50/p95/p99 by defined workload | Privacy minimization; instrumentation not yet connected |
| P1 | **Integration Contract Registry** | Reduces brittle one-off integrations | Catalogue of connectors with owner, permissions, schema, rate limits, data classification, test mode and rollback behavior | Contract-test coverage; breaking-change detection | Each connector needs explicit user/org authorization |
| P1 | **Data Quality & Semantic Layer** | Makes KPI comparisons consistent across projects and countries | Metric dictionary, unit/currency/time-zone conventions, lineage and validation rules | Missingness, duplication, reconciliation and definition-drift rates | Business owners must approve metric definitions |
| P1 | **Scenario & System-Dynamics Lab** | Tests feedback loops and assumptions without presenting scenarios as predictions | Small causal-loop model with assumptions, sensitivity ranges and validation notes | Assumption traceability; sensitivity coverage; forecast calibration when outcomes exist | Correlation is not causation; domain review required |
| P1 | **Market X Intelligence Workbench** | Organizes macro, sector, competitor, customer, technology and policy signals | Evidence-backed briefing with date, geography, source quality, change vs. prior period and implications | Timeliness, citation coverage, useful-action rate | Live data feeds remain NOT CONNECTED until verified |
| P1 | **Country & Geo-Segmentation Pack** | Supports country-aware comparisons without erasing local context | Country schema for demographics/economy/regulation/infrastructure plus data-quality flags | Coverage by geography; comparability warnings; source freshness | Use lawful, reputable aggregate data; avoid unsupported inferences |
| P1 | **Workflow Supply-Chain Hardening** | Reduces mutable dependency and untrusted workflow risks | Inventory every action, reusable workflow, local action, container and dependency; pilot official lockfile tooling in an isolated branch | Inventory coverage; pinned/locked coverage; clean validation run | Locking does not prove dependencies are benign |
| P1 | **Risk, Incident & Recovery Exercise Program** | Tests whether controls work during failure, not only in normal paths | Tabletop exercises and controlled staging recovery tests | Recovery objectives met; evidence of restore-and-retest | Approved scope, safe staging and reviewer required |
| P1 | **Value Realization & Benefits Ledger** | Prevents “AI savings” or ROI claims without baselines | Per-use-case baseline, counterfactual, cost, quality, time saved and attribution method | Verified net benefit with uncertainty and quality guardrails | Baseline and attribution must be agreed before pilot |
| P2 | **Knowledge & Learning Studio (StudyCore)** | Converts research into reusable learning and decision support | Curated source notes, concept maps, spaced review and assessment rubric | Learning outcomes and reuse, not page count | Copyright, source quality and human review |
| P2 | **Human-Centered Service Design** | Makes systems useful, understandable and accessible | Interviews, journey map, accessibility review and feedback loop | Task completion, user-reported usefulness, accessibility issues closed | Consent, privacy and representative sampling |
| P2 | **Responsible Open-Source & Research Program** | Builds review capacity and reduces isolated reinvention | Public issue backlog, contribution rules, reproducible examples and citation policy | Reproducible contributions, review turnaround, issue resolution | Do not publish secrets, personal data or unreviewed sensitive material |
| P2 | **Skills & Change Adoption Program** | Addresses the organizational work needed to realize technical value | Role-based learning paths, operating procedures and change-impact map | Competency checks, adoption, support burden and user feedback | Named business sponsors and protected staff time |
| P2 | **Partnership Discovery Desk** | Finds complementary research, standards, education and implementation partners | Non-binding partner map with purpose, fit, evidence, risks and next step | Qualified introductions and jointly validated pilot proposals | No endorsement, commitment or data-sharing assumption |

## 3. Reference architecture: Evidence-to-Action Control Plane

**Signal / request → scope & permissions → source retrieval → provenance + freshness checks → factor/country analysis → relationship & scenario tests → recommendation → deterministic policy decision → authenticated approval (when required) → bounded execution → independent verification → outcome measurement → learning.**

Shared services:
- **Registry:** canonical IDs, versioning, ownership, lifecycle and dependencies.
- **Evidence ledger:** source, retrieval time, permitted use, freshness, claim supported and uncertainty.
- **Policy gate:** explicit allow/deny/escalate decisions; fail closed on unknown authority.
- **Evaluation harness:** unit, integration, resilience, regression and human-review tests.
- **Observability:** traces, metrics, logs, cost, latency, errors and outcome linkage.
- **Recovery controls:** staging, backups, restore drills, rollback criteria and incident ownership.
- **Reporting:** actuals, targets and forecasts shown separately; missing data shown as UNKNOWN/NOT CONNECTED, never as zero.

## 4. Rules and operating principles

1. **Evidence before confidence:** every material recommendation should show its sources, timestamp, scope, uncertainty and assumptions.
2. **Propose is not authorize:** model output, retrieved content, issue text or connector result is data, not permission.
3. **Least privilege:** each connector and agent receives only task-required access; prefer short-lived, revocable authorization.
4. **Human escalation:** require authorized review for high-impact, irreversible, privacy-sensitive, financial or production actions.
5. **Independent verification:** the actor proposing or executing a change should not be its sole approver or verifier.
6. **Reproducibility:** record commit, configuration, input dataset/version, test environment and evidence references for material results.
7. **Fail closed:** unknown identity, stale approval, schema mismatch, missing provenance or failed critical test blocks execution.
8. **Data minimization:** collect only necessary data, honor consent and access rules, set retention limits and avoid unnecessary sensitive attributes.
9. **No metric gaming:** report quality, safety, reliability, cost and latency together; do not optimize speed at the expense of correctness.
10. **Clear lifecycle:** distinguish PROPOSED, DISCOVERY, PILOT, VERIFIED, APPROVED, ACTIVE, SUSPENDED and RETIRED. Do not label a concept as deployed.
11. **Separate observations from causal claims:** correlations and scenarios do not prove causation or predictability.
12. **No false precision:** targets, estimates and qualitative priorities must be labeled and justified.

## 5. External standards, research and partnership candidates

These are research leads, not endorsements or existing partnerships.

- **NIST / CAISI and NCCoE:** agent standards, identity and authorization; useful for mapping identity, delegated authority and interoperability controls. Sources: [AI Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure), [Software Agent Identity and Authority concept paper](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents).
- **NIST TEVV-Athlon:** a structured method for tailoring AI testing, evaluation, verification and validation to a use case. Adapt it to QZ acceptance tests rather than claiming generic benchmark scores are sufficient. [Framework](https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems).
- **CISA and international cyber agencies:** guidance on careful adoption of agentic AI, including bounded autonomy, layered defenses, identity, monitoring and threat modeling. [Joint guidance](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/41544ff).
- **Australian Signals Directorate (ASD) / ACSC:** agent harness security and governance; relevant to the tool/data boundary surrounding a model. [Agentic AI harness guidance](https://www.cyber.gov.au/news/asd-releases-new-guidance-on-the-agentic-ai-harnesses).
- **Cloud Security Alliance:** reference architecture and control-plane thinking for AI agents. [AI Agents: Architecture and Control Plane](https://cloudsecurityalliance.org/artifacts/ai-agents-architecture-and-control-plane).
- **IEEE Standards Association:** emerging work on autonomous-agent governance and AI observability. Treat as active standards-development work, not final adopted standards. [P1968 agent governance project](https://standards.ieee.org/ieee/1968/12749/), [P4213 AI observability project](https://standards.ieee.org/ieee/4213/12758/).
- **GitHub:** workflow dependency lockfiles reached general availability on 28 October 2026 for supported plans. Pilot official tooling only after inventory and review; the lockfile does not establish dependency safety. [Official announcement](https://github.blog/changelog/2026-10-28-github-actions-workflow-lockfiles-are-generally-available/).
- **University and regional ecosystem discovery:** consider non-exclusive conversations with universities, standards groups, public-interest technology communities and relevant East African digital-innovation networks for research methods, local context, evaluation and skills development. Identify specific institutions only after transparent fit-and-due-diligence review; no partnership is implied here.

## 6. First 30 / 60 / 90 days — proposed sequence

### Days 0–30: establish truth and safety
- Reconcile the canonical inventory against the PR #8 master register and existing PR #1/#2/#4/#5/#7/#8/#9 scopes.
- Publish the common evidence record, lifecycle states, metric dictionary and decision/authorization boundary.
- Inventory current workflow and connector permissions; verify exact-head CI and review state.
- Select one low-risk, read-only pilot with a clear user and measurable baseline.
- Define TEVV acceptance criteria before implementation.

**Exit gate:** inventory owner confirmed; data access approved; threat model and test plan reviewed; baseline and rollback plan written.

### Days 31–60: controlled pilot
- Implement only the minimum reusable registry/provenance/observability components required by the chosen pilot.
- Run repeatable tests, stale-data tests, schema-failure tests and authorization-denial tests in controlled staging.
- Collect timestamped performance and quality measurements with reproducible raw rows.
- Conduct user feedback and accessibility review; document training/support needs.

**Exit gate:** critical tests pass on exact commit; failures are classified; independent reviewer signs off; recovery exercise evidenced.

### Days 61–90: decide based on evidence
- Compare results against baseline and pre-agreed acceptance thresholds.
- Publish benefit, cost, quality, latency, risk and uncertainty together.
- Decide to scale, revise, keep in pilot or retire. Do not scale merely because the demo works.
- Expand to the next domain only after the previous gate passes.

**Exit gate:** documented decision owner, evidence-backed benefits, accepted residual risk and explicit release approval. Production stays on HOLD until all existing QZ gates are satisfied.

## 7. Measurement framework

Report these separately and do not invent values:
- **Evidence:** source coverage, freshness compliance, traceability, correction rate.
- **Quality:** task success, factual error rate, unsupported-claim rate, human disagreement and regression rate.
- **Safety/security:** unauthorized-action block rate, privilege scope, revocation effectiveness, unresolved critical findings.
- **Reliability:** successful runs, classified failures, cancellations, availability and recovery evidence.
- **Performance:** p50/p95/p99 by workload, queue/network/model/local compute split, throughput and cost per successful outcome.
- **Value:** baseline-to-outcome change, staff time, operating cost, service quality and uncertainty/attribution.
- **Adoption:** task completion, user feedback, training completion and support burden.
- **Governance:** owner coverage, review status, data permissions, open risks and release-gate status.

Use time-series graphs only when at least two valid timestamped observations exist for the same metric definition and comparable workload. Show sample counts and gaps; label targets and forecasts separately from actuals. Current product/agent production telemetry remains **NOT CONNECTED** until verified.

## 8. Immediate next actions

1. **P0 — Inventory reconciliation:** retrieve and reconcile the approved master inventory; keep canonical counts open until an accountable owner confirms them.
2. **P0 — Authority and evaluation:** convert existing AA-001–AA-014 and QZ-AT-001–023 proposals into a reviewed, traceable staging execution plan; they remain NOT RUN until evidence exists.
3. **P0 — CI dependency controls:** complete a full ref-specific workflow inventory, review action and reusable-workflow references, then pilot lockfile generation on an isolated branch and verify exact-head CI.
4. **P1 — Observability pilot:** select one read-only use case and define its event schema, baseline, acceptance thresholds and privacy boundaries before connecting telemetry.
5. **P1 — Market X data plan:** define a source catalogue and freshness windows for macro, sector, country, competitor and policy signals; do not describe it as live until feeds and timestamps are verified.
6. **P2 — Partnership discovery:** prepare a one-page research brief and due-diligence checklist; make no commitments or data-sharing promises without approval.

## Conclusion

The highest-leverage innovation is not “more engines” by itself. It is a **modular, evidence-first and permission-aware platform** where every proposed engine shares provenance, evaluation, observability, governance and value measurement. Build the control plane first, validate one bounded pilot, and expand only when the evidence supports it.

**Current verified status:** this document is a proposal. It does not establish that integrations, partnerships, tests, live feeds, production telemetry or new subprojects are active. PR #9 remains a draft proposal; exact-head CI and independent review must be rechecked before any release decision.
