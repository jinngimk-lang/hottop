from datetime import UTC, datetime

import pytest

from hottop.models import (
    ComparisonCandidate,
    CreativeBeat,
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


@pytest.mark.parametrize(
    "field",
    [
        "keywords",
        "jobs_to_be_done",
        "pain_points_solved",
        "differentiators",
        "known_alternatives",
        "strengths",
        "preferred_roles",
    ],
)
def test_product_profile_normalizes_semantic_lists(field: str):
    product = ProductProfile(name="Ribbon Lunch", **{field: ["  tactile product truth  "]})

    assert getattr(product, field) == ["tactile product truth"]


@pytest.mark.parametrize(
    "field",
    [
        "keywords",
        "jobs_to_be_done",
        "pain_points_solved",
        "differentiators",
        "known_alternatives",
        "strengths",
        "preferred_roles",
    ],
)
def test_product_profile_rejects_blank_semantic_list_items(field: str):
    with pytest.raises(ValueError, match="product profile semantic lists must not contain blank text"):
        ProductProfile(name="Ribbon Lunch", **{field: ["useful semantic", "   "]})


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


def test_promotion_context_normalizes_resolved_semantics():
    context = PromotionContext(
        subject_name="Ribbon Lunch",
        subject_type="product",
        category="food",
        primary_job="  make lunch feel more playful  ",
        primary_pain_point="  repetitive lunch routines  ",
        primary_differentiator="  long ribbon-like shape  ",
    )

    assert context.primary_job == "make lunch feel more playful"
    assert context.primary_pain_point == "repetitive lunch routines"
    assert context.primary_differentiator == "long ribbon-like shape"


@pytest.mark.parametrize(
    "field",
    ["primary_job", "primary_pain_point", "primary_differentiator"],
)
def test_promotion_context_rejects_blank_resolved_semantics(field: str):
    payload = {
        "subject_name": "Ribbon Lunch",
        "subject_type": "product",
        "category": "food",
        field: "   ",
    }

    with pytest.raises(ValueError, match=f"promotion {field.replace('_', ' ')} must not be blank"):
        PromotionContext(**payload)


def test_promotion_context_normalizes_semantic_terms():
    context = PromotionContext(
        subject_name="Ribbon Lunch",
        subject_type="product",
        category="food",
        semantic_terms=["  ribbon-like shape  ", "  playful lunch ritual  "],
    )

    assert context.semantic_terms == ["ribbon-like shape", "playful lunch ritual"]


def test_promotion_context_rejects_blank_semantic_terms():
    with pytest.raises(ValueError, match="promotion semantic terms must not contain blank text"):
        PromotionContext(
            subject_name="Ribbon Lunch",
            subject_type="product",
            category="food",
            semantic_terms=["ribbon-like shape", "   "],
        )


def test_comparison_candidate_normalizes_name_identity():
    candidate = ComparisonCandidate(
        name="  Named Competitor  ",
        relation="direct-competitor",
    )

    assert candidate.name == "Named Competitor"


def test_comparison_candidate_rejects_blank_name_identity():
    with pytest.raises(ValueError, match="comparison candidate name must not be blank"):
        ComparisonCandidate(name="   ", relation="direct-competitor")


def test_comparison_candidate_normalizes_notes():
    candidate = ComparisonCandidate(
        name="Named Competitor",
        relation="direct-competitor",
        notes=["  factual limitation for creative handoff  "],
    )

    assert candidate.notes == ["factual limitation for creative handoff"]


def test_comparison_candidate_rejects_blank_notes():
    with pytest.raises(ValueError, match="comparison candidate notes must not contain blank text"):
        ComparisonCandidate(
            name="Named Competitor",
            relation="direct-competitor",
            notes=["supported context", "   "],
        )


def test_creative_beat_normalizes_render_text():
    beat = CreativeBeat(
        scene="  Ribbon stretches across the table  ",
        intent="  delay the product reveal  ",
    )

    assert beat.scene == "Ribbon stretches across the table"
    assert beat.intent == "delay the product reveal"


@pytest.mark.parametrize("field", ["scene", "intent"])
def test_creative_beat_rejects_blank_render_text(field: str):
    payload = {
        "scene": "Ribbon stretches across the table",
        "intent": "delay the product reveal",
    }
    payload[field] = "   "

    with pytest.raises(ValueError, match=f"creative beat {field} must not be blank"):
        CreativeBeat(**payload)


def test_creative_beat_normalizes_caption_when_present():
    beat = CreativeBeat(
        scene="Ribbon stretches across the table",
        caption="  Keep pulling.  ",
        intent="delay the product reveal",
    )

    assert beat.caption == "Keep pulling."


def test_creative_beat_rejects_blank_caption_when_present():
    with pytest.raises(ValueError, match="creative beat caption must not be blank"):
        CreativeBeat(
            scene="Ribbon stretches across the table",
            caption="   ",
            intent="delay the product reveal",
        )
