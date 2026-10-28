# QQQ-SP-NextGenAI — Frontier & Emerging AI Observatory
**Parent:** QQQ-SP Next-Generation AI Ecosystem  
**Status:** research and controlled experimentation  
**Last reviewed:** 2026-10-28

## Mission
Identify, study and evaluate next-generation AI capabilities across multimodal systems, agents, retrieval and memory, open-weight/local models, small/on-device inference, privacy-preserving computation, evaluation science and compute infrastructure. Convert verified evidence into testable proposals, not automatic architecture claims.

## Research lanes
- **Frontier model watch:** dated release/source register, model cards, context, modalities, tools, availability, costs and retirement notice.
- **Agent and workflow systems:** task planning, tool permissions, bounded orchestration, human handoff, traceability and long-horizon reliability.
- **Multimodal intelligence:** text/image/audio/video/document tasks, modality-specific evaluation and uncertainty.
- **Open-weight and edge AI:** hardware requirements, latency, licensing, update management, local privacy and quantized performance.
- **Retrieval and memory:** RAG, structured/graph retrieval, data provenance, stale content, cache invalidation and deletion.
- **Evaluation and alignment:** contamination-aware task sets, red-team tests, robustness, calibrated confidence, repeatability and failure analysis.
- **Privacy and security:** least privilege, confidential data handling, sandboxing, prompt injection, supply-chain review, model/data poisoning and bounded consumption.
- **Emerging compute:** quantum and other specialized compute assessed only when a concrete, independently supported use case and feasibility test exist; do not conflate quantum research with current general-purpose AI deployment.

## Operating loop
`SCAN → SOURCE-CHECK → TRIAGE → FORM HYPOTHESIS → DESIGN TEST → RUN SANDBOX EXPERIMENT → INDEPENDENT REVIEW → VERSIONED PROPOSAL → HUMAN APPROVAL → STAGED TRIAL`

No model, policy, code, or build pipeline may rewrite, approve and deploy itself in one unsupervised loop. Keep proposal, evaluation and promotion roles separate.

## Research record
Each finding must include: claim; source and publication date; retrieval date; source class; independent corroboration; uncertainty; affected QQQ units; experiment design; cost/resource envelope; safety/privacy risks; dependency and rollback; owner/reviewer; and next review date.

## Security and governance baselines
Use the NIST AI RMF / Generative AI Profile and current OWASP GenAI LLM Top 10 as risk-management inputs. The OWASP 2026 guide emphasizes risks such as prompt injection, sensitive-information disclosure, excessive agency, supply-chain weaknesses, data/model poisoning and unbounded consumption.

Sources:
- NIST AI RMF Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP GenAI LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP Top 10 for Agentic Applications: https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/

## KPIs (not yet measured)
- research-source corroboration rate;
- time from release discovery to reviewed assessment;
- experiment reproducibility;
- quality gain versus a fixed baseline;
- regression rate and time to rollback;
- cost per useful evaluated finding;
- high-severity issues found before staging;
- percentage of promotions with independent approval and complete evidence.

## Acceptance criteria
A candidate is not labelled “next generation” solely due to marketing. It must have primary-source evidence, a defined use case, a controlled experiment, reproducible results, and risk/maintenance analysis. Keep all production deployment and self-modifying changes behind explicit human authorization.