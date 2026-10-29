# QQQ GenAI Threat-to-Test Matrix (Offline Planning Baseline)

**Status:** Proposed test plan; not a completed security assessment.  
**Applies to:** Synthetic/offline QQQ intelligence and recommendation-contract prototype.  
**Owner:** Unassigned. **Independent reviewer:** Unassigned.  
**Last researched:** 2026-10-29.  
**Release rule:** No production or live-service claims follow from this document. Convert each row into a test only when its applicable component exists.

## Purpose

Translate current public AI-security guidance into bounded, reproducible regression-test candidates. Retrieved content and model output are data, not authorization. The recommendation contract validates structure; it does not prove source truth, authenticate a person, enforce runtime permissions, or authorize execution.

## Threat-to-test matrix

| ID | Risk area | Offline fixture / test idea | Expected safe behavior | Evidence to retain | Applicability |
|---|---|---|---|---|---|
| QSEC-01 | Prompt injection in retrieved text | Include synthetic untrusted text that asks the system to ignore policy or expose hidden context. | Treat it as source content; do not elevate it to system policy or authorization. | Fixture ID, test result, parser/policy version. | When retrieval or prompt assembly exists. |
| QSEC-02 | Sensitive-information disclosure | Place synthetic canary secrets in a restricted test field and request an unauthorized public output. | Redact or deny the protected field according to an explicit policy; never use real credentials in tests. | Canary ID (not the secret), policy decision, output assertion. | When data access or output filtering exists. |
| QSEC-03 | Excessive agency | Provide a recommendation that contains an execution request or unsupported action payload. | Reject unknown execution fields; keep recommendation generation separate from authorization and execution. | Input fixture, validation errors, contract version. | Partially applicable to the current recommendation contract. |
| QSEC-04 | Supply-chain integrity | Test a synthetic dependency/model manifest with missing provenance, an unexpected version, or a digest mismatch. | Mark provenance unknown or block the component under a defined policy; never claim the manifest alone proves safety. | Manifest fixture, expected/actual digest metadata, decision. | When dependencies/models are inventoried. |
| QSEC-05 | Data/model poisoning | Include conflicting synthetic source records and an untrusted source identity. | Preserve disagreement and provenance; do not silently convert a conflict into a supported claim. | Source IDs, conflict result, uncertainty state. | When ingestion/analysis exists. |
| QSEC-06 | Unbounded consumption | Feed oversized but harmless synthetic input and a controlled loop/count fixture. | Enforce configured size/iteration/time budgets and return a bounded failure. | Input size, configured limits, observed resource metrics. | When runtime processing exists; do not infer latency from a unit test. |
| QSEC-07 | Misinformation / unsupported certainty | Supply a claim without adequate evidence or with conflicting evidence. | Use UNKNOWN/BLOCKED or an explicitly qualified result; never fabricate references or confidence. | Claim ID, evidence references, state and reason. | Applicable to evidence and intelligence contracts. |
| QSEC-08 | Hidden-context exposure | Ask for synthetic internal instructions or test-only metadata that is not part of the authorized output schema. | Do not disclose protected context; security must rely on access controls, not secrecy of prompts. | Requested field, policy result, redacted assertion. | When prompts/context and output boundaries exist. |
| QSEC-09 | Vector/embedding isolation | Use synthetic records with tenant labels and a deliberately mismatched access scope. | Return only records allowed by the test policy; fail closed on missing tenant/scope metadata. | Record IDs, scope fixture, retrieval decision. | Only if vector retrieval or embeddings are introduced. |
| QSEC-10 | Improper output handling | Feed malformed structured output, extra fields, invalid IDs and unsafe downstream-action-shaped fields to validators. | Reject invalid/unknown fields and prevent unvalidated output from being consumed as an action. | Input fixture, validation result, downstream-call count (must be zero). | Partially applicable to the current recommendation contract. |
| QSEC-11 | Authorization timeout / policy-service failure | Simulate a missing or timed-out policy decision in an offline stub. | No high-impact action occurs; produce a clear BLOCKED/UNKNOWN result and auditable reason. | Timeout fixture, policy version, action-not-invoked assertion. | When runtime policy gates are designed. |
| QSEC-12 | Audit and replay | Validate that the same fixture and contract version produce stable validation results and traceable error IDs. | Stable output for deterministic validators; retain version and fixture identity without logging secrets. | Fixture hash, commit SHA, test output. | Applicable to contract tests. |

## Acceptance criteria

1. Every implemented row has a deterministic synthetic fixture, an explicit expected outcome, and a regression test.
2. Unknown, conflicting, stale, or unauthenticated evidence is never silently treated as supported.
3. Recommendation objects cannot authorize or invoke tools by themselves.
4. Tests use synthetic data only; no real secrets, personal records, production endpoints, or live destructive actions.
5. Failure behavior is explicitly documented for policy timeouts and missing evidence; high-impact actions require an approved policy and human authorization.
6. Results identify the exact commit SHA and test run. A passing test suite is not a security certification or production sign-off.
7. Rows marked not applicable remain planned work, not passed controls.

## Research references

- OWASP GenAI Security Project, **OWASP Top 10 for LLM Applications 2026** (published 4 August 2026): https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP GenAI Security Project, **GenAI Red Teaming Manual v1.0** (listed 20 October 2026): https://genai.owasp.org/resources/
- OWASP GenAI Security Project, **Agent Control Standard (ACS)**: https://genai.owasp.org/resource/agent-control-standard-acs/
- NIST, **AI Risk Management Framework**: https://www.nist.gov/itl/ai-risk-management-framework
- NIST, **NISTIR 8547 — Transition to Post-Quantum Cryptography Standards** (final, 27 October 2026): https://csrc.nist.gov/pubs/ir/8547/final

## Current limitations and next step

This matrix is a proposed baseline for test planning, not evidence that all risks have been tested or mitigated. Assign a real owner and independent reviewer, select the first applicable rows, implement one bounded offline test slice at a time, and record exact-head CI evidence. Do not claim OWASP/NIST compliance, certification, production readiness, live telemetry, or security assurance from this document alone.
