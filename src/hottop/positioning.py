from __future__ import annotations

from .models import ComparisonCandidate, ProductProfile, PromotionContext


def infer_promotion_context(profile: ProductProfile) -> PromotionContext:
    category = (profile.category or profile.subject_type.replace("-", " ")).strip()
    semantic_terms: list[str] = []
    for value in [
        *profile.keywords,
        *profile.jobs_to_be_done,
        *profile.pain_points_solved,
        *profile.differentiators,
        *profile.strengths,
    ]:
        normalized = value.strip()
        if normalized and normalized not in semantic_terms:
            semantic_terms.append(normalized)

    return PromotionContext(
        subject_name=profile.name,
        subject_type=profile.subject_type,
        category=category or "product",
        primary_job=profile.jobs_to_be_done[0] if profile.jobs_to_be_done else None,
        primary_pain_point=profile.pain_points_solved[0] if profile.pain_points_solved else None,
        primary_differentiator=profile.differentiators[0] if profile.differentiators else None,
        semantic_terms=semantic_terms,
    )


def build_comparison_research_queries(profile: ProductProfile) -> list[str]:
    """Build web-research queries for direct competitors and practical substitutes.

    The function deliberately emits queries rather than hard-coded competitor names. The research
    layer can resolve current brands/products from fresh public sources, then feed those candidates
    back into the deterministic selector below.
    """

    context = infer_promotion_context(profile)
    queries = [
        f'"{profile.name}" competitors',
        f'"{profile.name}" alternatives',
    ]
    if context.primary_job:
        queries.append(f"best {context.category} for {context.primary_job}")
    else:
        queries.append(f"best {context.category} alternatives")
    if context.primary_pain_point:
        queries.append(f"{context.primary_pain_point} alternatives")
    for alternative in profile.known_alternatives[:3]:
        queries.append(f'"{profile.name}" vs "{alternative}"')

    return list(dict.fromkeys(query for query in queries if query.strip()))


def _candidate_score(profile: ProductProfile, candidate: ComparisonCandidate) -> float:
    relation_weight = {
        "direct-competitor": 1.0,
        "incumbent-default": 0.9,
        "adjacent-substitute": 0.8,
        "legacy-workflow": 0.75,
        "manual-workaround": 0.7,
    }[candidate.relation]

    known_bonus = 0.1 if candidate.name in profile.known_alternatives else 0.0
    evidence_bonus = 0.05 if candidate.evidence else 0.0
    return (
        0.30 * candidate.recognizability
        + 0.30 * candidate.category_overlap
        + 0.20 * candidate.pain_point_contrast
        + 0.10 * candidate.evidence_quality
        + 0.10 * relation_weight
        + known_bonus
        + evidence_bonus
    )


def choose_comparison_target(
    profile: ProductProfile,
    candidates: list[ComparisonCandidate],
) -> ComparisonCandidate | None:
    """Choose the comparison that creates the clearest, safest meme contrast.

    Selection rewards recognizability, same-category overlap and pain-point contrast. It does not
    infer factual weaknesses. A candidate stays `satire` unless the research layer explicitly
    supplies evidence and marks the comparison `supported`.
    """

    if not candidates:
        return None

    eligible = [candidate for candidate in candidates if candidate.name != profile.name]
    if not eligible:
        return None

    chosen = max(eligible, key=lambda candidate: _candidate_score(profile, candidate))
    if not chosen.evidence and chosen.claim_posture == "supported":
        chosen = chosen.model_copy(update={"claim_posture": "satire"})
    return chosen
