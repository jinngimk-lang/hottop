import pytest

from hottop.creative import CreativeContextReview, CreativeReview
from hottop.intake import resolve_intent
from hottop.models import CreativeConcept, PromotionContext
from hottop.orchestrator import OrchestrationInput, OrchestrationOption, orchestrate


def _concept(topic_id: str, expression_form: str, bridge: str) -> CreativeConcept:
    return CreativeConcept.model_validate(
        {
            "topic": {
                "id": topic_id,
                "title": "Fictional culture moment",
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
                "category_default": "show the bowl immediately",
                "deleted_constraint": "full product reveal in frame one",
                "new_competition_axis": "curiosity before reveal",
                "bridge_type": "shape-material",
                "bridge": bridge,
                "expression_form": expression_form,
            },
            "beats": [
                {"scene": "A ribbon crosses the frame.", "caption": None, "intent": "tease"},
                {"scene": "Texture reveals the ribbon is food.", "caption": "Wait for it.", "intent": "material clue"},
                {"scene": "The ribbon lands in the product bowl.", "caption": "The reveal is the product.", "intent": "reveal"},
            ],
            "visual_medium": "commercial-product",
            "genre_treatment": "minimal premium food photography",
            "punchlines": ["The reveal is the product."],
            "image_prompt": "Original product-led reveal using a ribbon-like food action.",
            "negative_prompt": "No copied layout, protected character, logo, or trade dress.",
            "risk_flags": [],
            "claim_status": "satire",
        }
    )


def _review(name: str, ownability: float = 0.9) -> CreativeReview:
    return CreativeReview(name=name, instant_comprehension=0.9, natural_linkage=0.9, product_centrality=0.9, surprise=0.85, ownability=ownability, evidence_safety=0.95, original_execution=0.95)


def _context(name: str, score: float, *, humor_expected: bool = False) -> CreativeContextReview:
    return CreativeContextReview(name=name, platform_fit=score, style_fit=score, campaign_goal_fit=score, ambition_fit=score, project_shape_fit=score, hotspot_native_fit=score, humor_or_delight=score, humor_expected=humor_expected)


def _promotion_context() -> PromotionContext:
    return PromotionContext(subject_name="Ribbon Lunch", subject_type="product", category="food", primary_job="memorable quick lunch", primary_pain_point="generic food ads look interchangeable", primary_differentiator="long elastic ribbon texture", semantic_terms=["long", "elastic", "ribbon"])


def _option(label: str = "bridge-reveal") -> OrchestrationOption:
    return OrchestrationOption(label=label, concept=_concept(label, "swipe-reveal", "the product ribbon becomes the visual action"), review=_review(label), context_review=_context(label, 0.95))


def test_orchestrator_selects_platform_fit_passing_candidate_and_keeps_alternates():
    intent = resolve_intent("给这个食品新品做一个小红书出圈高级广告，产品最后再揭示", overrides={"promotion_target": "Ribbon Lunch"})
    payload = OrchestrationInput(intent=intent, promotion_context=_promotion_context(), options=[OrchestrationOption(label="pain-contrast", concept=_concept("pain", "four-panel", "generic old way conflict"), review=_review("pain-contrast"), context_review=_context("pain-contrast", 0.68)), _option(), OrchestrationOption(label="category-reframe", concept=_concept("reframe", "split-old-vs-new", "remove full reveal convention"), review=_review("category-reframe"), context_review=_context("category-reframe", 0.78))], references=[])
    result = orchestrate(payload)
    assert result.schema_version == "hottop.orchestration.v1"
    assert result.selected_label == "bridge-reveal"
    assert result.selected_render.schema_version == "hottop.render.v2"
    assert result.selected_render.expression_form == "swipe-reveal"
    assert len(result.alternates) == 2
    assert "platform" in result.selection_rationale.lower()


