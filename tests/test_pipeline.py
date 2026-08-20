from datetime import UTC, datetime

from hottop.models import ProductProfile, TrendCandidate
from hottop.pipeline import build_batch


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


def test_build_batch_dedupes_ranks_and_builds_briefs() -> None:
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
    )

    assert result.input_count == 3
    assert result.unique_count == 2
    assert len(result.briefs) == 2
    assert result.briefs[0].topic.metrics["cross_source_count"] == 2.0
    assert result.briefs[0].role_map.comparison_target == "work巴迪"
    assert result.briefs[0].claim_status == "satire"


def test_build_batch_top_limits_output() -> None:
    product = ProductProfile(name="InkClawAgent")
    items = [
        _candidate("a", "Topic A", "source-a", 1),
        _candidate("b", "Topic B", "source-b", 2),
    ]

    result = build_batch(items, product, top=1)

    assert result.input_count == 2
    assert result.unique_count == 2
    assert len(result.briefs) == 1
