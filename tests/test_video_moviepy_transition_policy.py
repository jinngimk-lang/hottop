from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_moviepy import build_moviepy_timeline
from hottop.video_production import build_video_production_plan, load_video_production_config


def _software3d_plan():
    request = CreativeRenderRequest(
        topic_id="odyssey-transition-contract",
        topic_title="cinematic software3d transition contract",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="cinematic-low-poly",
        genre_treatment="cinematic mythic software 3D",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="operator turns ritual into immediate action",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The witch reaches toward the same workstation.",
                caption="就差一点。",
                intent="setup",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The same workstation and witch continue without a spatial reset.",
                caption="先配环境。",
                intent="escalation",
            ),
            CreativeRenderFrame(
                index=3,
                scene="The same geography continues as the setup burden grows.",
                caption="怎么越写越大？",
                intent="reaction",
            ),
        ],
        master_prompt="original cinematic low-poly continuous action",
        negative_prompt="slideshow hard cuts",
        punchlines=["直接干活。"],
        risk_flags=[],
        claim_status="satire",
    )
    config = load_video_production_config(Path("config/video/cinematic-software3d.yml"))
    return build_video_production_plan(request, config)


def test_software3d_moviepy_timeline_uses_short_boundary_fades(tmp_path):
    timeline = build_moviepy_timeline(_software3d_plan(), shots_dir=tmp_path / "shots")

    max_transition = 2 / timeline.fps
    assert timeline.shots[0].fade_in_seconds == 0
    assert 0 < timeline.shots[0].fade_out_seconds <= max_transition
    assert 0 < timeline.shots[1].fade_in_seconds <= max_transition
    assert 0 < timeline.shots[1].fade_out_seconds <= max_transition
    assert 0 < timeline.shots[2].fade_in_seconds <= max_transition
    assert timeline.shots[2].fade_out_seconds == 0

    for shot in timeline.shots:
        assert shot.fade_in_seconds + shot.fade_out_seconds < shot.duration_seconds
