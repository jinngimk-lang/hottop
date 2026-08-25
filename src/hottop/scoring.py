from __future__ import annotations

from datetime import UTC, datetime

from .models import TrendCandidate, TrendScore

WEIGHTS = {
    "recency": 0.20,
    "cross_source_presence": 0.16,
    "recognizability": 0.13,
    "conflict_clarity": 0.13,
    "visual_potential": 0.09,
    "product_fit": 0.09,
    "evidence_quality": 0.05,
    "source_quality": 0.08,
    "evidence_freshness": 0.07,
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _freshness_from_age_hours(age_hours: float) -> float:
    if age_hours <= 24:
        return 1.0
    if age_hours <= 72:
        return 0.75
    if age_hours <= 168:
        return 0.40
    if age_hours <= 336:
        return 0.20
    return 0.05


def _recency(candidate: TrendCandidate, now: datetime) -> float:
    if candidate.published_at is None:
        return 0.35
    published = candidate.published_at
    if published.tzinfo is None:
        published = published.replace(tzinfo=UTC)
    age_hours = max(0.0, (now - published.astimezone(UTC)).total_seconds() / 3600)
    return _freshness_from_age_hours(age_hours)


def _cross_source(candidate: TrendCandidate) -> float:
    count = max(1.0, float(candidate.metrics.get("cross_source_count", 1)))
    return _clamp01(count / 5.0)


def _source_quality(candidate: TrendCandidate) -> float:
    if candidate.source_quality is not None:
        return _clamp01(candidate.source_quality)
    return _clamp01(candidate.metrics.get("source_quality", 0.5))


def _evidence_freshness(candidate: TrendCandidate, now: datetime) -> float:
    if not candidate.evidence:
        return 0.25

    scores: list[float] = []
    for evidence in candidate.evidence:
        timestamp = evidence.published_at or evidence.observed_at
        age_hours = max(0.0, (now - timestamp.astimezone(UTC)).total_seconds() / 3600)
        freshness = _freshness_from_age_hours(age_hours)
        quality = evidence.source_quality if evidence.source_quality is not None else 0.5
        scores.append(freshness * (0.7 + 0.3 * _clamp01(quality)))
    return _clamp01(sum(scores) / len(scores))


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
        "source_quality": _source_quality(candidate),
        "evidence_freshness": _evidence_freshness(candidate, current),
    }
    total = sum(dimensions[name] * weight for name, weight in WEIGHTS.items()) * 100
    return TrendScore(total=round(max(0.0, min(100.0, total)), 2), dimensions=dimensions)
