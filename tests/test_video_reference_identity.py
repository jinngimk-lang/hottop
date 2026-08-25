from pathlib import Path

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config
from hottop.video_reference import VideoReference, validate_reference_identity_consistency


def test_video_reference_carries_character_identity_anchor():
    reference = VideoReference(
        image_path="assets/generated-original/hero.png",
        rights="generated-original",
        subject_id=" hero ",
        role=" returning sailor hero ",
        identity_lock=["weathered face", "dark curly hair", "bronze cloak"],
    )

    assert reference.subject_id == "hero"
    assert reference.role == "returning sailor hero"
    assert reference.identity_lock == ["weathered face", "dark curly hair", "bronze cloak"]


def test_reference_identity_rejects_same_subject_with_conflicting_anchor():
    references = [
        VideoReference(
            image_path="assets/generated-original/hero-a.png",
            rights="generated-original",
            subject_id="hero",
            identity_lock=["dark curly hair"],
        ),
        VideoReference(
            image_path="assets/generated-original/hero-b.png",
            rights="generated-original",
            subject_id="hero",
            identity_lock=["dark curly hair"],
        ),
    ]

    with pytest.raises(ValueError, match="conflicting reference image"):
        validate_reference_identity_consistency(references)


def test_reference_identity_rejects_same_subject_with_conflicting_lock():
    references = [
        VideoReference(
            image_path="assets/generated-original/hero.png",
            rights="generated-original",
            subject_id="hero",
            identity_lock=["dark curly hair", "bronze cloak"],
        ),
        VideoReference(
            image_path="assets/generated-original/hero.png",
            rights="generated-original",
            subject_id="hero",
            identity_lock=["blond hair", "white cloak"],
        ),
    ]

    with pytest.raises(ValueError, match="conflicting identity lock"):
        validate_reference_identity_consistency(references)


def test_video_plan_rejects_conflicting_identity_before_generation_commands():
    config = load_video_production_config(Path("config/video/cinematic-zero-cost.yml"))
    request = CreativeRenderRequest(
        topic_id="identity-conflict",
        topic_title="identity conflict",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic mythic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The hero enters.",
                intent="setup",
                reference=VideoReference(
                    image_path="assets/generated-original/hero-a.png",
                    rights="generated-original",
                    subject_id="hero",
                    identity_lock=["dark curly hair"],
                ),
            ),
            CreativeRenderFrame(
                index=2,
                scene="The hero returns.",
                intent="payoff",
                reference=VideoReference(
                    image_path="assets/generated-original/hero-b.png",
                    rights="generated-original",
                    subject_id="hero",
                    identity_lock=["dark curly hair"],
                ),
            ),
        ],
        master_prompt="original cinematic mythic world",
        negative_prompt="actor likeness, copied film frame",
        punchlines=["done"],
        claim_status="satire",
    )

    with pytest.raises(ValueError, match="conflicting reference image"):
        build_video_production_plan(request, config)


def test_video_plan_adds_identity_lock_to_generation_prompt():
    config = load_video_production_config(Path("config/video/cinematic-zero-cost.yml"))
    reference = VideoReference(
        image_path="assets/generated-original/hero.png",
        rights="generated-original",
        subject_id="hero",
        role="returning sailor hero",
        identity_lock=["weathered face", "dark curly hair", "bronze cloak"],
    )
    request = CreativeRenderRequest(
        topic_id="identity-anchor",
        topic_title="original mythic coding meme",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic mythic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The hero enters the banquet hall.",
                caption="我来。",
                intent="hero entrance",
                speaker="hero",
                delivery="dry",
                reference=reference,
            ),
            CreativeRenderFrame(
                index=2,
                scene="The same hero opens the tool and breaks the curse.",
                caption="先把活干完。",
                intent="payoff",
                speaker="hero",
                delivery="calm",
                reference=reference,
            ),
        ],
        master_prompt="original cinematic mythic world",
        negative_prompt="actor likeness, copied film frame",
        punchlines=["先把活干完。"],
        claim_status="satire",
    )

    plan = build_video_production_plan(request, config)

    assert all("Identity anchor hero" in shot.generation_prompt for shot in plan.shots)
    assert all("weathered face" in shot.generation_prompt for shot in plan.shots)
    assert all("returning sailor hero" in shot.generation_prompt for shot in plan.shots)
