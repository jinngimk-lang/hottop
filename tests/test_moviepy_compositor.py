from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_moviepy import build_moviepy_timeline
from hottop.video_production import build_video_production_plan, load_video_production_config


def _plan():
    request = CreativeRenderRequest(
        topic_id="cow-snake",
        topic_title="anti-polish story",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="cheap rough 3D absurd comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="snake as workflow obstruction",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Cow encounters a snake in one workshop.",
                caption="妈——！",
                intent="reaction",
            ),
            CreativeRenderFrame(
                index=2,
                scene="Mother cow enters the same workshop.",
                caption="傻孩子，用 InkClawAgent。",
                intent="solution",
            ),
        ],
        master_prompt="original rough 3D",
        negative_prompt="glossy ad",
        punchlines=["别被蛇绊住。"],
        risk_flags=[],
        claim_status="satire",
    )
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    return build_video_production_plan(request, config)


def test_moviepy_timeline_maps_shots_and_dialogue_without_importing_renderer(tmp_path):
    timeline = build_moviepy_timeline(_plan(), shots_dir=tmp_path / "shots")

    assert [Path(item.source).name for item in timeline.shots] == [
        "shot-001.mp4",
        "shot-002.mp4",
    ]
    assert timeline.shots[0].start_seconds == 0
    assert timeline.shots[1].start_seconds > timeline.shots[0].start_seconds
    assert [caption.text for caption in timeline.captions] == [
        "妈——！",
        "傻孩子，用 InkClawAgent。",
    ]
    assert timeline.bgm_description
    assert timeline.generate_synthetic_bgm is True
