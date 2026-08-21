from hottop.models import ComparisonCandidate, ProductProfile
from hottop.positioning import (
    build_comparison_research_queries,
    choose_comparison_target,
    infer_promotion_context,
)


def test_product_profile_can_describe_non_ai_brand_or_product():
    profile = ProductProfile(
        name="Example Running Shoe",
        subject_type="product",
        category="running shoes",
        keywords=["marathon", "daily trainer"],
        jobs_to_be_done=["comfortable long runs"],
        pain_points_solved=["heavy shoes on long runs"],
        differentiators=["lightweight cushioning"],
    )

    assert profile.subject_type == "product"
    assert profile.category == "running shoes"
    assert "comfortable long runs" in profile.jobs_to_be_done


def test_infer_promotion_context_uses_profile_semantics_not_ai_assumptions():
    profile = ProductProfile(
        name="Example Coffee",
        subject_type="brand",
        category="ready-to-drink coffee",
        pain_points_solved=["no time to brew coffee"],
        differentiators=["ready immediately"],
    )

    context = infer_promotion_context(profile)

    assert context.category == "ready-to-drink coffee"
    assert context.primary_pain_point == "no time to brew coffee"
    assert context.primary_differentiator == "ready immediately"


def test_comparison_research_queries_cover_direct_competitors_and_substitutes():
    profile = ProductProfile(
        name="Example Coffee",
        subject_type="brand",
        category="ready-to-drink coffee",
        jobs_to_be_done=["quick caffeine before commuting"],
        pain_points_solved=["no time to brew coffee"],
    )

    queries = build_comparison_research_queries(profile)

    assert '"Example Coffee" competitors' in queries
    assert '"Example Coffee" alternatives' in queries
    assert "best ready-to-drink coffee for quick caffeine before commuting" in queries
    assert "no time to brew coffee alternatives" in queries


def test_choose_comparison_target_prefers_recognizable_high_overlap_candidate():
    profile = ProductProfile(
        name="Example Coffee",
        subject_type="brand",
        category="ready-to-drink coffee",
        jobs_to_be_done=["quick caffeine before commuting"],
    )
    candidates = [
        ComparisonCandidate(
            name="Generic Energy Drink",
            category="energy drinks",
            relation="adjacent-substitute",
            recognizability=0.8,
            category_overlap=0.4,
            evidence_quality=0.8,
        ),
        ComparisonCandidate(
            name="Popular Bottled Coffee",
            category="ready-to-drink coffee",
            relation="direct-competitor",
            recognizability=0.9,
            category_overlap=1.0,
            evidence_quality=0.9,
        ),
    ]

    chosen = choose_comparison_target(profile, candidates)

    assert chosen is not None
    assert chosen.name == "Popular Bottled Coffee"


def test_comparison_target_without_evidence_is_still_only_a_satirical_target():
    profile = ProductProfile(name="Example Product", category="consumer product")
    candidate = ComparisonCandidate(
        name="Known Alternative",
        category="consumer product",
        relation="direct-competitor",
        recognizability=0.9,
        category_overlap=1.0,
    )

    chosen = choose_comparison_target(profile, [candidate])

    assert chosen is not None
    assert chosen.claim_posture == "satire"
