from hottop.mapping import build_role_map, infer_archetype
from hottop.models import ProductProfile, TrendCandidate


def _candidate(title: str, summary: str | None = None) -> TrendCandidate:
    return TrendCandidate(
        id="topic:1",
        title=title,
        summary=summary,
        url="https://example.com/topic",
        source="news",
    )


def test_cyclops_cave_topic_maps_to_monster_vs_clever_hero():
    candidate = _candidate("Odyssey cyclops cave confrontation")
    assert infer_archetype(candidate) == "monster-vs-clever-hero"


def test_role_map_promotes_product_as_solver_and_comparison_as_obstacle():
    candidate = _candidate("Odyssey cyclops cave confrontation")
    product = ProductProfile(name="InkClawAgent")
    role_map = build_role_map(candidate, product, comparison_target="work巴迪")
    assert role_map.promoted_product == "InkClawAgent"
    assert role_map.product_role in {"clever hero", "solver", "breaker"}
    assert role_map.comparison_target == "work巴迪"
    assert "obstacle" in (role_map.comparison_role or "") or "monster" in (
        role_map.comparison_role or ""
    )
