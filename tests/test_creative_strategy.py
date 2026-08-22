from hottop.creative import (
    BridgeCandidate,
    CreativeReview,
    CreativeSignals,
    build_creative_strategy,
    select_best_bridge,
    select_best_review,
    select_expression_form,
    select_visual_medium,
)
from hottop.models import CreativeStrategy


def test_creative_strategy_persists_reframing_and_bridge_fields() -> None:
    strategy = CreativeStrategy(
        category_default="better physical keyboard",
        deleted_constraint="physical keyboard",
        new_competition_axis="direct touch interaction",
        bridge_type="action-motion",
        bridge="the promoted product becomes the action itself",
        expression_form="split-old-vs-new",
    )

    assert strategy.deleted_constraint == "physical keyboard"
    assert strategy.bridge_type == "action-motion"
    assert strategy.expression_form == "split-old-vs-new"


def test_creative_strategy_text_is_canonical_when_provided() -> None:
    strategy = CreativeStrategy(
        category_default="  better physical keyboard  ",
        deleted_constraint="  physical keyboard  ",
        new_competition_axis="  direct touch interaction  ",
        bridge_type="action-motion",
        bridge="  the promoted product becomes the action itself  ",
        expression_form="split-old-vs-new",
    )

    assert strategy.category_default == "better physical keyboard"
    assert strategy.deleted_constraint == "physical keyboard"
    assert strategy.new_competition_axis == "direct touch interaction"
    assert strategy.bridge == "the promoted product becomes the action itself"


def test_creative_strategy_rejects_blank_text_when_provided() -> None:
    for field_name in (
        "category_default",
        "deleted_constraint",
        "new_competition_axis",
        "bridge",
    ):
        values = {
            "category_default": None,
            "deleted_constraint": None,
            "new_competition_axis": None,
            "bridge": None,
            "expression_form": "single-visual-metaphor",
        }
        values[field_name] = "   "
        try:
            CreativeStrategy(**values)
        except ValueError:
            continue
        raise AssertionError(f"whitespace-only {field_name} must be rejected when provided")


def test_constraint_deletion_wins_over_narrative_format() -> None:
    signals = CreativeSignals(
        has_deleted_constraint=True,
        has_narrative_conflict=True,
        is_cinematic=True,
    )

    assert select_expression_form(signals) == "split-old-vs-new"


def test_swipe_reveal_is_selected_for_delayed_product_reveal() -> None:
    signals = CreativeSignals(needs_reveal_sequence=True)

    assert select_expression_form(signals) == "swipe-reveal"


def test_product_as_prop_is_selected_for_embodied_action_bridge() -> None:
    signals = CreativeSignals(
        product_embodies_bridge=True,
        bridge_type="action-motion",
    )

    assert select_expression_form(signals) == "product-as-prop"


def test_cinematic_single_moment_uses_faux_film_still() -> None:
    signals = CreativeSignals(is_cinematic=True)

    assert select_expression_form(signals) == "faux-film-still"


def test_narrative_conflict_uses_four_panel_when_no_stronger_signal() -> None:
    signals = CreativeSignals(has_narrative_conflict=True)

    assert select_expression_form(signals) == "four-panel"


def test_default_is_single_visual_metaphor() -> None:
    assert select_expression_form(CreativeSignals()) == "single-visual-metaphor"


def test_best_bridge_prefers_product_specific_visual_link() -> None:
    generic = BridgeCandidate(
        bridge_type="role",
        bridge="the product is the hero",
        product_specificity=0.25,
        hotspot_fit=0.8,
        visual_clarity=0.8,
        surprise=0.2,
    )
    embodied = BridgeCandidate(
        bridge_type="shape-material",
        bridge="the product material becomes the hotspot's signature visual action",
        product_specificity=0.95,
        hotspot_fit=0.9,
        visual_clarity=0.95,
        surprise=0.85,
    )

    selected = select_best_bridge([generic, embodied])

    assert selected is embodied
    assert selected.score > generic.score


