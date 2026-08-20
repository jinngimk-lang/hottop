from __future__ import annotations

from datetime import UTC, datetime

from .models import TrendCandidate, TrendScore

WEIGHTS = {
    "recency": 0.25,
    "cross_source_presence": 0.20,
    "recognizability": 0.15,
    "conflict_clarity": 0.15,
    "visual_potential": 0.10,
    "product_fit": 0.10,
    "evidence_quality": 0.05,
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _recency(candidate: TrendCandidate, now: datetime) -> float:
    if candidate.published_at is None:
        return 0.35
    published = candidate.published_at
    if published.tzinfo is None:
        published = published.replace(tzinfo=UTC)
    age_hours = max(0.0, (now - published.astimezone(UTC)).total_seconds() / 3600)
    if age_hours <= 24:
        return 1.0
    if age_hours <= 72:
        return 0.75
    if age_hours <= 168:
        return 0.40
    return 0.10


def _cross_source(candidate: TrendCandidate) -> float:
    count = max(1.0, float(candidate.metrics.get("cross_source_count", 1)))
    return _clamp01(count / 5.0)


def score_candidate(candidate: TrendCandidate, now: datetime | None = None) -> TrendScore:
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)

    dimensions = {
        "recency": _recency(candidate, current),
        "cross_source_presence": _cross_source(candidate),
        "recognizability": _clamp01(candidate.metrics.get("recognizability", 0.5)),
        "conflict_clarity": _clamp01(candidate.metrics.get("conflict_clarity", 0.4)),
        "visual_potential": _clamp01(candidate.metrics.get("visual_potential", 0.4)),
        "product_fit": _clamp01(candidate.metrics.get("product_fit", 0.4)),
        "evidence_quality": _clamp01(candidate.metrics.get("evidence_quality", 0.4)),
    }
    total = sum(dimensions[name] * weight for name, weight in WEIGHTS.items()) * 100
    return TrendScore(total=round(max(0.0, min(100.0, total)), 2), dimensions=dimensions)
