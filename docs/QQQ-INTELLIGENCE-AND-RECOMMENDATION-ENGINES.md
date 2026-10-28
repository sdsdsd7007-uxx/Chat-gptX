# QQQ Intelligence Engine + Recommendation Engine — Operating Contract
**Version:** v1.0 proposal for QQQ v53.2  
**Date:** 2026-10-28  
**Status:** documented operating contract; no live orchestration implied

## 1. Separation of responsibilities

### QQQ-Intelligence Engine
Owns the evidence process: scope, source intake, validation, analysis, synthesis, risk/uncertainty, and the report. It must answer: **What do we know, how do we know it, what is uncertain, and what changed?**

### QQQ-Recommendation Engine
Owns decision support: alternatives, trade-offs, priority, feasibility, risk treatment, proposed next actions, owners, acceptance criteria and rollback. It must answer: **Given the evidence and the user's goal, what should we do next, why, and how will we verify it?**

The Recommendation Engine may challenge a recommendation, but it may not fabricate or silently alter the underlying findings. The Intelligence Engine may report a risk, but it may not self-authorize an action.

## 2. Required I/O contracts

### Intelligence Report
- run_id, cycle_id, task_id, creation timestamp, target scope;
- sources: identifiers/URLs, publisher/author, publication date, retrieval date, version;
- verified findings and evidence references;
- interpretations, hypotheses and counter-explanations;
- confidence basis, freshness and unresolved data gaps;
- risks, affected parties, limitations and prohibited inferences;
- status per phase: PASS / PARTIAL / UNKNOWN / BLOCKED;
- recommended areas for further investigation (not an execution authorization).

### Recommendation Set
- linked report_id and finding IDs;
- ordered options and rationale;
- strategic alignment and expected value;
- evidence strength, assumptions and uncertainty;
- impact/effort/cost/time-horizon estimates with basis;
- risks and mitigations, owner/reviewer roles and dependencies;
- acceptance criteria, monitoring signals, stop conditions and rollback;
- gate result: RECOMMEND / NEEDS-EVIDENCE / HUMAN-APPROVAL / HOLD.

Never use a numeric confidence score unless its meaning and calibration have been defined. Unknown is a valid outcome.

## 3. Phase result rules
- **PASS:** output exists and acceptance criteria are met with evidence.
- **PARTIAL:** some criteria met; outstanding evidence is named.
- **UNKNOWN:** the state cannot be verified from available sources.
- **BLOCKED:** a required source, permission, safety condition or dependency prevents proceeding.
- **HOLD:** the release/action gate is intentionally closed.

Missing data cannot be treated as a PASS. A high score cannot average away a critical safety, privacy, legal or authorization failure.

## 4. Cycle manager state machine
`IDLE → RECEIVED → SCOPED → INGESTING → VALIDATING → ANALYZING → REPORT_READY → RECOMMENDATIONS_READY → GATE_PENDING → APPROVED_EXECUTION or DEFERRED → VERIFYING → LEARNING → NEXT_CYCLE or CLOSED`

Each transition has a timestamp and evidence reference. Use bounded retries, deadlines, cancellation, idempotency keys and explicit failure states. Parallel processing must be capped per resource and task class; steps sharing mutable state must be serialized or protected by concurrency controls.

## 5. Learning and self-adaptation controls
1. Keep immutable evidence snapshots or versioned references for every cycle.
2. Record outcome measurements against a stated baseline.
3. Generate a versioned proposal—not a live rewrite—when evidence suggests an improvement.
4. Run regression, security, data-integrity and cost/latency tests.
5. Have an independent reviewer assess the proposal and risks.
6. Promote only through a separate authorized staging/release process.
7. Preserve a rollback path and an audit record.

The engine cannot alter its own permission rules, release gates or review requirements. Do not automatically inject book summaries or historical interpretations into production decision logic without a tested, approved translation and evaluation.

## 6. Recommendation scoring (proposed rubric)
For decisions where a weighted comparison is suitable:
- value/impact: 30%;
- evidence strength: 25%;
- feasibility and effort: 15%;
- risk/reversibility: 15%;
- strategic alignment: 10%;
- learning value: 5%.

For each option, show the component assessments and their evidence. Keep hard constraints as pass/fail gates before scoring. If values are not measurable, use reasoned qualitative ratings rather than fake precision.

## 7. Example cycle for QQQ study work
**Goal:** build reliable learning notes and decision tools from *التفكير الاستراتيجي* and related leadership material.

- Intelligence phase: check official source and edition, map contents, extract concepts using page references, record what is not yet checked, and summarize the distinction between strategic thinking and planning.
- Report phase: state findings, source locations, uncertainty and what remains to read.
- Recommendation phase: prioritize exact-edition verification and chapter-by-chapter notes before creating new automation or claiming a system integration.
- Gate: review citations and copyright boundaries; no cloud sync without an authorized connector.
- Verify: check notes against the source and record reviewer feedback.
- Next cycle: reconcile the series bibliography, then study the next confirmed work.

This is a workflow example, not evidence of a live engine or full-book completion.

## 8. Operational performance measures
Define and measure, rather than assume:
- source coverage / provenance completeness;
- stale source and unresolved contradiction rate;
- report acceptance rate by independent reviewer;
- recommendation acceptance and reversal rate;
- cycle completion time and p50/p95/p99 where runtime telemetry exists;
- percentage of changes with regression tests and rollback;
- effort/resource use per accepted deliverable;
- number of unauthorized actions (required target: zero in defined tests).

Do not claim zero latency, 100% accuracy, 0% waste or 100-microsecond end-to-end study cycles without clear methods and measured evidence.

## 9. Definition of DONE
The intelligence report is complete when every major claim has traceable source support or is labeled as interpretation/unknown. Recommendations are complete when alternatives and risks are compared, a justified next action is identified, and acceptance/rollback conditions are defined. The cycle may then repeat within its approved scope—or close explicitly if no next step is supported.

**Current status: OPERATING CONTRACT DOCUMENTED / LIVE ENGINE NOT VERIFIED / PRODUCTION HOLD.**