def test_strategy_builder_combines_reframe_bridge_and_format_selection() -> None:
    candidates = [
        BridgeCandidate(
            bridge_type="role",
            bridge="the brand plays a generic guide",
            product_specificity=0.3,
            hotspot_fit=0.7,
            visual_clarity=0.7,
            surprise=0.2,
        ),
        BridgeCandidate(
            bridge_type="action-motion",
            bridge="the product's real use action becomes the hotspot action",
            product_specificity=0.9,
            hotspot_fit=0.9,
            visual_clarity=0.9,
            surprise=0.8,
        ),
    ]

    strategy = build_creative_strategy(
        category_default="make the old interface prettier",
        deleted_constraint="the extra interface layer",
        new_competition_axis="direct intent-to-result flow",
        bridge_candidates=candidates,
        signals=CreativeSignals(has_deleted_constraint=True, has_narrative_conflict=True),
    )

    assert strategy.expression_form == "split-old-vs-new"
    assert strategy.bridge_type == "action-motion"
    assert strategy.bridge == "the product's real use action becomes the hotspot action"


def test_visual_medium_router_prefers_hotspot_medium_over_product_category() -> None:
    assert select_visual_medium(tags=["film", "adventure"], subject_category="food") == (
        "live-action-cinematic"
    )
    assert select_visual_medium(tags=["animation", "3d"], subject_category="software") == "animation-3d"
    assert select_visual_medium(tags=["social", "creator"], subject_category="fashion") == (
        "documentary-social"
    )


def test_visual_medium_router_uses_product_medium_when_hotspot_is_neutral() -> None:
    assert select_visual_medium(tags=["culture"], subject_category="food") == "commercial-product"
    assert select_visual_medium(tags=["technology"], subject_category="software") == "technology-realism"


def test_creative_review_rejects_hot_character_plus_logo_even_when_recognizable() -> None:
    review = CreativeReview(
        name="hot character plus logo",
        instant_comprehension=0.95,
        natural_linkage=0.25,
        product_centrality=0.2,
        surprise=0.2,
        ownability=0.15,
        evidence_safety=0.9,
        original_execution=0.4,
    )

    assert review.passes is False


def test_creative_review_accepts_specific_surprising_original_bridge() -> None:
    review = CreativeReview(
        name="product material becomes the cultural action",
        instant_comprehension=0.9,
        natural_linkage=0.95,
        product_centrality=0.95,
        surprise=0.85,
        ownability=0.9,
        evidence_safety=0.9,
        original_execution=0.9,
    )

    assert review.passes is True
    assert review.total >= 0.85


def test_creative_review_name_is_canonical() -> None:
    review = CreativeReview(
        name="  product material becomes the cultural action  ",
        instant_comprehension=0.9,
        natural_linkage=0.95,
        product_centrality=0.95,
        surprise=0.85,
        ownability=0.9,
        evidence_safety=0.9,
        original_execution=0.9,
    )

    assert review.name == "product material becomes the cultural action"


def test_creative_review_rejects_blank_name() -> None:
    try:
        CreativeReview(
            name="   ",
            instant_comprehension=0.9,
            natural_linkage=0.95,
            product_centrality=0.95,
            surprise=0.85,
            ownability=0.9,
            evidence_safety=0.9,
            original_execution=0.9,
        )
    except ValueError:
        return
    raise AssertionError("whitespace-only creative review names must be rejected")


def test_best_review_prefers_passing_ownable_direction() -> None:
    generic = CreativeReview(
        name="generic comparison",
        instant_comprehension=0.85,
        natural_linkage=0.6,
        product_centrality=0.5,
        surprise=0.35,
        ownability=0.35,
        evidence_safety=0.9,
        original_execution=0.7,
    )
    ownable = CreativeReview(
        name="ownable metaphor",
        instant_comprehension=0.9,
        natural_linkage=0.9,
        product_centrality=0.95,
        surprise=0.85,
        ownability=0.95,
        evidence_safety=0.9,
        original_execution=0.9,
    )

    assert select_best_review([generic, ownable]) is ownable
