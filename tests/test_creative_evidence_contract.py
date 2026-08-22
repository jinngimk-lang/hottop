import pytest
from pydantic import ValidationError

from hottop.models import (
    CreativeBeat,
    CreativeConcept,
    CreativeStrategy,
    Evidence,
    PromotionContext,
    TrendCandidate,
)
from hottop.rendering import build_creative_render_request


def _concept_payload() -> dict:
    return {
        "topic": TrendCandidate(
            id="tech:workflow",
            title="A workflow trend",
            url="https://example.com/trend",
            source="example",
        ),
        "promotion": PromotionContext(
            subject_name="ProductX",
            subject_type="product",
            category="software",
        ),
        "strategy": CreativeStrategy(
            category_default="more manual steps",
            deleted_constraint="manual handoffs",
            new_competition_axis="continuous coordination",
            bridge_type="function",
            bridge="the product becomes the coordination route",
            expression_form="split-old-vs-new",
        ),
        "comparison_target": "Named Competitor",
        "beats": [
            CreativeBeat(scene="old workflow beside new workflow", intent="contrast"),
        ],
        "visual_medium": "technology-realism",
        "genre_treatment": "original contemporary software campaign imagery",
        "punchlines": ["Change the workflow, not the claim."],
        "image_prompt": "Create an original workflow comparison visual.",
        "negative_prompt": "No proprietary UI, logos, or copied layouts.",
    }


def test_supported_creative_claim_requires_comparison_evidence() -> None:
    payload = _concept_payload()
    payload["claim_status"] = "supported"

    with pytest.raises(ValidationError, match="supported creative claims require comparison evidence"):
        CreativeConcept(**payload)


def test_named_comparison_cannot_remain_needs_evidence_in_production() -> None:
    payload = _concept_payload()
    payload["claim_status"] = "needs_evidence"

    with pytest.raises(
        ValidationError,
        match="named creative comparisons must be supported by evidence or explicit satire",
    ):
        CreativeConcept(**payload)


def test_creative_comparison_target_is_canonical() -> None:
    payload = _concept_payload()
    payload["comparison_target"] = "  Named Competitor  "

    concept = CreativeConcept(**payload)

    assert concept.comparison_target == "Named Competitor"


def test_creative_comparison_target_rejects_blank_identity() -> None:
    payload = _concept_payload()
    payload["comparison_target"] = "   "

    with pytest.raises(ValidationError, match="comparison target must not be blank"):
        CreativeConcept(**payload)


def test_render_v2_preserves_comparison_evidence_provenance() -> None:
    payload = _concept_payload()
    payload["claim_status"] = "supported"
    payload["comparison_evidence"] = [
        Evidence(
            url="https://example.com/evidence",
            source="Primary source",
            note="Supports the limited comparison used by the concept.",
        )
    ]
    concept = CreativeConcept(**payload)

    request = build_creative_render_request(concept)

    assert request.claim_status == "supported"
    assert len(request.comparison_evidence) == 1
    assert str(request.comparison_evidence[0].url) == "https://example.com/evidence"
    assert request.comparison_evidence[0].source == "Primary source"