def test_orchestrator_rejects_when_all_candidates_fail_existing_hard_gate():
    intent = resolve_intent("宣传这个产品", overrides={"promotion_target": "Ribbon Lunch"})
    payload = OrchestrationInput(intent=intent, promotion_context=_promotion_context(), options=[OrchestrationOption(label="generic", concept=_concept("bad", "single-visual-metaphor", "hot character plus logo"), review=_review("generic", ownability=0.3), context_review=_context("generic", 1.0))], references=[])
    with pytest.raises(ValueError, match="creative review gate"):
        orchestrate(payload)


def test_orchestration_option_rejects_review_for_a_different_label():
    with pytest.raises(ValueError, match="review name must match option label"):
        OrchestrationOption(label="bridge-reveal", concept=_concept("mismatch", "swipe-reveal", "the product ribbon becomes the action"), review=_review("different-concept"), context_review=_context("bridge-reveal", 0.95))


def test_orchestration_input_rejects_concept_for_a_different_promotion_context():
    intent = resolve_intent("宣传另一个产品", overrides={"promotion_target": "Other Product"})
    context = PromotionContext(subject_name="Other Product", subject_type="product", category="consumer")
    with pytest.raises(ValueError, match="concept promotion must match orchestration promotion context"):
        OrchestrationInput(intent=intent, promotion_context=context, options=[OrchestrationOption(label="wrong-product", concept=_concept("wrong-product", "single-visual-metaphor", "a strong bridge for a different product"), review=_review("wrong-product"), context_review=_context("wrong-product", 0.9))], references=[])


def test_orchestration_input_rejects_intent_for_a_different_promotion_target():
    intent = resolve_intent("宣传另一个产品", overrides={"promotion_target": "Other Product"})
    with pytest.raises(ValueError, match="intent promotion target must match orchestration promotion context"):
        OrchestrationInput(intent=intent, promotion_context=_promotion_context(), options=[OrchestrationOption(label="right-concept-wrong-intent", concept=_concept("right-concept-wrong-intent", "swipe-reveal", "the product ribbon becomes the visual action"), review=_review("right-concept-wrong-intent"), context_review=_context("right-concept-wrong-intent", 0.9))], references=[])


def test_orchestration_option_rejects_context_review_for_a_different_label():
    context_review = CreativeContextReview.model_validate({"name": "different-concept", "platform_fit": 0.95, "style_fit": 0.95, "campaign_goal_fit": 0.95, "ambition_fit": 0.95, "project_shape_fit": 0.95, "hotspot_native_fit": 0.95, "humor_or_delight": 0.95, "humor_expected": False})
    with pytest.raises(ValueError, match="context review name must match option label"):
        OrchestrationOption(label="bridge-reveal", concept=_concept("context-mismatch", "swipe-reveal", "the product ribbon becomes the action"), review=_review("bridge-reveal"), context_review=context_review)


def test_context_review_identity_is_canonical_in_orchestration_result():
    intent = resolve_intent("宣传这个产品", overrides={"promotion_target": "Ribbon Lunch"})
    payload = OrchestrationInput(intent=intent, promotion_context=_promotion_context(), options=[OrchestrationOption(label="bridge-reveal", concept=_concept("canonical-context", "swipe-reveal", "the product ribbon becomes the action"), review=_review("bridge-reveal"), context_review=_context("  bridge-reveal  ", 0.95))], references=[])
    result = orchestrate(payload)
    assert result.selected_review.context.name == result.selected_label == "bridge-reveal"


def test_intent_promotion_identity_is_canonical_in_orchestration_result():
    intent = resolve_intent("宣传这个产品", overrides={"promotion_target": "  Ribbon Lunch  "})
    payload = OrchestrationInput(intent=intent, promotion_context=_promotion_context(), options=[_option()], references=[])
    result = orchestrate(payload)
    assert result.intent.promotion_target.value == result.promotion_context.subject_name == "Ribbon Lunch"
