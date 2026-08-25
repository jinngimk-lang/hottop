from __future__ import annotations

from .models import ProductProfile, RoleMap, TrendCandidate


def _text(candidate: TrendCandidate) -> str:
    return f"{candidate.title} {candidate.summary or ''}".lower()


def infer_archetype(candidate: TrendCandidate) -> str:
    text = _text(candidate)
    if any(token in text for token in ("cyclops", "独眼", "monster", "怪物", "cave", "山洞")):
        return "monster-vs-clever-hero"
    if any(token in text for token in ("maze", "迷宫", "labyrinth")):
        return "maze-vs-guide"
    if any(token in text for token in ("siege", "围城", "城门", "fortress")):
        return "siege-vs-breaker"
    if any(token in text for token in ("team", "团队", "overload", "忙不过来")):
        return "overloaded-team-vs-orchestrator"
    if any(token in text for token in ("manual", "手动", "重复", "slow", "慢")):
        return "slow-manual-process-vs-automation"
    if any(token in text for token in ("tool", "工具", "fragment", "碎片", "多个应用")):
        return "fragmented-tools-vs-coordinator"
    return "gatekeeper-vs-bypass"


_ARCHETYPE_ROLES = {
    "monster-vs-clever-hero": ("clever hero", "monster obstacle"),
    "maze-vs-guide": ("solver", "maze obstacle"),
    "siege-vs-breaker": ("breaker", "gatekeeping obstacle"),
    "overloaded-team-vs-orchestrator": ("solver", "overload obstacle"),
    "slow-manual-process-vs-automation": ("solver", "manual-process obstacle"),
    "fragmented-tools-vs-coordinator": ("solver", "fragmentation obstacle"),
    "gatekeeper-vs-bypass": ("breaker", "gatekeeping obstacle"),
}


def build_role_map(
    candidate: TrendCandidate,
    product: ProductProfile,
    comparison_target: str | None = None,
) -> RoleMap:
    archetype = infer_archetype(candidate)
    product_role, comparison_role = _ARCHETYPE_ROLES[archetype]
    return RoleMap(
        topic_world=candidate.title,
        conflict=f"{candidate.title}: recognizable obstacle versus a smarter way through",
        promoted_product=product.name,
        product_role=product_role,
        comparison_target=comparison_target,
        comparison_role=comparison_role if comparison_target else None,
        archetype=archetype,
        why_it_maps=(
            f"Use the topic's {archetype} conflict as a metaphor: {product.name} becomes the "
            "decisive way through the problem while the comparison target, if present, represents friction."
        ),
    )
