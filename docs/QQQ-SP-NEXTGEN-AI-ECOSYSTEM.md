# QQQ-SP — Next-Generation AI Ecosystem
**Framework:** QQQ v53.0 design baseline  
**Review date:** 2026-10-28  
**Status:** proposed sub-project family; production HOLD  
**Parent:** QQQ-Core, coordinated through QQQ-SP1 Integration Vanguard and QQQ-SP2 learning/meta-improvement concepts

## Executive purpose
Create four clearly bounded sub-projects for studying and integrating major AI platforms, permitted web knowledge sources, and next-generation AI research. An evaluation unit compares candidates through reproducible tasks rather than unverified claims or product hype.

These are **project charters and an evaluation plan**, not evidence that connectors are installed, platforms are linked, all websites are indexed, or any autonomous agent is online.

## Sub-project registry

| ID | Name | Mandate | First deliverable | Default permissions |
|---|---|---|---|---|
| QQQ-SP-Gemini | Gemini Platform Intelligence | Track Google's Gemini API/app capabilities, model/version changes, pricing, modality/tool support and safe integration patterns | Dated model/source register and adapter acceptance contract | Public docs read-only; API access only after owner approval |
| QQQ-SP-ChatGPT | ChatGPT / OpenAI Platform Intelligence | Track ChatGPT product surfaces, OpenAI API models, tool and connector capabilities, availability, policy and release changes | Dated capability register separating ChatGPT app from API | Public docs read-only; API access only after owner approval |
| QQQ-SP-WebVerse | Governed Web Knowledge Fabric | Discover and index selected public/permitted web sources with provenance, freshness, rights and crawler controls | Source registry, crawl policy, robots/terms handling, provenance and deduplication design | Allowlisted read-only sources; no authentication bypass or unrestricted crawling |
| QQQ-SP-NextGenAI | Frontier & Emerging AI Observatory | Evaluate emerging model families, open-weight/local models, multimodal systems, agents, retrieval, privacy techniques and compute trends | Horizon-scan register and evidence-backed experiment queue | Research only; no automatic model promotion |
| QQQ-AI-EvalLab | Cross-Platform Evaluation Unit | Compare systems on the same tasks, constraints and scoring rubric | Reproducible test pack, scorecard and limitations report | Sandboxed evaluations; human review required |

The four SP projects are the requested scope. QQQ-AI-EvalLab is a shared test unit so their results can be compared fairly.

## Current public-source snapshot (2026-10-28)
This is a dated snapshot from vendor documentation, not an independent benchmark:
- Google documents Gemini 4 Argon as its latest most capable model, with a unified 1M-token context, long decode up to 1M tokens, multimodal input including text, image, video, audio and PDF, and capabilities including function calling, search grounding, URL context and computer-use preview. Availability and exact features depend on the specific model and endpoint.
- OpenAI announced GPT-6.1 Terra on 2026-10-26 for ChatGPT Work/Codex and the API, emphasizing visual reasoning, computer use and writing. OpenAI’s release notes say Terra is in Work and Codex rather than the Chat tab. Public statements and prices are provider-published and should be labelled as such.
- The ChatGPT consumer/work product and OpenAI API are different product surfaces; likewise, Gemini consumer experiences and the Gemini API are not interchangeable. Always record exact product, model ID, endpoint, plan, region, settings and evaluation date.
- No overall winner is declared here. A valid comparative claim needs the same evaluation set, tool permissions, time budget, sample size and independent scoring.

Official sources:
1. Gemini latest model page: https://ai.google.dev/gemini-api/docs/latest-model?hl=en
2. Gemini model directory: https://ai.google.dev/gemini-api/docs/models.md
3. Gemini API changelog: https://ai.google.dev/gemini-api/docs/changelog
4. OpenAI GPT-6.1 Terra announcement: https://openai.com/index/introducing-gpt-6-1-terra/
5. OpenAI model release notes: https://help.openai.com/en/articles/9624314-model-release-notes
6. ChatGPT release notes: https://help.openai.com/en/articles/6825453-chatgpt-release-notes

## Operating architecture

`SOURCES → PROVENANCE & RIGHTS → NORMALIZE → TASK ROUTER → APPROVED PLATFORM ADAPTERS → EVAL LAB → HUMAN REVIEW → VERSIONED FINDINGS → QQQ KNOWLEDGE REGISTER`

