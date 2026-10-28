# Project Z Benchmark Protocol

**Status:** proposed evaluation protocol  
**Data:** synthetic-only until a separately reviewed public or authorized dataset is selected  
**Purpose:** prevent overclaiming from tiny CI smoke tests.

## Current verified smoke-test scope

The verified workflow run executes 500 fabricated events over 5 iterations, validates ingestion and lexical retrieval, and reports median / p95 for ingestion, search and their combined pipeline. The recorded combined p95 of 4.696 ms is a single small GitHub-hosted-runner observation. It is not a production SLO, stable baseline, or representative workload result.

## Required protocol before comparing retrieval designs

### 1. Freeze the evaluation set
- Version the corpus, query set, relevance judgments and generator script.
- Record provenance, licensing, creation date, language and known coverage gaps.
- Keep a held-out test set separate from tuning queries.
- Have relevance labels reviewed independently; record adjudication and disagreements.
- Do not manufacture additional relevance labels merely to increase sample count.

### 2. Stratify workload
Include, where applicable:
- common and rare metric names;
- multi-token and partial-match queries;
- identifiers, punctuation, underscores and hyphens;
- time-window and service-context queries;
- empty, malformed, ambiguous and out-of-scope queries;
- multilingual and domain-specific queries only when the product requires them.

Report each slice separately. Aggregate averages can hide weak slices.

### 3. Compare candidates fairly
- A: deterministic lexical baseline (current).
- B: dense/vector retrieval, only after a suitable labelled corpus and privacy review exist.
- C: hybrid lexical + dense retrieval, with fusion parameters tuned only on validation data.
- Optional reranking is a separate stage and must be measured separately.

Keep corpus snapshot, preprocessing, top-k, hardware, software versions, cache state and query set fixed across candidates.

### 4. Quality measures
Report precision@k, recall@k, MRR, nDCG@k, zero-result rate and duplicate-result rate. Explain relevance-label policy and metric aggregation. Add human-reviewed task success and evidence correctness before any user-facing answer-generation claims.

### 5. Performance measures
- Warm-up runs separated from measured runs.
- At least 30 measured repetitions for a preliminary local microbenchmark; more for stable tail estimates.
- Report sample count, median, p90, p95 and p99 where sample size supports them.
- Use a pinned, described runtime/hardware baseline and representative concurrency.
- Separate ingestion, indexing, candidate retrieval, reranking and end-to-end latency.
- Include memory and compute/cost where relevant.
- Use paired query-level comparisons and confidence intervals for quality differences.

### 6. Safety and access-control tests
- Synthetic fixtures by default; no secrets, customer data or personal records.
- Verify authorization filters before retrieval results are exposed.
- Test malformed inputs, oversized payloads, duplicate IDs, stale records and partial failures.
- A confirmed access-control leak is a stop-ship issue, not an ordinary quality regression.

## Promotion gates

Do not select a vector database or declare the 150 ms p95 objective met until:
1. the labelled set is sufficiently representative and independently reviewed;
2. lexical, dense and hybrid candidates are compared under the same conditions;
3. confidence intervals and per-slice results are reported;
4. privacy, licensing, access control and retention are reviewed;
5. operational cost and recovery behavior are documented.

## Research basis

- NIST AI RMF: Govern, Map, Measure, Manage; measurement should document uncertainty and support independent review. https://www.nist.gov/itl/ai-risk-management-framework
- Thomas et al. (SIGIR 2026), *Evaluation Validity in Information Retrieval*: evaluation metrics are abstractions and should be checked for validity against intended user outcomes. https://www.microsoft.com/en-us/research/publication/evaluation-validity-in-information-retrieval/
- Soboroff (NIST, 2014), *Computing confidence intervals for common IR measures*. https://www.nist.gov/publications/computing-confidence-intervals-common-ir-measures
- IBM Research / ACL 2023, *Moving Beyond Downstream Task Accuracy for Information Retrieval Benchmarking*: include latency and hardware/cost conditions alongside quality. https://research.ibm.com/publications/moving-beyond-downstream-task-accuracy-for-information-retrieval-benchmarking

This protocol is a proposed gate, not a claim that the full evaluation has been performed.
