# QZ Portfolio — Integrations, Strategic Partnerships & Adoption
**Document ID:** QZ-PARTNERS-001  
**Status:** PROPOSED — prospect and operating-model guide, not a record of contacted or contracted partners  
**As of:** 2026-10-29

## 1. Partnership thesis

Partnerships should close a specific gap in official data access, technical assurance, domain expertise, user validation, education or deployment support. Do not pursue logos or integrations without a named use case, permission to use data, mutual benefit, a data/ownership agreement and an exit route.

**No organization listed below has been contacted or agreed to partner on the basis of this document.** Names are potential stakeholder categories/examples for discovery only.

## 2. Integration map

| Integration | Initial mode | Value hypothesis | Required controls / evidence | Priority |
|---|---|---|---|---:|
| GitHub repository, Actions and issues | Read-only inspection; propose docs/PR changes | Traceable code, tests, issues and release records | Exact commit/branch, scoped write permissions, independent review, protected branch check | P0 |
| Google Sheets register | Read/write only in specified project ranges | Accessible issue, KPI, risk and test register | Verify sheet/range IDs, preserve rows, validate output after writes, avoid using it as authoritative security ledger | P0 |
| Dropbox / file library | Read-only by default, approved saves | Durable research and evidence artifacts | Confirm destination, source version and audience; avoid public links for sensitive data | P1 |
| Odoo ERP | Read-only API/export pilot | Procurement/inventory reconciliation and stock insight | Owner approval, minimum fields, field mapping, data minimization, totals reconciliation, no write scope | P1 |
| Official public data feeds | Pull-only, source-specific adapter | Current-country/sector indicators | Use the official publication, record release/revision time, definitions, units and freshness SLA | P1 |
| OpenTelemetry or compatible collector | Instrumentation pilot | Trace task → model/tool → policy → outcome and timing | Approved collector destination, redaction, retention and access control | P1 |
| Identity / IAM service | Trusted authorization integration after design | Verifiable actor identity and least-privilege mandate | Security review, key/token lifecycle, revocation, audit and fail-closed negative tests | P0 |
| Model-provider APIs / local models | Offline evaluation before connection | Capability, quality, latency, privacy and cost trade-offs | Data policy, approved endpoint, key handling, repeatable test pack and kill switch | P2 |
| Email/calendar collaboration | Explicit read-only workflow after user/owner approval | Decision meetings, tasks and reminders | Minimize personal data, resolve access scope, never email or invite external parties without approval | P2 |

## 3. Potential strategic stakeholders — discovery only

### Public data, economic policy and statistics
- **Uganda Bureau of Statistics (UBOS):** potential source/data-definition discussion for official statistics and regional/sector data, subject to public availability and terms.
- **Ministry of Finance, Planning and Economic Development (MoFPED):** potential official economic report and fiscal-data source mapping.
- **Bank of Uganda:** potential monetary/financial indicators and definitions; do not interpret historical rates or exchange-rate averages as live quotes.
- **National Information Technology Authority–Uganda (NITA-U):** potential standards, public digital service and interoperability guidance where relevant.
- **Personal Data Protection Office (PDPO):** consult authoritative public privacy guidance and applicable requirements; do not imply endorsement or certification.
- **Relevant ministries and district/local-government data owners:** approach only for a specific service/use case, permitted dataset and written authorization.

### Research, skills and independent assurance
- **Ugandan universities/research units:** potential independent evaluation, student projects, domain review and reproducibility work; choose based on relevant expertise and approved research ethics.
- **Local ICT professional communities and standards bodies:** peer review, architecture critique, skills development and interoperability discussion.
- **OWASP GenAI Security Project:** public threat taxonomies and testing resources; community material is not a substitute for a bespoke security review.
- **NIST / NCCoE publications:** reference material for AI risk and agent identity; do not imply a commercial partnership or formal conformity.
- **OpenTelemetry community:** instrumentation conventions and ecosystem documentation, not a claim of certification.
- **GitHub engineering/security ecosystem:** upstream docs, issues, release notes and responsible issue reporting; use official release artifacts and source commits.

