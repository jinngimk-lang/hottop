import pytest

from hottop.mapping import build_role_map
from hottop.mechanism import HotspotMechanism, ProductMechanismMapping
from hottop.models import ProductProfile, TrendCandidate


def _candidate() -> TrendCandidate:
    return TrendCandidate(
        id="topic:1",
        title="A supplied cultural scene",
        url="https://example.com/topic",
        source="news",
    )


def _mapping() -> ProductMechanismMapping:
    return ProductMechanismMapping(
        mechanism=HotspotMechanism(
            topic_id="topic:1",
            source_mode="user-supplied",
            recognition_hook="a huge obstacle traps everyone until the rules of the situation are changed",
            causal_chain=["group enters", "obstacle blocks exit", "a new route breaks the trap"],
            native_visual_grammar="large physical obstruction with tiny trapped figures",
            native_dialogue_grammar="short setup, escalating frustration, abrupt practical reversal",
        ),
        promoted_product="InkClawAgent",
        product_role="the route that bypasses the obstruction",
        product_bridge="remove the workflow assumption that everyone must pass through the same blocker",
        outcome_before="the group is trapped behind the blocker",
        outcome_after="the group exits without fighting the blocker on its terms",
        punchline="别跟堵口的东西耗，换条路。",
        comparison_target="old workflow",
        comparison_role="the obstruction that blocks the exit",
    )


def test_role_map_uses_explicit_mechanism_role_instead_of_keyword_archetype() -> None:
    role_map = build_role_map(
        _candidate(),
        ProductProfile(name="InkClawAgent"),
        mechanism_mapping=_mapping(),
    )

    assert role_map.promoted_product == "InkClawAgent"
    assert role_map.product_role == "the route that bypasses the obstruction"
    assert role_map.comparison_target == "old workflow"
    assert role_map.comparison_role == "the obstruction that blocks the exit"
    assert role_map.archetype == "mechanism-driven"
    assert "group enters" in role_map.conflict


def test_role_map_rejects_mismatched_topic_or_product() -> None:
    wrong_topic = _mapping().model_copy(deep=True)
    wrong_topic.mechanism.topic_id = "different"
    with pytest.raises(ValueError, match="topic id must match"):
        build_role_map(
            _candidate(),
            ProductProfile(name="InkClawAgent"),
            mechanism_mapping=wrong_topic,
        )

    wrong_product = _mapping().model_copy(update={"promoted_product": "OtherProduct"})
    with pytest.raises(ValueError, match="promoted product must match"):
        build_role_map(
            _candidate(),
            ProductProfile(name="InkClawAgent"),
            mechanism_mapping=wrong_product,
        )
