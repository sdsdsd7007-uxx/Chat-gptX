# QZ Intelligence Subprojects — Architecture v1.0

**Status:** PROPOSED / DRAFT — not deployed  
**Review date:** 2026-10-29  
**Release stance:** PRODUCTION HOLD until existing QZ gates are satisfied.

## Purpose
Create modular intelligence projects that study factors independently, test cross-factor relationships, and provide each country with an evidence-grounded project. Shared contracts enable synchronization without erasing context, uncertainty, provenance or independent ownership.

This proposal does not assert that projects, live integrations, automated agents or performance targets already exist.

## Architecture

Project Q + Z / QZ Master Control  
↓  
ASSD / ASD / SD Strategic Orchestrator  
↓  
QQQ Mega-Engine  
├── Factor Intelligence Projects  
├── Country Intelligence Projects  
├── Relationship Intelligence Engine  
└── StudyCore and DIIP  
↓  
QZ Synchronization & Evidence Contracts  
↓  
Recommendation Engine  
↓  
Policy + Authenticated Approval Gate  
↓  
Bounded Authorized Action  
↓  
Independent Verification & Outcome Measurement  
↓  
Learning and next cycle

## Core rules
1. Intelligence proposes; policy evaluates; authenticated authorization permits; bounded execution acts; independent evidence verifies.
2. Each factor retains its own scope, owner, evidence register, evaluation suite and version.
3. Country projects share schemas but retain country-specific sources, definitions, laws and uncertainty.
4. Correlation is not causation. Scenario sensitivities are not predictions.
5. Missing values remain UNKNOWN or NOT CONNECTED; never substitute zero.
6. No self-approval, hidden privilege expansion, automatic purchase orders, unapproved financial actions or production deployments.
7. A 100-microsecond target applies only to selected lightweight local operations under a defined workload—not full research.

## Project files
- FACTOR_REGISTRY.md — initial factor domains and standard engine stack.
- COUNTRY_PROJECT_TEMPLATE.md — country-level project standard.
- RELATIONSHIP_INTELLIGENCE.md — cross-factor analysis and synchronization.
- KPI_AND_PERFORMANCE_REPORTING.md — KPI definitions and progress/time graph rules.
- IMPLEMENTATION_PLAN_AND_ACCEPTANCE.md — staged plan, tests and release gates.

## Portfolio expansion — 2026-10-29

The initial domain/relationship/country design has been extended with a governed opportunity portfolio spanning trust, evidence, intelligence, Market X, operations, enterprise integration, engineering, people and adoption. All entries remain **PROPOSED** until ownership, data access, baseline, acceptance and review are confirmed.

- [Opportunity portfolio — proposed engines and subprojects](OPPORTUNITY_PORTFOLIO.md)
- [Target architecture, integration map and contracts](TARGET_ARCHITECTURE_AND_INTEGRATION_MAP.md)
- [Integration, strategic stakeholder and adoption strategy](PARTNERSHIP_AND_ADOPTION_STRATEGY.md)
- [Experiment backlog, 90-day sequence and graph contracts](EXPERIMENT_BACKLOG_AND_ROADMAP.md)
- [Technology and standards horizon scan — 2026-10-29](TECHNOLOGY_AND_STANDARDS_HORIZON_SCAN.md)
- [QZ/ASSD performance and progress report with graphs](reports/QZ_ASSD_Performance_Progress_Report_2026-10-29.md)
- [CI duration trend (SVG)](reports/CI_DURATION_TREND.svg)
- [CI outcome distribution (SVG)](reports/CI_OUTCOME_DISTRIBUTION.svg)
- [Raw CI run history (CSV)](reports/CI_RUN_HISTORY_2026-10-29.csv)

### New live technology signals to evaluate (not activate automatically)

GitHub announced Agentic Workflows general availability on 2026-10-28 and Actions workflow dependency lockfiles general availability the same day. Agentic workflow automation is a possible fit for read-only issue triage, CI failure analysis and documentation/report generation, but only in an isolated sandbox after verifying current versions and security advisories. The official `gh-aw` repository notes a retired vulnerable version range (v0.83.3 up to but excluding v0.85.4); version/source verification is a mandatory prerequisite. For dependency lockfiles, remote reusable workflows called via `jobs.<id>.uses` remain a separately handled gap in upstream issue #179. The inspected workflow files did not contain such calls, so no present exposure is confirmed in that inspected set. See the horizon-scan document for sources and details.

