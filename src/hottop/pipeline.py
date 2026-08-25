from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Protocol

from pydantic import BaseModel, Field

from .briefing import build_brief
from .dedupe import merge_candidates
from .mechanism import MechanismMemeBrief, ProductMechanismMapping
from .models import ProductProfile, TrendCandidate, TrendScore
from .scoring import score_candidate


class Collector(Protocol):
    async def collect(self, limit: int = 30) -> list[TrendCandidate]: ...


class RankedCandidate(BaseModel):
    candidate: TrendCandidate
    score: TrendScore


class BatchResult(BaseModel):
    input_count: int = Field(ge=0)
    unique_count: int = Field(ge=0)
    ranked: list[RankedCandidate]
    briefs: list[MechanismMemeBrief]
    mechanism_required_ids: list[str] = Field(default_factory=list)


def build_batch(
    candidates: list[TrendCandidate],
    product: ProductProfile,
    comparison_target: str | None = None,
    top: int = 5,
    now: datetime | None = None,
    mechanism_mappings: dict[str, ProductMechanismMapping] | None = None,
) -> BatchResult:
    """Rank candidate hotspots and build briefs only where reviewed mechanism analysis exists.

    Discovery/ranking is deterministic. Creative mechanism understanding is not fabricated from title
    keywords: missing mappings are returned as explicit follow-up work instead of generic briefs.
    """

    if top < 1:
        raise ValueError("top must be at least 1")

    unique = merge_candidates(candidates)
    ranked = [
        RankedCandidate(candidate=candidate, score=score_candidate(candidate, now=now))
        for candidate in unique
    ]
    ranked.sort(key=lambda item: item.score.total, reverse=True)
    selected = ranked[:top]
    mappings = mechanism_mappings or {}

    briefs: list[MechanismMemeBrief] = []
    mechanism_required_ids: list[str] = []
    for item in selected:
        mapping = mappings.get(item.candidate.id)
        if mapping is None:
            mechanism_required_ids.append(item.candidate.id)
            continue
        briefs.append(
            build_brief(
                item.candidate,
                product,
                comparison_target=comparison_target,
                mechanism_mapping=mapping,
            )
        )

    return BatchResult(
        input_count=len(candidates),
        unique_count=len(unique),
        ranked=selected,
        briefs=briefs,
        mechanism_required_ids=mechanism_required_ids,
    )


async def collect_and_build_batch(
    collectors: list[Collector],
    product: ProductProfile,
    comparison_target: str | None = None,
    limit_per_source: int = 30,
    top: int = 5,
    now: datetime | None = None,
    mechanism_mappings: dict[str, ProductMechanismMapping] | None = None,
) -> BatchResult:
    if limit_per_source < 1:
        raise ValueError("limit_per_source must be at least 1")

    collected = await asyncio.gather(
        *(collector.collect(limit=limit_per_source) for collector in collectors)
    )
    candidates = [candidate for source_items in collected for candidate in source_items]
    return build_batch(
        candidates,
        product,
        comparison_target=comparison_target,
        top=top,
        now=now,
        mechanism_mappings=mechanism_mappings,
    )
