from __future__ import annotations

from .mechanism import ProductMechanismMapping
from .models import ProductProfile, RoleMap, TrendCandidate


def build_role_map(
    candidate: TrendCandidate,
    product: ProductProfile,
    *,
    mechanism_mapping: ProductMechanismMapping,
    comparison_target: str | None = None,
) -> RoleMap:
    """Build a role map from explicit hotspot analysis instead of keyword archetype inference."""

    if mechanism_mapping.mechanism.topic_id != candidate.id:
        raise ValueError("mechanism mapping topic id must match the selected trend candidate")
    if mechanism_mapping.promoted_product != product.name:
        raise ValueError("mechanism mapping promoted product must match the product profile")

    mapped_comparison = mechanism_mapping.comparison_target
    if comparison_target is not None and mapped_comparison not in {None, comparison_target}:
        raise ValueError("comparison target conflicts with the mechanism mapping")
    effective_comparison = comparison_target or mapped_comparison
    comparison_role = mechanism_mapping.comparison_role if effective_comparison else None

    chain = " → ".join(mechanism_mapping.mechanism.causal_chain)
    return RoleMap(
        topic_world=candidate.title,
        conflict=chain,
        promoted_product=product.name,
        product_role=mechanism_mapping.product_role,
        comparison_target=effective_comparison,
        comparison_role=comparison_role,
        archetype="mechanism-driven",
        why_it_maps=(
            f"{mechanism_mapping.product_bridge} Outcome changes from "
            f"'{mechanism_mapping.outcome_before}' to '{mechanism_mapping.outcome_after}'."
        ),
    )
