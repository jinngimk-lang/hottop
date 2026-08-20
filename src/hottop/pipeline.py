from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .briefing import build_brief
from .dedupe import merge_candidates
from .models import MemeBrief, ProductProfile, TrendCandidate, TrendScore
from .scoring import score_candidate


class RankedCandidate(BaseModel):
    candidate: TrendCandidate
    score: TrendScore


class BatchResult(BaseModel):
    input_count: int = Field(ge=0)
    unique_count: int = Field(ge=0)
    ranked: list[RankedCandidate]
    briefs: list[MemeBrief]


def build_batch(
    candidates: list[TrendCandidate],
    product: ProductProfile,
    comparison_target: str | None = None,
    top: int = 5,
    now: datetime | None = None,
) -> BatchResult:
    if top < 1:
        raise ValueError("top must be at least 1")

    unique = merge_candidates(candidates)
    ranked = [
        RankedCandidate(candidate=candidate, score=score_candidate(candidate, now=now))
        for candidate in unique
    ]
    ranked.sort(key=lambda item: item.score.total, reverse=True)
    selected = ranked[:top]
    briefs = [
        build_brief(item.candidate, product, comparison_target=comparison_target)
        for item in selected
    ]

    return BatchResult(
        input_count=len(candidates),
        unique_count=len(unique),
        ranked=selected,
        briefs=briefs,
    )