**Current control state:** CI-only performance graph available; application/agent production telemetry remains NOT CONNECTED. Proposal/test states remain PROPOSED — NOT RUN where stated. Production remains HOLD pending independent review, trusted authorization, staging tests, recovery/rollback proof and explicit release approval.



## v114.0 concept track — Omniversal Hyper-Nexus

The requested v114.0 label is maintained as a **concept/design track**, aligned to the existing Dropbox **v121.0 assurance pack**. It does not replace the current v121 record or imply production release. The v121 pack states that its tests remain NOT RUN and that production is HOLD.

- [v114.0 Hyper-Nexus blueprint](PROJECT_QZ_V114_OMNIVERSAL_HYPER_NEXUS_BLUEPRINT.md)
- [MD-SIU intelligence specification](MD_SIU_MULTI_DIMENSIONAL_INTELLIGENCE_SPEC.md)
- [QR-DTS sync and reconciliation design](SYNC_RECONCILIATION_SPEC.md)
- [UVSGM values governance matrix](UVSGM_VALUES_GOVERNANCE_MATRIX.md)
- [v114 acceptance and integration roadmap](V114_TO_NEXT_BASELINE_ROADMAP.md)
- [v114 proposed acceptance test matrix](V114_ACCEPTANCE_TEST_MATRIX.csv)
- [Hyper-Nexus architecture map](V114_ARCHITECTURE_MAP.svg)
- [Assurance inventory overview](V114_ASSURANCE_INVENTORY_OVERVIEW.svg)
- [Proposed roadmap Gantt](V114_PROPOSED_ROADMAP_GANTT.svg)

The inventory graph counts documented assurance records, not passed tests or real-world performance. Application/runtime telemetry remains NOT CONNECTED; the existing CI timing chart measures CI workflow wall time only. All v114 tests remain PROPOSED — NOT RUN, and production HOLD is unchanged.

## Inventory-count reconciliation — OPEN

The numbers currently used across the QZ/QQQ materials describe different and not-yet-reconciled inventory concepts:

| Label | Current interpretation | Authority |
|---|---|---|
| 24 factor entries | Proposed domain catalogue in `FACTOR_REGISTRY.md`; not proof of 24 active services or approved projects | PR #9 proposal only |
| “12-domain” | Historical label referenced in the master-control discussion; authoritative list and mapping not yet verified here | OPEN |
| “eight-project network” | Historical architecture label; membership and relationship to the 12-domain list are not yet verified here | OPEN |

**Control rule:** do not add, remove, rename, merge or report a canonical project count until the owner-approved source-of-truth inventory is retrieved and reconciled. Build a mapping of canonical ID, display name, parent/subproject relationship, lifecycle state (proposed/active/retired), accountable owner, repository path and evidence link. Distinguish *domains*, *project families*, *subprojects* and *running services*; they are not interchangeable counts.

**Exit criteria:** the accountable owner confirms the source-of-truth list; all historical labels are mapped or explicitly retired; duplicate/alias IDs are recorded; an independent reviewer verifies the mapping; the master register and this proposal link to the same versioned inventory. Until then, inventory reconciliation remains **OPEN / BLOCKING CANONICAL ADOPTION**.

## Reuse existing QZ components
Complement PR #8 (QZ Autopilot Master Control Register), PR #4 (QZ/ASSD validation), and PR #5/#7 (QQQ/StudyCore/Mega-Engine). Reconcile existing IDs and the 12-domain/eight-project wording before declaring a canonical inventory. Do not duplicate or silently rename existing subprojects.

## Evidence labels
VERIFIED = checked for stated scope; REPORTED = attributed source claim; ESTIMATED = method and assumptions disclosed; STALE = outside freshness window; UNKNOWN = insufficient evidence; NOT CONNECTED = source unavailable; PROPOSED = not implemented/tested.

## Decision flow
SCOPE → PERMITTED INGESTION → VALIDATE → STUDY FACTORS → TEST RELATIONSHIPS → COUNTRY CONTEXT → RECOMMEND → AUTHORIZE → EXECUTE WITH BOUNDS → VERIFY → LEARN.

Related control register: https://github.com/sdsdsd7007-uxx/Chat-gptX/pull/8. These documents do not close its independent-review, authorization, staging, recovery or release blockers.
