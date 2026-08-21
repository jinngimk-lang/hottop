import pytest

from hottop.creative_package import CreativePackageInput, build_creative_package


def _concept(*, topic_id: str, expression_form: str, bridge: str) -> dict:
    return {
        "topic": {
            "id": topic_id,
            "title": "Fictional ribbon-food culture moment",
            "url": f"https://example.com/{topic_id}",
            "source": "test",
            "tags": ["culture", "food"],
        },
        "promotion": {
            "subject_name": "Ribbon Lunch",
            "subject_type": "product",
            "category": "food",
            "primary_job": "memorable quick lunch",
            "primary_pain_point": "generic food ads look interchangeable",
            "primary_differentiator": "long elastic ribbon texture",
            "semantic_terms": ["long", "elastic", "ribbon"],
        },
        "strategy": {
            "category_default": "show the finished bowl immediately",
            "deleted_constraint": "the product must be fully revealed at the start",
            "new_competition_axis": "curiosity and visual participation",
            "bridge_type": "shape-material",
            "bridge": bridge,
            "expression_form": expression_form,
        },
        "beats": [
            {
                "scene": "A minimal original gesture launches a ribbon-like strand.",
                "caption": None,
                "intent": "tease",
            },
            {
                "scene": "The strand reveals food texture while crossing the frame.",
                "caption": "Wait for it.",
                "intent": "extend curiosity",
            },
            {
                "scene": "The strand lands in a fictional bowl and reveals the product.",
                "caption": "The reveal is the product.",
                "intent": "reveal",
            },
        ],
        "visual_medium": "commercial-product",
        "genre_treatment": "minimal premium food photography with playful social pacing",
        "punchlines": ["The reveal is the product."],
        "image_prompt": "Original commercial food sequence with a ribbon-like product action.",
        "negative_prompt": "No copied ad layout, character design, logo, or trade dress.",
        "risk_flags": [],
        "claim_status": "satire",
    }


def test_package_selects_highest_scoring_passing_option_and_preserves_reference():
    package = CreativePackageInput.model_validate(
        {
            "options": [
                {
                    "label": "pain-point-contrast",
                    "concept": _concept(
                        topic_id="weak",
                        expression_form="four-panel",
                        bridge="the product is a generic hero beside the hotspot",
                    ),
                    "review": {
                        "name": "pain-point-contrast",
                        "instant_comprehension": 0.8,
                        "natural_linkage": 0.7,
                        "product_centrality": 0.4,
                        "surprise": 0.4,
                        "ownability": 0.35,
                        "evidence_safety": 0.9,
                        "original_execution": 0.8,
                    },
                },
                {
                    "label": "bridge-led-reveal",
                    "concept": _concept(
                        topic_id="strong",
                        expression_form="swipe-reveal",
                        bridge="the product ribbon becomes the visual action before the food reveal",
                    ),
                    "review": {
                        "name": "bridge-led-reveal",
                        "instant_comprehension": 0.92,
                        "natural_linkage": 0.95,
                        "product_centrality": 0.97,
                        "surprise": 0.88,
                        "ownability": 0.93,
                        "evidence_safety": 0.95,
                        "original_execution": 0.95,
                    },
                },
            ],
            "references": [
                {
                    "source_url": "https://example.com/reference",
                    "source_title": "Fictional campaign reference",
                    "source_type": "campaign-page",
                    "rights_mode": "analysis-only",
                    "expression_form": "swipe-reveal",
                    "visual_medium": "commercial-product",
                    "composition_grammar": ["one dominant object", "large negative space"],
                    "reveal_pattern": "abstract action → material clue → product reveal",
                    "text_grammar": "minimal copy",
                    "bridge_type": "shape-material",
                    "why_effective": "curiosity is resolved by the product itself",
                    "what_not_to_copy": ["exact composition", "branding", "source pixels"],
                    "provenance_note": "Public reference used only to study grammar.",
                }
            ],
        }
    )

    result = build_creative_package(package)

    assert result.schema_version == "hottop.creative-package.v1"
    assert result.selected_index == 1
    assert result.selected_concept.topic.id == "strong"
    assert result.selected_render.schema_version == "hottop.render.v2"
    assert result.selected_render.expression_form == "swipe-reveal"
    assert len(result.references) == 1
    assert result.references[0].rights_mode == "analysis-only"
    assert result.option_diagnostics[0].passes is False
    assert result.option_diagnostics[1].passes is True


def test_package_refuses_to_select_when_all_options_fail_hard_gate():
    package = CreativePackageInput.model_validate(
        {
            "options": [
                {
                    "label": "forced-hot-character",
                    "concept": _concept(
                        topic_id="forced",
                        expression_form="single-visual-metaphor",
                        bridge="hot character plus logo",
                    ),
                    "review": {
                        "name": "forced-hot-character",
                        "instant_comprehension": 0.8,
                        "natural_linkage": 0.3,
                        "product_centrality": 0.3,
                        "surprise": 0.4,
                        "ownability": 0.3,
                        "evidence_safety": 0.9,
                        "original_execution": 0.8,
                    },
                }
            ]
        }
    )

    with pytest.raises(ValueError, match="passed the creative review gate"):
        build_creative_package(package)


def test_package_rejects_review_bound_to_a_different_option_label():
    with pytest.raises(ValueError, match="review name must match option label"):
        CreativePackageInput.model_validate(
            {
                "options": [
                    {
                        "label": "bridge-led-reveal",
                        "concept": _concept(
                            topic_id="mismatched-review",
                            expression_form="swipe-reveal",
                            bridge="the product ribbon becomes the visual action",
                        ),
                        "review": {
                            "name": "different-concept",
                            "instant_comprehension": 0.95,
                            "natural_linkage": 0.95,
                            "product_centrality": 0.95,
                            "surprise": 0.95,
                            "ownability": 0.95,
                            "evidence_safety": 0.95,
                            "original_execution": 0.95,
                        },
                    }
                ]
            }
        )
