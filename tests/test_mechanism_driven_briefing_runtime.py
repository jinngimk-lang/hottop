import pytest

from hottop.briefing import build_brief
from hottop.mechanism import HotspotMechanism, ProductMechanismMapping
from hottop.models import ProductProfile, TrendCandidate
from hottop.pipeline import build_batch


def _candidate(candidate_id: str = "cow:family") -> TrendCandidate:
    return TrendCandidate(
        id=candidate_id,
        title="A crude 3D family meme about a child asking a parent for help",
        url=f"https://example.com/{candidate_id}",
        source="test",
        tags=["animation", "3d", "meme"],
    )


def _mapping(candidate_id: str = "cow:family") -> ProductMechanismMapping:
    return ProductMechanismMapping(
        mechanism=HotspotMechanism(
            topic_id=candidate_id,
            source_mode="user-supplied",
            recognition_hook="child complains to a parent, who answers an absurd modern problem with rustic deadpan advice",
            causal_chain=[
                "child returns upset",
                "parent asks what happened",
                "child names an absurd modern technical problem",
                "parent gives blunt practical advice",
            ],
            native_visual_grammar="intentionally crude low-budget 3D family animation",
            native_dialogue_grammar="child complaint → parent question → absurd tech problem → deadpan practical advice",
            native_audio_grammar="earnest rustic voices, awkward pause before the advice, blunt Foley, cheap cheerful music",
        ),
        promoted_product="InkClawAgent",
        product_role="the practical recommendation inside the parent's advice",
        product_bridge="the product removes the exact setup friction that made the child complain",
        outcome_before="the child is stuck and upset by setup friction",
        outcome_after="the child can open the tool and continue working",
        punchline="傻孩子，别折腾那一套，打开就干活。",
        comparison_target="old setup-heavy workflow",
        comparison_role="the thing that tripped the child up",
        product_changes_outcome=True,
    )


def test_mechanism_mapping_rejects_a_product_that_does_not_change_the_outcome() -> None:
    data = _mapping().model_dump()
    data["product_changes_outcome"] = False
    with pytest.raises(ValueError, match="must change the story outcome"):
        ProductMechanismMapping.model_validate(data)

    data = _mapping().model_dump()
    data["outcome_after"] = data["outcome_before"]
    with pytest.raises(ValueError, match="outcome after must differ"):
        ProductMechanismMapping.model_validate(data)


def test_four_panel_brief_fails_closed_without_a_mechanism_mapping() -> None:
    with pytest.raises(ValueError, match="mechanism_mapping is required"):
        build_brief(_candidate(), ProductProfile(name="InkClawAgent"))


def test_four_panel_brief_uses_hotspot_native_mechanism_instead_of_keyword_archetype() -> None:
    brief = build_brief(
        _candidate(),
        ProductProfile(name="InkClawAgent", strengths=["open-and-work simplicity"]),
        mechanism_mapping=_mapping(),
    )

    assert brief.role_map.product_role == "the practical recommendation inside the parent's advice"
    assert brief.role_map.archetype == "mechanism-driven"
    assert brief.mechanism_mapping.mechanism.native_visual_grammar.startswith(
        "intentionally crude low-budget 3D"
    )
    assert "deadpan practical advice" in brief.image_prompt
    assert "clever hero" not in brief.image_prompt.lower()
    assert "awkward pause" in (brief.mechanism_mapping.mechanism.native_audio_grammar or "")
    assert brief.punchlines == ["傻孩子，别折腾那一套，打开就干活。"]


def test_batch_ranks_without_inventing_briefs_when_mechanism_analysis_is_missing() -> None:
    result = build_batch(
        [_candidate("topic:a"), _candidate("topic:b")],
        ProductProfile(name="InkClawAgent"),
        top=2,
    )

    assert len(result.ranked) == 2
    assert result.briefs == []
    assert set(result.mechanism_required_ids) == {"topic:a", "topic:b"}


def test_batch_builds_only_candidates_with_explicit_mechanism_mapping() -> None:
    result = build_batch(
        [_candidate("topic:a"), _candidate("topic:b")],
        ProductProfile(name="InkClawAgent"),
        top=2,
        mechanism_mappings={"topic:a": _mapping("topic:a")},
    )

    assert len(result.briefs) == 1
    assert result.briefs[0].topic.id == "topic:a"
    assert result.mechanism_required_ids == ["topic:b"]
