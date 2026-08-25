from datetime import UTC, datetime

import pytest

from hottop.mechanism import HotspotMechanism, ProductMechanismMapping
from hottop.models import ProductProfile, TrendCandidate
from hottop.pipeline import build_batch, collect_and_build_batch


def _candidate(candidate_id: str, title: str, source: str, rank: int) -> TrendCandidate:
    return TrendCandidate(
        id=candidate_id,
        title=title,
        url=f"https://example.com/{candidate_id}",
        source=source,
        source_rank=rank,
        published_at=datetime(2026, 8, 20, 10, 0, tzinfo=UTC),
        tags=["film", "conflict"],
    )


def _mapping(candidate_id: str, product: str = "InkClawAgent") -> ProductMechanismMapping:
    return ProductMechanismMapping(
        mechanism=HotspotMechanism(
            topic_id=candidate_id,
            source_mode="fresh-discovered",
            recognition_hook="a recognizable conflict is resolved by changing the rule rather than copying its surface",
            causal_chain=["the problem appears", "friction escalates", "the rule changes", "work continues"],
            native_visual_grammar="original cinematic conflict staging",
            native_dialogue_grammar="short setup, escalation, clean reversal",
        ),
        promoted_product=product,
        product_role="the rule-changing route",
        product_bridge="the product removes the workflow assumption that creates the friction",
        outcome_before="the user is stuck in setup friction",
        outcome_after="the user returns to the real task",
        punchline="别耗在旧规则里。",
        comparison_target="work巴迪",
        comparison_role="the old friction-heavy route",
    )


def test_build_batch_dedupes_ranks_and_builds_only_reviewed_mechanism_briefs() -> None:
    product = ProductProfile(name="InkClawAgent", strengths=["multi-agent collaboration"])
    items = [
        _candidate("a", "The Odyssey returns", "source-a", 1),
        _candidate("b", "The Odyssey returns", "source-b", 2),
        _candidate("c", "Another topic", "source-c", 8),
    ]

    result = build_batch(
        items,
        product,
        comparison_target="work巴迪",
        top=2,
        now=datetime(2026, 8, 20, 12, 0, tzinfo=UTC),
        mechanism_mappings={"a": _mapping("a"), "c": _mapping("c")},
    )

    assert result.input_count == 3
    assert result.unique_count == 2
    assert len(result.briefs) == 2
    assert result.mechanism_required_ids == []
    assert result.briefs[0].topic.metrics["cross_source_count"] == 2.0
    assert result.briefs[0].role_map.comparison_target == "work巴迪"
    assert result.briefs[0].claim_status == "satire"


def test_build_batch_top_limits_ranked_output_without_inventing_briefs() -> None:
    product = ProductProfile(name="InkClawAgent")
    items = [
        _candidate("a", "Topic A", "source-a", 1),
        _candidate("b", "Topic B", "source-b", 2),
    ]

    result = build_batch(items, product, top=1)

    assert result.input_count == 2
    assert result.unique_count == 2
    assert len(result.ranked) == 1
    assert result.briefs == []
    assert result.mechanism_required_ids == [result.ranked[0].candidate.id]


class _FakeCollector:
    def __init__(self, items: list[TrendCandidate]) -> None:
        self.items = items
        self.limits: list[int] = []

    async def collect(self, limit: int = 30) -> list[TrendCandidate]:
        self.limits.append(limit)
        return self.items[:limit]


@pytest.mark.asyncio
async def test_collect_and_build_batch_fans_in_collectors_and_requires_analysis_for_missing_topic() -> None:
    product = ProductProfile(name="InkClawAgent")
    first = _FakeCollector([_candidate("a", "Shared topic", "source-a", 1)])
    second = _FakeCollector(
        [
            _candidate("b", "Shared topic", "source-b", 2),
            _candidate("c", "Unique topic", "source-b", 3),
        ]
    )

    result = await collect_and_build_batch(
        [first, second],
        product,
        comparison_target="work巴迪",
        limit_per_source=2,
        top=2,
        now=datetime(2026, 8, 20, 12, 0, tzinfo=UTC),
        mechanism_mappings={"a": _mapping("a")},
    )

    assert first.limits == [2]
    assert second.limits == [2]
    assert result.input_count == 3
    assert result.unique_count == 2
    assert len(result.briefs) == 1
    assert result.briefs[0].topic.metrics["cross_source_count"] == 2.0
    assert result.briefs[0].role_map.comparison_target == "work巴迪"
    assert result.mechanism_required_ids == ["c"]