Cross-cutting controls:
- Source timestamp, retrieved timestamp, model/version, endpoint, environment and evidence reference.
- Data minimization, retention rules, redaction, and clear separation of public facts, vendor claims, independent findings, hypotheses and unknowns.
- Per-tool authorization, least privilege, secrets stored outside source code, bounded quotas and retries.
- Prompt-injection defense: fetched web pages and files are untrusted data, not policy instructions.
- No autonomous production change, procurement commitment, permission change or model promotion from evaluation results alone.
- Rollback, incident escalation, human review and audit history for material changes.

## Cross-platform evaluation rubric (proposed weights)
Weights are initial design choices and must be agreed before scoring. Do not fill numeric scores until tests are run.

| Dimension | Weight | Measurement idea |
|---|---:|---|
| Task correctness and completeness | 25% | Blind rubric against known-answer or expert-reviewed tasks |
| Reliability and repeatability | 15% | Success rate over repeated runs; variance and failure classes |
| Safety and instruction-boundary behavior | 15% | Prompt-injection, refusal, data-boundary and tool-authorization tests |
| Multimodal and structured-input quality | 10% | Separate image, audio, video, PDF and structured extraction tasks |
| Latency and throughput | 10% | p50/p95/p99 under the same load and region |
| Total cost per accepted task | 10% | Input/output tokens, tool costs and retry/verification costs |
| Privacy, retention and governance fit | 10% | Settings, retention, admin control, residency, access and audit evidence |
| Interoperability / maintainability | 5% | Adapter quality, schema stability, versioning and migration burden |
| **Total** | **100%** | Scores reported with sample size, confidence limits and caveats |

Scoring rule: retain per-task results; do not let a weighted average hide a critical security or data-quality failure. A critical gate failure means HOLD regardless of total score.

## Initial benchmark pack
1. Evidence-backed web research with citation verification.
2. Long-document synthesis with contradiction detection and pinpoint references.
3. Arabic/English reasoning, translation and clear communication.
4. Image/PDF/audio/video extraction with uncertainty marking.
5. Code analysis and bounded repository change in a sandbox.
6. Structured extraction to JSON/CSV with strict schema adherence.
7. Business operations case: procurement, inventory or vendor analysis using synthetic data.
8. Scenario analysis with assumptions, probabilities and uncertainty stated.
9. Prompt-injection and untrusted-document tests; no unauthorized tool invocation.
10. Cost/latency/reliability stress test with bounded concurrency and retry budget.
11. Knowledge freshness: detect changed or withdrawn official model documentation.
12. Privacy test: avoid emitting secrets or unnecessary personal data from synthetic fixtures.

For each task: use identical prompt intent, input, allowed tools, output schema, time cap and evaluation rules. Use at least several repeated trials, blind scoring where practical, deterministic checks for structure, human review for quality, and published test-set versions. Model-specific options can be tested separately but must be declared.

## WebVerse access and rights policy
“Every website” is not a feasible or safe blanket crawl scope. WebVerse must use an allowlist or justified priority set; respect site terms, licensing and applicable law; follow robots.txt directives as crawler policy; use published APIs where appropriate; obey rate limits; identify the crawler; cache responsibly; provide source attribution; and stop on access-control or privacy boundaries. Robots.txt is not itself authorization to access protected data. No login bypass, CAPTCHA bypass, paywall circumvention, personal-data harvesting or unrestricted high-rate scanning.

## Release gates
- G1: scope, source list, owner, data classification and retention approved.
- G2: adapter and source-provenance tests pass in local/sandbox environment.
- G3: security, prompt-injection, rights, privacy and rate-limit tests pass.
- G4: cross-platform test pack and evaluation protocol are versioned and repeatable.
- G5: independent reviewer checks source citations, metrics and limits.
- G6: any live API or staging access separately approved with bounded permissions and cost controls.
- G7: production use requires explicit authorized sign-off, monitoring and rollback.

## Definition of DONE
A sub-project is DONE only when its versioned deliverables, reproducible tests, evidence sources, owner/reviewer, open risks and rollback/stop conditions are recorded. A document, prototype or scheduled review alone does not establish a live connection.

**Current state:** design and research baseline established; provider adapters, real-world benchmark scores, broad web indexing and production connections remain **NOT VERIFIED**.