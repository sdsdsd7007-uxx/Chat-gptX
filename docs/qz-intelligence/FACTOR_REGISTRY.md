# Factor Intelligence Registry
**Registry ID:** QZ-INTEL-REG-001  
**Status:** PROPOSED — reconcile with existing QQQ-ISP inventory before adoption.

Each row is a proposed project family, not proof of a running service. Assign an owner, independent reviewer, scope, data classification, source policy, evaluation set and acceptance criteria before implementation.

| ID | Factor project | Core scope |
|---|---|---|
| STR-01 | Strategic Development | Strategy, alignment, execution and adaptation |
| ECO-02 | Macroeconomics | Inflation, rates, FX, growth and labor |
| MKT-03 | Market Intelligence | Demand, competition, pricing and segmentation |
| FIN-04 | Finance & Capital | Cash, margins, liquidity and capital allocation |
| GEO-05 | Geopolitical Risk | Cross-border developments and exposures |
| DIP-06 | Diplomacy & Relations | Treaties, bilateral and regional relationships |
| ERP-07 | Enterprise Systems | ERP workflows, integrations and controls |
| PUR-08 | Purchasing & Suppliers | RFQs, quotes, supplier terms and procurement controls |
| INV-09 | Inventory & Replenishment | Forecast demand, usable stock and confirmed incoming |
| LOG-10 | Logistics & Supply Chain | Freight, transport, lead times and distribution |
| PRD-11 | Productivity & Process | Throughput, cycle time, bottlenecks and errors |
| CUS-12 | Customer & Service | Satisfaction, retention, complaints and service quality |
| PPL-13 | People & Capability | Skills, training, workload and capability |
| QUA-14 | Quality Management | Standards, defects and corrective actions |
| AI-15 | AI & Model Evaluation | Model performance, limitations and evaluation |
| DAT-16 | Data Integrity | Provenance, completeness, consistency and freshness |
| SEC-17 | Security & Authority | Identity, least privilege and tool-boundary controls |
| RSK-18 | Risk & Resilience | Risk, continuity, recovery and stress testing |
| LEG-19 | Law & Regulation | Applicable laws, obligations and official changes |
| TEC-20 | Technology & Innovation | Feasibility, adoption and technology evaluation |
| RES-21 | Research & Science | Literature, evidence synthesis and reproducibility |
| SUS-22 | Sustainability & Environment | Environmental impact and resource efficiency |
| GOV-23 | Governance & Accountability | Decision rights, audit and oversight |
| EDU-24 | StudyCore & Learning | Structured study, synthesis and application review |

## Standard engine stack
1. Scope & Policy — question, boundaries, permitted data and stop rules.
2. Evidence Acquisition — sources, citations, publication/observation dates and provenance.
3. Data Integrity — schema, units, missingness, duplication and freshness.
4. StudyCore — literature, prior work, lessons and knowledge links.
5. Specialist Analysis — domain-appropriate methods.
6. Forecast & Scenario — uncertainty, sensitivity and calibration.
7. Risk & Opportunity — failure modes, alternatives and reversibility.
8. Recommendation — options, trade-offs, dependencies and expected value.
9. Verification — independent checks, tests and reproducibility.
10. Learning — compare outcomes with prior assumptions.
11. Governance & Audit — identity, authorization and accountable ownership.
12. Performance & Resource — latency, cost, error, quality and workload.

## Required output contract
Record project_id, run_id, version, scope, sources, observation_period, freshness, evidence_status, method, assumptions, findings, uncertainty, counterevidence, dependencies, recommendations, KPI references, owner, review_status and next_review.

## Quality gates
- No material claim without traceable evidence or explicit uncertainty.
- No target without owner, baseline method, unit, review date and rationale.
- No model update based only on self-evaluation.
- No cross-factor aggregation until definitions, units and periods are reconciled.
- No consequential action without authenticated authorization at the tool/policy boundary.
