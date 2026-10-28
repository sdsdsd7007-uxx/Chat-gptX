"""Synthetic-only telemetry ingestion and lexical baseline for Project Z.

No network, persistence, external connectors, or production writes are performed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import math
import re
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9]+")
MAX_BATCH_LINES = 10_000
MAX_LINE_CHARS = 65_536
MAX_TAGS = 64
MAX_FIELD_LENGTHS = {
    "event_id": 256,
    "timestamp": 64,
    "source": 256,
    "metric": 256,
    "unit": 64,
}
MAX_TAG_KEY_LENGTH = 128
MAX_TAG_VALUE_LENGTH = 256


@dataclass(frozen=True)
class TelemetryEvent:
    event_id: str
    timestamp: str
    source: str
    metric: str
    value: float
    unit: str
    tags: dict[str, str]


@dataclass(frozen=True)
class IngestionResult:
    accepted: tuple[TelemetryEvent, ...]
    rejected: tuple[dict[str, object], ...]


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate keys rather than silently accepting the last value."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _validate_event(raw: object) -> TelemetryEvent:
    if not isinstance(raw, dict):
        raise ValueError("event must be a JSON object")
    required = {"event_id", "timestamp", "source", "metric", "value", "unit"}
    allowed = required | {"tags"}
    if not required.issubset(raw) or not set(raw).issubset(allowed):
        raise ValueError("event has missing or unknown fields")
    for key, max_length in MAX_FIELD_LENGTHS.items():
        if not isinstance(raw[key], str) or not raw[key].strip():
            raise ValueError(f"{key} must be a non-empty string")
        if len(raw[key]) > max_length:
            raise ValueError(f"{key} exceeds maximum length")
    timestamp = datetime.fromisoformat(raw["timestamp"].replace("Z", "+00:00"))
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    value = raw["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("value must be a finite number")
    try:
        numeric_value = float(value)
    except (OverflowError, ValueError):
        raise ValueError("value must be a finite number") from None
    if not math.isfinite(numeric_value):
        raise ValueError("value must be a finite number")
    tags = raw.get("tags", {})
    if not isinstance(tags, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in tags.items()
    ):
        raise ValueError("tags must be a string-to-string object")
    if len(tags) > MAX_TAGS:
        raise ValueError("tags exceed maximum count")
    if any(not k or len(k) > MAX_TAG_KEY_LENGTH for k in tags):
        raise ValueError("tag key is empty or exceeds maximum length")
    if any(len(v) > MAX_TAG_VALUE_LENGTH for v in tags.values()):
        raise ValueError("tag value exceeds maximum length")
    return TelemetryEvent(
        event_id=raw["event_id"].strip(),
        timestamp=timestamp.isoformat(),
        source=raw["source"].strip(),
        metric=raw["metric"].strip(),
        value=numeric_value,
        unit=raw["unit"].strip(),
        tags=dict(tags),
    )


def ingest_jsonl(lines: Iterable[str]) -> IngestionResult:
    """Parse bounded JSONL input; reject malformed rows and duplicate IDs.

    Processing stops at MAX_BATCH_LINES to bound memory and CPU use. When the
    limit is exceeded, one explicit rejection is recorded for the first
    out-of-range line and the remaining iterator is not consumed.
    """
    accepted: list[TelemetryEvent] = []
    rejected: list[dict[str, object]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(lines, start=1):
        if line_number > MAX_BATCH_LINES:
            rejected.append({
                "line": line_number,
                "reason": "batch exceeds maximum line count; remaining input not consumed",
            })
            break
        try:
            if not isinstance(line, str):
                raise ValueError("JSONL line must be a string")
            if len(line) > MAX_LINE_CHARS:
                raise ValueError("JSONL line exceeds maximum length")
            raw = json.loads(line, object_pairs_hook=_unique_object)
            event = _validate_event(raw)
            if event.event_id in seen:
                raise ValueError("duplicate event_id")
            seen.add(event.event_id)
            accepted.append(event)
        except (json.JSONDecodeError, TypeError, ValueError, OverflowError, RecursionError) as exc:
            rejected.append({"line": line_number, "reason": str(exc)})
    return IngestionResult(tuple(accepted), tuple(rejected))


def search_events(events: Iterable[TelemetryEvent], query: str, limit: int = 10) -> list[TelemetryEvent]:
    """Small deterministic lexical baseline; not a semantic/vector search engine."""
    if not isinstance(query, str) or not query.strip():
        return []
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    terms = set(TOKEN_RE.findall(query.lower()))
    if not terms:
        return []
    ranked: list[tuple[int, str, TelemetryEvent]] = []
    for event in events:
        text = " ".join([event.event_id, event.source, event.metric, event.unit, *event.tags.keys(), *event.tags.values()])
        overlap = len(terms.intersection(TOKEN_RE.findall(text.lower())))
        if overlap:
            ranked.append((overlap, event.event_id, event))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]
