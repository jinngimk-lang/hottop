import pytest
from pydantic import ValidationError

from hottop.models import (
    CreativeBeat,
    CreativeConcept,
    CreativeStrategy,
    PromotionContext,
    TrendCandidate,
)
from hottop.rendering import build_creative_render_request


def _concept(**overrides: object) -> CreativeConcept:
    data = {
        "topic": TrendCandidate(
            id="culture:render-text",
            title="A visual action becomes a social meme",
            url="https://example.com/culture",
            source="culture",
        ),
        "promotion": PromotionContext(
            subject_name="Ribbon Noodle",
            subject_type="product",
            category="food",
        ),
        "strategy": CreativeStrategy(
            bridge_type="shape-material",
            bridge="the food ribbon becomes the recognizable visual action",
            expression_form="single-visual-metaphor",
        ),
        "beats": [CreativeBeat(scene="one decisive product image", intent="reveal")],
        "visual_medium": "commercial-product",
        "genre_treatment": "minimal premium studio photography",
        "punchlines": ["先让人想看，再让人想吃。"],
        "image_prompt": "Create an original premium food advertisement.",
        "negative_prompt": "No protected character replica or copied ad layout.",
    }
    data.update(overrides)
    return CreativeConcept.model_validate(data)


def test_creative_concept_canonicalizes_required_render_text() -> None:
    concept = _concept(
        genre_treatment="  minimal premium studio photography  ",
        punchlines=["  先让人想看，再让人想吃。  "],
        image_prompt="  Create an original premium food advertisement.  ",
        negative_prompt="  No protected character replica or copied ad layout.  ",
    )

    assert concept.genre_treatment == "minimal premium studio photography"
    assert concept.punchlines == ["先让人想看，再让人想吃。"]
    assert concept.image_prompt == "Create an original premium food advertisement."
    assert concept.negative_prompt == "No protected character replica or copied ad layout."


@pytest.mark.parametrize("field", ["genre_treatment", "image_prompt", "negative_prompt"])
def test_creative_concept_rejects_blank_required_render_text(field: str) -> None:
    with pytest.raises(ValidationError):
        _concept(**{field: "   "})


def test_creative_concept_rejects_blank_punchline() -> None:
    with pytest.raises(ValidationError):
        _concept(punchlines=["   "])


def test_creative_concept_canonicalizes_risk_flags() -> None:
    concept = _concept(risk_flags=["  avoid protected likenesses  "])

    assert concept.risk_flags == ["avoid protected likenesses"]


def test_creative_concept_rejects_blank_risk_flag() -> None:
    with pytest.raises(ValidationError):
        _concept(risk_flags=["   "])


def test_swipe_reveal_render_request_preserves_strategy_and_medium() -> None:
    topic = TrendCandidate(
        id="culture:stretch-food",
        title="A visual action becomes a social meme",
        url="https://example.com/culture",
        source="culture",
    )
    concept = CreativeConcept(
        topic=topic,
        promotion=PromotionContext(
            subject_name="Ribbon Noodle",
            subject_type="product",
            category="food",
            primary_job="deliver a memorable eating experience",
            primary_pain_point="ordinary food ads look interchangeable",
            primary_differentiator="long, elastic ribbon-like texture",
        ),
        strategy=CreativeStrategy(
            category_default="show the plated dish directly",
            deleted_constraint="reveal the product immediately",
            new_competition_axis="visual curiosity before product reveal",
            bridge_type="shape-material",
            bridge="the food ribbon becomes the recognizable visual action",
            expression_form="swipe-reveal",
        ),
        comparison_target="ordinary food-ad convention",
        beats=[
            CreativeBeat(scene="only the stretching action is visible", intent="tease"),
            CreativeBeat(scene="the material resemblance becomes clearer", intent="extend"),
            CreativeBeat(scene="the food product is finally revealed", caption="原来是它", intent="reveal"),
        ],
        visual_medium="commercial-product",
        genre_treatment="minimal premium studio photography",
        punchlines=["先让人想看，再让人想吃。"],
        image_prompt="Create an original premium swipe-reveal food advertisement.",
        negative_prompt="No protected character replica or copied ad layout.",
    )

    request = build_creative_render_request(concept)

    assert request.schema_version == "hottop.render.v2"
    assert request.expression_form == "swipe-reveal"
    assert request.visual_medium == "commercial-product"
    assert request.genre_treatment == "minimal premium studio photography"
    assert request.deleted_constraint == "reveal the product immediately"
    assert request.bridge_type == "shape-material"
    assert len(request.frames) == 3
    assert request.frames[-1].intent == "reveal"
    assert request.frames[-1].caption == "原来是它"


def test_flexible_render_contract_does_not_require_four_frames() -> None:
    topic = TrendCandidate(
        id="film:single-moment",
        title="A cinematic cultural moment",
        url="https://example.com/film",
        source="film",
    )
    concept = CreativeConcept(
        topic=topic,
        promotion=PromotionContext(
            subject_name="ProductX",
            subject_type="product",
            category="consumer",
        ),
        strategy=CreativeStrategy(
            bridge_type="function",
            bridge="the product becomes the decisive key",
            expression_form="faux-film-still",
        ),
        beats=[CreativeBeat(scene="one decisive cinematic image", intent="punchline")],
        visual_medium="live-action-cinematic",
        genre_treatment="original high-budget adventure realism",
        punchlines=["一眼就懂。"],
        image_prompt="Create one original cinematic advertising still.",
        negative_prompt="No actor likeness or exact film frame.",
    )

    request = build_creative_render_request(concept)

    assert len(request.frames) == 1
    assert request.expression_form == "faux-film-still"


def test_motion_distribution_contract_survives_creative_render_handoff() -> None:
    concept = _concept(
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
    )

    request = build_creative_render_request(concept)
    payload = request.model_dump(mode="json")

    assert payload["distribution_mode"] == "motion"
    assert payload["in_asset_cta_policy"] == "no-destination"
    assert payload["motion_continuity_required"] is True


def test_distribution_render_contract_is_backward_compatible_for_existing_concepts() -> None:
    request = build_creative_render_request(_concept())

    assert request.distribution_mode == "auto"
    assert request.in_asset_cta_policy == "no-destination"
    assert request.motion_continuity_required is False