### Enterprise users and delivery ecosystem
- **SMEs, manufacturers, distributors and retailers:** candidate design partners for procurement, stock, supplier and workflow pilots.
- **ERP implementers / Odoo service providers:** integration mapping, sandbox access, migration support and operator training.
- **Cloud/security service providers:** compare managed identity, logging, sandboxing, backup and incident response only after a data residency and cost review.
- **Civil society, business associations and service organizations:** candidate user validation for accessible, explainable and practical dashboards.

## 4. Partner qualification scorecard

Score each dimension 0–3 with evidence and reviewer; do not sum into an automatic selection if a hard gate fails.

1. Strategic fit: stated use case and decision owner.
2. Evidence access: legal/contractual basis, freshness, provenance, export rights.
3. Mutual value: benefits to both parties articulated.
4. Technical fit: APIs/formats, reliability, documentation and support.
5. Security/privacy: access model, retention, data residency, incident reporting and exit.
6. Interoperability: versioned contracts, units, identifiers, rate limits and error handling.
7. Sustainability: maintenance owner, total cost, staffing and supplier concentration.
8. Evaluation: baseline, pilot design, outcome metric and independent review.
9. Independence/conflicts: funding, incentives, vendor lock-in and alternatives.
10. Exit/reversibility: exportability, deletion, credential revocation and transition plan.

**Hard-stop cases:** no legal authority to use data; unwillingness to clarify ownership; unknown source provenance for critical metrics; no safe test environment for writes; excessive access requirements; or no recovery/exit path.

## 5. Nontechnical operating model

| Role | Responsibility | Minimum output |
|---|---|---|
| Portfolio sponsor | Approves strategic scope, risk appetite and priority conflicts | Portfolio decision log |
| Product / service owner | Defines users, outcome, exclusions and acceptance | Product brief, baseline, success metric |
| Domain owner | Validates business meaning, thresholds and process fit | Domain rules and sign-off |
| Data/source steward | Owns provenance, freshness and permission | Source register and quality report |
| Security / identity owner | Owns threat model, access and incident response | Authorization and negative-test evidence |
| Operations owner | Maintains budgets, alerts, restoration and runbooks | On-call/escalation and recovery proof |
| Independent reviewer | Challenges evidence, tests assumptions and checks risk | Signed review with unresolved findings |
| Partner lead | Manages interviews, agreements and benefits | Partner register and due-diligence pack |
| Training/change lead | Supports adoption, SOPs and feedback | Practical learning assessment and usage feedback |

A person may fill multiple roles in a small pilot, but the independent reviewer must not self-approve the work they authored or operate. Critical/high-impact approval needs separation appropriate to risk.

## 6. Partnership discovery protocol

1. Write a one-page problem brief and the specific decision the partnership will improve.
2. Identify public evidence and alternatives before asking for non-public data.
3. Prepare a 30–45 minute discovery agenda, data questions, and a clear no-obligation pilot concept. This is a proposed meeting format, not a booked event.
4. Obtain permission for notes, data use, sharing, retention, and attribution.
5. Agree the smallest reversible pilot, owners, baseline, measures, review date and exit.
6. Do not call the relationship a partnership until both sides confirm a documented agreement.
7. Publish results only within approved permissions and with limitations disclosed.

## 7. First pilot candidates

**Candidate A — Official-source Market X brief:** public data only; source freshness, change detection, confidence and one-picture executive report. Low external-action risk.

**Candidate B — Odoo purchasing/inventory read-only insight:** synthetic or approved export first; map item, supplier, lead time, available/usable stock, confirmed incoming, demand and expiry; compare the proposed replenishment method to a historical baseline.

**Candidate C — QZ/ASSD quality and safety lab:** synthetic agent identity/delegation and prompt-injection cases, deterministic allow/deny decisions, audit, idempotency and rollback in isolated test fixtures.

**Candidate D — Skills/reproducibility collaboration:** a university or technical community reviews a public, non-sensitive benchmark and reproduces conclusions. No live credentials or production data required.

## 8. Success and stop conditions

Continue only when evidence demonstrates at least one valued improvement without violating a hard safety/privacy/security condition. Pause if data access is uncertain, quality degrades, owners disengage, cost exceeds an approved budget, the baseline cannot be reproduced or exit cannot be executed.
