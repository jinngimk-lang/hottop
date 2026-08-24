from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="odyssey-witch-pigs",
        topic_title="mythic witch rescue meme",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="mythic Mediterranean cinematic comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="a transformation curse literalizes workflow friction",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="An original mythic banquet hall with sailors coding at a feast.",
                caption="这需求再改一下就行……",
                intent="setup",
            )
        ],
        master_prompt="original cinematic mythic scene, consistent cast, dramatic practical light",
        negative_prompt="actor likeness, copied film frame, official character design",
        punchlines=["先把活干完，再谈史诗。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def test_roughness_is_style_sensitive_instead_of_universal():
    anti = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    cinematic = load_video_production_config(Path("config/video/cinematic-meme-direct.yml"))

    assert anti.roughness_score == 78
    assert cinematic.roughness_score == 28
    assert anti.style_profile == "anti-polish"
    assert cinematic.style_profile == "cinematic"
    assert cinematic.anti_polish.enabled is False

    anti_plan = build_video_production_plan(_request(), anti)
    cinematic_plan = build_video_production_plan(_request(), cinematic)
    assert anti_plan.roughness_score == 78
    assert cinematic_plan.roughness_score == 28
    assert "rough cheap low-budget" in anti_plan.shots[0].generation_prompt.lower()
    assert "controlled cinematic polish" in cinematic_plan.shots[0].generation_prompt.lower()
    assert "rough cheap low-budget" not in cinematic_plan.shots[0].generation_prompt.lower()


def test_cinematic_meme_profile_routes_audio_for_mythic_film_style():
    config = load_video_production_config(Path("config/video/cinematic-meme-direct.yml"))
    plan = build_video_production_plan(_request(), config)

    assert plan.audio_profile is not None
    assert plan.audio_profile.voice_profile == "natural-mandarin-cinematic"
    assert plan.audio_profile.music_profile == "mythic-dark-comedy-original"
    assert plan.audio_profile.sfx_profile == "cinematic-mythic-foley"
    assert plan.audio_profile.original_music_only is True
    assert plan.compositor_backend == "moviepy"
    assert plan.encoder_backend == "ffmpeg"
