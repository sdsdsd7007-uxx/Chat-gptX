"""Offline retrieval quality metrics for a tiny, explicitly synthetic labelled set."""
from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence

from project_z.telemetry import TelemetryEvent, search_events


def evaluate_queries(
    events: Iterable[TelemetryEvent],
    queries: Sequence[Mapping[str, object]],
    *,
    k: int = 5,
) -> dict[str, float | int]:
    """Compute macro precision@k, recall@k, MRR and nDCG@k against synthetic qrels."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    corpus = tuple(events)
    if not queries:
        raise ValueError("at least one labelled query is required")
    precision_values: list[float] = []
    recall_values: list[float] = []
    reciprocal_ranks: list[float] = []
    ndcgs: list[float] = []
    for item in queries:
        query = item.get("query")
        relevant = item.get("relevant_event_ids")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("each query must be a non-empty string")
        if not isinstance(relevant, list) or not relevant or any(not isinstance(x, str) for x in relevant):
            raise ValueError("relevant_event_ids must be a non-empty list of strings")
        relevant_set = set(relevant)
        ranked = search_events(corpus, query, limit=max(k, len(corpus)))
        ranked_ids = [event.event_id for event in ranked]
        top_ids = ranked_ids[:k]
        hits = sum(event_id in relevant_set for event_id in top_ids)
        precision_values.append(hits / k)
        recall_values.append(hits / len(relevant_set))
        rank = next((i + 1 for i, event_id in enumerate(ranked_ids) if event_id in relevant_set), None)
        reciprocal_ranks.append(1.0 / rank if rank else 0.0)
        dcg = sum((1.0 / math.log2(i + 2)) for i, event_id in enumerate(top_ids) if event_id in relevant_set)
        ideal_hits = min(k, len(relevant_set))
        idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
        ndcgs.append(dcg / idcg if idcg else 0.0)
    mean = lambda values: sum(values) / len(values)
    return {
        "query_count": len(queries),
        f"precision_at_{k}": round(mean(precision_values), 6),
        f"recall_at_{k}": round(mean(recall_values), 6),
        "mrr": round(mean(reciprocal_ranks), 6),
        f"ndcg_at_{k}": round(mean(ndcgs), 6),
    }
