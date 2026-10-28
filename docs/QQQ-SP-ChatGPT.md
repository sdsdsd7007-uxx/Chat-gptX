# QQQ-SP-ChatGPT — ChatGPT & OpenAI Platform Intelligence
**Parent:** QQQ-SP Next-Generation AI Ecosystem  
**Status:** research / adapter design; no live API integration implied  
**Last source review:** 2026-10-28

## Mission
Track ChatGPT product capabilities separately from the OpenAI API and evaluate appropriate workflows with explicit model IDs, product surfaces, policy controls and evidence.

## Workstreams
1. **Product/API separation:** record whether a capability is in ChatGPT Chat, Work, Codex, mobile, a connector/app, or the API. Never infer that an app feature is exposed identically through the API.
2. **Release and model tracker:** model IDs, availability, plan and region restrictions, release notes, deprecation dates, pricing, context and tool capabilities where documented.
3. **Safe task integration:** typed request/response contracts, bounded tool permissions, schema checks, timeouts, cost limits, approval gates and auditable task IDs.
4. **Capability evaluation:** text reasoning, image/visual interpretation, writing, coding, computer-use tasks in a sandbox, multimodal extraction, structured data and source-backed research.
5. **Governance and reliability:** observe retention/settings, policy and data-protection documentation, version drift, error behavior, prompt injection and tool-authorization boundaries.

## Dated public evidence
OpenAI announced GPT-6.1 Terra on 2026-10-26, describing visual reasoning, computer use and writing. OpenAI model release notes state it is available in ChatGPT Work and Codex and through the API; it is not listed for the Chat tab in those notes. The announcement reports standard API prices of $1 per 1M input tokens, $0.05 per 1M cached input tokens and $5 per 1M output tokens at announcement time. Price and rollout must be rechecked when a job runs; subscription usage and API billing are distinct.

Official sources:
- https://openai.com/index/introducing-gpt-6-1-terra/
- https://help.openai.com/en/articles/9624314-model-release-notes
- https://help.openai.com/en/articles/6825453-chatgpt-release-notes

## First deliverables
- Release register with source date, product surface and availability notes.
- ChatGPT-product vs API feature matrix.
- Minimal adapter prototype using synthetic or non-sensitive inputs.
- EvalLab test results with exact model ID, model settings, tool permissions, date and sample count.
- Change/deprecation and rollback plan.

## KPIs (not yet measured)
- correctness, completeness and repeatability per task class;
- honest limitation reporting and scope adherence;
- computer-use task success in a sandbox, with unauthorized actions blocked;
- output-schema conformance;
- p50/p95/p99 latency and cost per accepted task;
- citation accuracy and source freshness;
- policy, privacy and security test pass rates.

## Guardrails
Vendor benchmark claims must be identified as vendor-reported. An official product feature does not establish universal availability or successful performance for a user's account. Avoid unrestricted access to files, browser, email, finance or production systems. Use least privilege, sandboxing and explicit approval for consequential actions.

## Acceptance criteria
The release register is reproducible from official references; product and API capabilities are correctly separated; the prototype uses scoped permissions; evaluation is repeatable; and an independent reviewer signs off. Live connectivity and production readiness remain UNKNOWN/HOLD until proven separately.