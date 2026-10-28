# QQQ-SP-AI-EvalLab — Cross-Platform Comparative Analysis
**As-of date:** 2026-10-28  
**Status:** evidence-backed capability snapshot + proposed common evaluation; numeric head-to-head scores NOT YET MEASURED.

## Executive finding
Gemini, ChatGPT/OpenAI API, WebVerse, and NextGenAI are not four interchangeable models:
- Gemini and OpenAI expose model/API families plus user-facing products.
- ChatGPT is a product surface as well as an ecosystem of tools and integrations; GPT-6.1 Terra is not available in every ChatGPT surface.
- WebVerse is a governed data-acquisition and retrieval system, not a generative model.
- NextGenAI is a research portfolio, not one product to rank.

Therefore the appropriate design is a **best-fit router plus a common independent evaluation harness**, not a claim that one provider wins every dimension.

## Publicly documented capability snapshot
| System | What official source supports today | Key limits for this comparison |
|---|---|---|
| Gemini 4 Argon API | Google documents a 1M-token unified context, long decode up to 1M tokens, inputs including text/image/video/audio/PDF, and tools such as function calling, search grounding, URL context, code execution and computer-use preview | Exact feature support and limits are model/endpoint specific; model docs are vendor-published, not a neutral comparative benchmark |
| GPT-6.1 Terra / OpenAI | OpenAI announced visual reasoning, computer use and writing; model release notes say Work/Codex and API availability. Announcement listed $1/M input, $0.05/M cached input and $5/M output at release | Product availability differs by ChatGPT surface and rollout; compare with same API/tool conditions, not marketing claims |
| ChatGPT product | Release notes include product-level interactive and work/collaboration capabilities that can differ by plan, surface and rollout | A ChatGPT subscription is not equivalent to API pricing or an API endpoint |
| WebVerse | Proposed source registry, fetch/API layer, provenance and search index | Not implemented as a live crawler here; permitted-source coverage and freshness are unknown |
| NextGenAI Observatory | Proposed horizon scanning and controlled experiments | Not a single model, endpoint or capability score; candidate-by-candidate evidence is required |

Primary sources:
- Gemini 4 Argon model guide: https://ai.google.dev/gemini-api/docs/latest-model?hl=en
- Gemini model directory: https://ai.google.dev/gemini-api/docs/models.md
- Gemini release notes: https://ai.google.dev/gemini-api/docs/changelog
- OpenAI GPT-6.1 Terra announcement: https://openai.com/index/introducing-gpt-6-1-terra/
- OpenAI model release notes: https://help.openai.com/en/articles/9624314-model-release-notes
- ChatGPT release notes: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- OWASP GenAI LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- Robots Exclusion Protocol: https://www.rfc-editor.org/rfc/rfc9309.html

## Comparison implications
1. **Long-context work:** Gemini 4 Argon has documented 1M context and long decode; validate retrieval accuracy as the context grows. Do not assume larger context guarantees better reasoning.
2. **Computer-use workflows:** both ecosystems document computer-use capabilities, but exact surface, region, tool permissions and availability differ. Test in an isolated sandbox and record exact endpoint/model.
3. **Multimodal:** compare individual input types separately. A model's ability to accept audio/video/PDF does not guarantee accurate extraction or safe action.
4. **Research and web grounding:** test whether citations support the claims, distinguish current from stale information, and preserve source provenance. Search availability alone is not citation correctness.
5. **Cost:** compare total cost per accepted task, not just token price. Include cached input, output, grounding/search, tool calls, retries, human review and failure recovery.
6. **Security:** a high-quality answer cannot compensate for an unauthorized tool call, secret exposure or disallowed source access. Critical failures trigger HOLD irrespective of an aggregate score.
7. **Next generation:** require an experiment and evidence rather than an assumption about AGI, quantum advantage or "autonomous everything."

## Reproducible test protocol
- Freeze task set, rubric version, model IDs, API/product surface, parameters, region, tools and allowed data class.
- Use the same inputs, time budget and tool permissions wherever technically comparable; document necessary differences.
- Run multiple trials per task and retain failed outputs, tool traces, source IDs and costs.
- Use deterministic checks for structured output and known facts, source-link verification for citations, and blinded human evaluation for qualitative tasks.
- Include a controlled prompt-injection set, data-boundary cases and unauthorized-tool tests with synthetic fixtures.
- Report n, pass rate, confidence interval where appropriate, p50/p95/p99 latency, total cost per accepted task, error categories and limitations.
- Repeat after a model release/deprecation or material endpoint change.

## Initial weighted rubric (proposal, not measured score)
| Dimension | Weight |
|---|---:|
| Task correctness and completeness | 25% |
| Reliability and repeatability | 15% |
| Safety and instruction-boundary behavior | 15% |
| Multimodal and structured-input quality | 10% |
| Latency/throughput | 10% |
| Total cost per accepted task | 10% |
| Privacy, retention and governance fit | 10% |
| Interoperability and maintainability | 5% |
| **Total** | **100%** |

Do not calculate aggregate scores until a pilot run exists. A critical safety, privacy or authorization failure is a hard gate and cannot be averaged away.

## Decision model
Use a best-fit router:
- Route large-document and multimodal candidate tasks to the model that proves best on the matching EvalLab tasks.
- Route computer-use work only to a sandboxed model/tool path with a narrow allowlist and human approval for material actions.
- Route factual research through WebVerse or approved search with citations and freshness checks.
- Route sensitive data only after a documented data-classification and retention review.
- Route unknown/novel model proposals to NextGenAI research and offline evaluation, never direct production.

## Current ratings
**No winner and no numeric scores assigned.** Public documentation is sufficient to describe supported features, but not to assert an independent head-to-head result. Current QQQ connection status and WebVerse production coverage remain UNKNOWN.

## Definition of DONE
Evaluation report records versioned tests, exact provider/model/product surface, data and sample size, scoring methodology, costs/latencies, source validation, failures, safety findings, owner, independent reviewer and next review date.