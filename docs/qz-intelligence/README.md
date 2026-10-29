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
