from datetime import UTC, datetime, timedelta

from hottop.models import TrendCandidate
from hottop.scoring import score_candidate


def test_recent_cross_source_visually_clear_topic_scores_higher():
    now = datetime.now(UTC)
    strong = TrendCandidate(
        id="strong",
        title="Odyssey cyclops confrontation",
        url="https://example.com/strong",
        source="dailyhot",
        published_at=now - timedelta(hours=2),
        tags=["film", "conflict", "visual"],
        metrics={
            "cross_source_count": 4,
            "recognizability": 0.9,
            "conflict_clarity": 0.95,
            "visual_potential": 0.95,
            "product_fit": 0.8,
            "evidence_quality": 0.8,
        },
    )
    weak = TrendCandidate(
        id="weak",
        title="Old generic topic",
        url="https://example.com/weak",
        source="rss",
        published_at=now - timedelta(days=10),
        metrics={"cross_source_count": 1, "recognizability": 0.2, "conflict_clarity": 0.1},
    )

    assert score_candidate(strong, now=now).total > score_candidate(weak, now=now).total


def test_score_is_bounded_0_to_100():
    candidate = TrendCandidate(
        id="x",
        title="Topic",
        url="https://example.com",
        source="x",
        metrics={"recognizability": 999, "product_fit": -5},
    )
    score = score_candidate(candidate)
    assert 0 <= score.total <= 100
