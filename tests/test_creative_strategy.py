from hottop.creative import (
    BridgeCandidate,
    CreativeSignals,
    select_best_bridge,
    select_expression_form,
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
