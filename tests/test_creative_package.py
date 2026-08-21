import pytest

from hottop.creative_package import CreativePackageInput, build_creative_package


def _concept(*, topic_id: str, expression_form: str, bridge: str) -> dict:
    return {
        "topic": {"id": topic_id, "title": "Fictional ribbon-food culture moment", "url": f"https://example.com/{topic_id}", "source": "test", "tags": ["culture", "food"]},
        "promotion": {"subject_name": "Ribbon Lunch", "subject_type": "product", "category": "food", "primary_job": "memorable quick lunch", "primary_pain_point": "generic food ads look interchangeable", "primary_differentiator": "long elastic ribbon texture", "semantic_terms": ["long", "elastic", "ribbon"]},
        "strategy": {"category_default": "show the finished bowl immediately", "deleted_constraint": "the product must be fully revealed at the start", "new_competition_axis": "curiosity and visual participation", "bridge_type": "shape-material", "bridge": bridge, "expression_form": expression_form},
        "beats": [{"scene": "A minimal original gesture launches a ribbon-like strand.", "caption": None, "intent": "tease"}, {"scene": "The strand reveals food texture while crossing the frame.", "caption": "Wait for it.", "intent": "extend curiosity"}, {"scene": "The strand lands in a fictional bowl and reveals the product.", "caption": "The reveal is the product.", "intent": "reveal"}],
        "visual_medium": "commercial-product", "genre_treatment": "minimal premium food photography with playful social pacing", "punchlines": ["The reveal is the product."], "image_prompt": "Original commercial food sequence with a ribbon-like product action.", "negative_prompt": "No copied ad layout, character design, logo, or trade dress.", "risk_flags": [], "claim_status": "satire",
    }


def _option(label: str, topic_id: str = "option") -> dict:
    return {
        "label": label,
        "concept": _concept(topic_id=topic_id, expression_form="swipe-reveal", bridge="the product ribbon becomes the visual action"),
        "review": {"name": label, "instant_comprehension": 0.95, "natural_linkage": 0.95, "product_centrality": 0.95, "surprise": 0.95, "ownability": 0.95, "evidence_safety": 0.95, "original_execution": 0.95},
    }


def test_package_selects_highest_scoring_passing_option_and_preserves_reference():
    weak = _option("pain-point-contrast", "weak")
    weak["review"].update({"product_centrality": 0.4, "surprise": 0.4, "ownability": 0.35})
    strong = _option("bridge-led-reveal", "strong")
    package = CreativePackageInput.model_validate({"options": [weak, strong], "references": [{"source_url": "https://example.com/reference", "source_title": "Fictional campaign reference", "source_type": "campaign-page", "rights_mode": "analysis-only", "expression_form": "swipe-reveal", "visual_medium": "commercial-product", "composition_grammar": ["one dominant object", "large negative space"], "reveal_pattern": "abstract action → material clue → product reveal", "text_grammar": "minimal copy", "bridge_type": "shape-material", "why_effective": "curiosity is resolved by the product itself", "what_not_to_copy": ["exact composition", "branding", "source pixels"], "provenance_note": "Public reference used only to study grammar."}]})
    result = build_creative_package(package)
    assert result.schema_version == "hottop.creative-package.v1"
    assert result.selected_index == 1
    assert result.selected_concept.topic.id == "strong"
    assert result.selected_render.schema_version == "hottop.render.v2"
    assert len(result.references) == 1
    assert result.option_diagnostics[0].passes is False
    assert result.option_diagnostics[1].passes is True


def test_package_refuses_to_select_when_all_options_fail_hard_gate():
    option = _option("forced-hot-character", "forced")
    option["review"].update({"natural_linkage": 0.3, "product_centrality": 0.3, "surprise": 0.4, "ownability": 0.3})
    package = CreativePackageInput.model_validate({"options": [option]})
    with pytest.raises(ValueError, match="passed the creative review gate"):
        build_creative_package(package)


def test_package_rejects_review_bound_to_a_different_option_label():
    option = _option("bridge-led-reveal", "mismatched-review")
    option["review"]["name"] = "different-concept"
    with pytest.raises(ValueError, match="review name must match option label"):
        CreativePackageInput.model_validate({"options": [option]})


def test_package_rejects_whitespace_only_option_identity():
    option = _option("   ", "blank-identity")
    with pytest.raises(ValueError, match="option label must not be blank"):
        CreativePackageInput.model_validate({"options": [option]})


def test_package_rejects_duplicate_option_identities():
    with pytest.raises(ValueError, match="option labels must be unique"):
        CreativePackageInput.model_validate({"options": [_option("same", "first"), _option("same", "second")]})
