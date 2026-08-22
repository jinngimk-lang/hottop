from datetime import UTC, datetime

import pytest

from hottop.models import (
    ComparisonCandidate,
    Evidence,
    ProductProfile,
    PromotionContext,
    TrendCandidate,
)


def test_trend_candidate_requires_core_identity():
    candidate = TrendCandidate(
        id="dailyhot:1",
        title="A current topic",
        url="https://example.com/topic",
        source="dailyhot",
    )
    assert candidate.source == "dailyhot"
    assert candidate.tags == []
    assert candidate.evidence == []


def test_trend_candidate_normalizes_id_identity():
    candidate = TrendCandidate(
        id="  dailyhot:1  ",
        title="A current topic",
        url="https://example.com/topic",
        source="dailyhot",
    )

    assert candidate.id == "dailyhot:1"


def test_trend_candidate_rejects_blank_id_identity():
    with pytest.raises(ValueError, match="trend id must not be blank"):
        TrendCandidate(
            id="   ",
            title="A current topic",
            url="https://example.com/topic",
            source="dailyhot",
        )


def test_trend_candidate_normalizes_source_identity():
    candidate = TrendCandidate(
        id="dailyhot:1",
        title="A current topic",
        url="https://example.com/topic",
        source="  dailyhot  ",
    )

    assert candidate.source == "dailyhot"


def test_trend_candidate_rejects_blank_source_identity():
    with pytest.raises(ValueError, match="trend source must not be blank"):
        TrendCandidate(
            id="dailyhot:1",
            title="A current topic",
            url="https://example.com/topic",
            source="   ",
        )


def test_product_profile_defaults_to_satirical_comparison_posture():
    product = ProductProfile(name="InkClawAgent", url="https://inkclawagent.com/home")
    assert product.name == "InkClawAgent"
    assert product.default_claim_status == "satire"


def test_product_profile_normalizes_name_identity():
    product = ProductProfile(name="  Ribbon Lunch  ")

    assert product.name == "Ribbon Lunch"


def test_product_profile_rejects_blank_name_identity():
    with pytest.raises(ValueError, match="product profile name must not be blank"):
        ProductProfile(name="   ")


def test_evidence_keeps_timestamp_timezone_aware():
    now = datetime.now(UTC)
    evidence = Evidence(url="https://example.com/a", source="example", observed_at=now)
    assert evidence.observed_at.tzinfo is not None


def test_empty_title_is_rejected():
    with pytest.raises(ValueError):
        TrendCandidate(id="x", title="", url="https://example.com", source="x")


def test_promotion_context_normalizes_identity_fields():
    context = PromotionContext(
        subject_name="  Ribbon Lunch  ",
        subject_type="product",
        category="  food  ",
    )

    assert context.subject_name == "Ribbon Lunch"
    assert context.category == "food"


@pytest.mark.parametrize("field", ["subject_name", "category"])
def test_promotion_context_rejects_blank_identity_fields(field: str):
    payload = {
        "subject_name": "Ribbon Lunch",
        "subject_type": "product",
        "category": "food",
    }
    payload[field] = "   "

    with pytest.raises(ValueError, match=f"promotion {field.replace('_', ' ')} must not be blank"):
        PromotionContext(**payload)


def test_comparison_candidate_normalizes_name_identity():
    candidate = ComparisonCandidate(
        name="  Named Competitor  ",
        relation="direct-competitor",
    )

    assert candidate.name == "Named Competitor"


def test_comparison_candidate_rejects_blank_name_identity():
    with pytest.raises(ValueError, match="comparison candidate name must not be blank"):
        ComparisonCandidate(name="   ", relation="direct-competitor")
