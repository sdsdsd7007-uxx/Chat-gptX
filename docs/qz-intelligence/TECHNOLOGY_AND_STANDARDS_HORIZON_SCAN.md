# Technology & Standards Horizon Scan — 2026-10-29
**Document ID:** QZ-RESEARCH-004  
**Status:** Research register / recommendations; verify releases before adoption  
**Scope:** Fresh ideas that could materially improve QZ/ASSD, QQQ, StudyCore and Market X.

## 1. New developments to evaluate

### A. GitHub Agentic Workflows — general availability announced 2026-10-28
**Potential fit:** repository issue triage, CI failure classification, report/doc updates and test suggestions.  
**Recommended first use:** read-only reporting in an isolated branch; any proposed write becomes a reviewed pull request. Keep normal CI, branch permissions and human review as independent controls.  
**Important caution:** the upstream repository page reports that releases from v0.83.3 up to but excluding v0.85.4 were retired after a security vulnerability was discovered. Verify the currently recommended release, source commit, permissions and threat model before evaluation; do not blindly install a version from an old quickstart.  
**Decision:** EXPLORE / SANDBOX ONLY; no activation or integration claimed.  
**Sources:** [GitHub GA announcement](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/), [official gh-aw repository and security note](https://github.com/github/gh-aw).

### B. GitHub Actions dependency lockfiles — GA announced 2026-10-28
**Potential fit:** immutable action dependency resolution and reproducible CI.  
**Observed project status:** PR #1/#2 workflow pins checkout/setup-python to full commit SHAs. PR #4/#5/#7 use v7 tags for checkout/setup-node in inspected workflows.  
**Caveat:** the upstream `gh-actions-lock` project documents that remote reusable workflows called by `jobs.<id>.uses` are not locked by the tool (issue #179); container images and local actions also have separate coverage caveats. The inspected workflows did not show remote reusable workflow calls, so this specific gap is not a confirmed exposure in those files.  
**Decision:** prioritize reviewed full-SHA pins for QZ's step actions or a documented lockfile pilot with an explicit coverage inventory; inspect lockfile diff and callee dependencies; don't mistake "verify passed" for "everything secured."  
**Sources:** [GitHub GA announcement](https://github.blog/changelog/2026-10-28-github-actions-workflow-lockfiles-are-generally-available/), [official extension limits](https://github.com/github/gh-actions-lock), [issue #179](https://github.com/github/gh-actions-lock/issues/179).

### C. NIST agent identity and authorization tenets — published 2026-10-27
**Potential fit:** trusted identity for each agent workload; identity lifecycle distinct from human accounts; delegated scopes attenuated; least privilege; revocation and audit.  
**Decision:** use as design input for GOV-01/GOV-02; define controls based on risk and test them rather than asserting compliance.  
**Source:** [NIST Design Tenets for Agent Identity Management Systems](https://www.nist.gov/blogs/cybersecurity-insights/design-tenets-agent-identity-management-systems).

### D. Australian Signals Directorate / Cyber.gov.au harness guidance — published 2026-09-11
**Potential fit:** treat the model-to-tool/data connection layer as a critical security boundary; emphasize least privilege, monitoring and human oversight of sensitive actions.  
**Decision:** incorporate into architecture and negative tests; start with low-risk cases and expand only after controls mature.  
**Source:** [Agentic AI harnesses](https://www.cyber.gov.au/advisory/agentic-ai-harnesses).

### E. OWASP Top 10 for Agentic Applications 2026 and new Agent Control resources
**Potential fit:** threat-to-test mapping for goal hijack, tool misuse, identity/privilege abuse, untrusted memory/context and excessive agency.  
**Decision:** map each relevant threat to a synthetic fixture, regression test, owner and evidence record. Use OWASP as a community reference and do a project-specific threat model.  
**Sources:** [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [OWASP 2026 Agent Control announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/).

### F. NIST AI RMF and ISO/IEC 42001
**Potential fit:** enterprise accountability, lifecycle risk, defined roles, impact assessment and continual improvement.  
**Decision:** use as governance crosswalk rather than label the project "compliant" or "certified." Confirm applicable national/legal obligations with qualified owners.  
**Sources:** [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [ISO/IEC 42001:2023](https://www.iso.org/standard/42001).

## 2. Emerging product/architecture ideas

1. **Evidence-as-a-product:** source registry, claim graph, freshness check and reproducible exports.
2. **Policy-as-code:** deterministic allow/deny decisions kept separate from model reasoning.
3. **Agent identity broker:** workload identity, scope-limited mandate, expiration/revocation, auditable delegation chain.
4. **Tool and connector inventory:** capabilities, data scopes, owners, side-effect classification, budget and expiry.
5. **Golden task set:** versioned tasks representing the actual intended workload, paired with human-reviewed expected evidence and outputs.
6. **Model router with quality floor:** routing by task fit/quality, data class, latency and approved spend; never route purely by speed.
7. **Evaluation-driven model changes:** compare candidates on the same task pack before promotion.
8. **Safety case packet:** scope, threat model, evidence, evaluation, independent review, residual risk, rollback and owner signature.
9. **Source-backed daily brief:** change detection rather than giant unfiltered summaries; show what changed, why it matters, evidence, confidence and action owner.
10. **Data contracts and semantic versioning:** consistent units, identifiers, definitions and migration rules across Market X, Odoo and country projects.
11. **Time-series observability:** per-step spans, timestamps, p50/p95/p99, errors, budget and source freshness.
12. **Human-centered workflow design:** user interviews, accessibility, change training, manual override and appeal/exception pathways.
13. **Digital resilience:** backup/restore, graceful degradation, supplier diversity, local cache and documented shutdown modes.
14. **Value ledger:** compare expected and observed quality, time, service and cost; only claim value with a reproducible baseline.
15. **Portfolio kill switch:** pause projects that lack an owner, source permission, repeatable value, acceptable risk or viable support path.

## 3. Research maturity rules

- Official sources establish what they actually state; do not inflate vendor claims into independent research.
- Separate current availability, announced capability, preview, roadmap and speculation.
- Record retrieval date, official source, release/version and unresolved question.
- For tools changing weekly, verify current release notes and security advisories at selection time.
- Treat partnerships as prospective unless the counterpart confirms a relationship.
- No recommendation is evidence of deployment; no documentation is proof of operational readiness.
