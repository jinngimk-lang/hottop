from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config


def _motion_render_request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="trend-niulai",
        topic_title="rough 3D absurd comedy",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="intentionally cheap 3D absurdist comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="starting an agent feels like an ops project",
        deleted_constraint="remove deployment ceremony before useful work",
        new_competition_axis="time to first useful work",
        bridge_type="role",
        bridge="a deadpan family comedy treats dependency friction as a literal nuisance",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The rough 3D cow codes in one messy workshop while a snake crawls under the desk.",
                caption="本来只想做个 Agent…",
                intent="setup and obstruction",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The cow recoils and calls for its mother; camera follows its eyeline to the doorway.",
                caption="妈——！",
                intent="reaction and continuous eyeline transition",
            ),
            CreativeRenderFrame(
                index=3,
                scene="The mother enters the same workshop, points to the laptop and solves the blockage.",
                caption="傻孩子，用 InkClawAgent。",
                intent="deadpan solution and payoff",
            ),
            CreativeRenderFrame(
                index=4,
                scene="The obstruction disappears; the cow works while the snake retreats through foreground.",
                caption="打开，直接干活",
                intent="benefit as visible consequence",
            ),
        ],
        master_prompt="original rough low-budget 3D animation, awkward but controlled comedy",
        negative_prompt="glossy AI ad, blue-purple hologram, unrelated slideshow stills, copied film frames",
        punchlines=["别被蛇绊住。"],
        risk_flags=["do not copy protected character design or exact film frame"],
        claim_status="satire",
    )


def test_anti_polish_profile_builds_complete_motion_plan():
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))
    plan = build_video_production_plan(_motion_render_request(), config)

    assert plan.schema_version == "hottop.video-plan.v1"
    assert plan.style_profile == "anti-polish"
    assert (plan.width, plan.height, plan.fps) == (720, 1280, 24)
    assert plan.generation_backend == "wan22-ti2v-5b"
    assert plan.compositor_backend == "motion-canvas"
    assert plan.encoder_backend == "ffmpeg"
    assert len(plan.shots) == 4
    assert plan.shots[0].start_seconds == 0
    assert plan.shots[-1].end_seconds <= config.duration_seconds
    assert all(shot.continuity_instruction for shot in plan.shots)
    assert any(cue.kind == "dialogue" for cue in plan.audio_cues)
    assert any(cue.kind == "foley" for cue in plan.audio_cues)
    assert any(cue.kind == "bgm" for cue in plan.audio_cues)
    assert plan.in_asset_cta_policy == "no-destination"
    assert "generate.py" in " ".join(plan.generation_commands)
    assert "Motion Canvas" in " ".join(plan.execution_notes)
    final_command = " ".join(plan.finalization_command)
    assert "libx264" in final_command
    assert "yuv420p" in final_command
    assert "+faststart" in final_command


def test_anti_polish_prompt_keeps_badness_controlled_not_broken():
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))
    plan = build_video_production_plan(_motion_render_request(), config)

    prompt = plan.shots[0].generation_prompt.lower()
    assert "rough" in prompt or "cheap" in prompt
    assert "character continuity" in " ".join(plan.execution_notes).lower()
    assert "subtitle correctness" in " ".join(plan.execution_notes).lower()
    assert "glossy ai ad" in plan.shots[0].negative_prompt.lower()
