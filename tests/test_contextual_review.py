from hottop.creative import (
    CreativeContextReview,
    CreativeReview,
    review_with_context,
    select_best_contextual_review,
)


def _base(name: str, *, ownability: float = 0.9) -> CreativeReview:
    return CreativeReview(
        name=name,
        instant_comprehension=0.9,
        natural_linkage=0.9,
        product_centrality=0.9,
        surprise=0.8,
        ownability=ownability,
        evidence_safety=0.9,
        original_execution=0.9,
    )


def test_context_never_rescues_a_base_review_that_fails_hard_gate():
    base = _base("generic", ownability=0.3)
    context = CreativeContextReview(
        platform_fit=1.0,
        style_fit=1.0,
        campaign_goal_fit=1.0,
        ambition_fit=1.0,
        project_shape_fit=1.0,
        hotspot_native_fit=1.0,
        humor_or_delight=1.0,
        humor_expected=True,
    )

    result = review_with_context(base, context)

    assert base.passes is False
    assert result.passes is False


def test_contextual_scores_rank_passing_concepts_for_the_current_request():
    first = review_with_context(
        _base("platform-native"),
        CreativeContextReview(
            platform_fit=0.95,
            style_fit=0.92,
            campaign_goal_fit=0.9,
            ambition_fit=0.9,
            project_shape_fit=0.95,
            hotspot_native_fit=0.94,
            humor_or_delight=0.88,
            humor_expected=True,
        ),
    )
    second = review_with_context(
        _base("generic"),
        CreativeContextReview(
            platform_fit=0.55,
            style_fit=0.55,
            campaign_goal_fit=0.7,
            ambition_fit=0.6,
            project_shape_fit=0.6,
            hotspot_native_fit=0.55,
            humor_or_delight=0.45,
            humor_expected=True,
        ),
    )

    selected = select_best_contextual_review([second, first])

    assert first.passes is True
    assert second.passes is True
    assert first.total > second.total
    assert selected.base.name == "platform-native"


def test_humor_score_is_neutral_when_humor_is_not_expected():
    low_humor = review_with_context(
        _base("premium"),
        CreativeContextReview(
            platform_fit=0.9,
            style_fit=0.9,
            campaign_goal_fit=0.9,
            ambition_fit=0.9,
            project_shape_fit=0.9,
            hotspot_native_fit=0.9,
            humor_or_delight=0.0,
            humor_expected=False,
        ),
    )
    high_humor = review_with_context(
        _base("premium-2"),
        CreativeContextReview(
            platform_fit=0.9,
            style_fit=0.9,
            campaign_goal_fit=0.9,
            ambition_fit=0.9,
            project_shape_fit=0.9,
            hotspot_native_fit=0.9,
            humor_or_delight=1.0,
            humor_expected=False,
        ),
    )

    assert low_humor.context_total == high_humor.context_total
