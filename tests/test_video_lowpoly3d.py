from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_lowpoly3d import project_point, render_lowpoly_frame, render_lowpoly_shot
from hottop.video_production import VideoProductionConfig, build_video_production_plan
from hottop.video_quality import VideoQualityPolicy, inspect_video_quality


def _render_request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="software-lowpoly-flagship",
        topic_title="controlled badness workshop",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="original cheap low-poly 3D comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup friction",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="a crude workshop obstruction becomes literal workflow friction",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Original orange bovine programmer works at an old laptop in one messy workshop.",
                caption="本来只想做个 Agent…",
                intent="setup",
                speaker="cow",
                delivery="deadpan Mandarin",
            ),
            CreativeRenderFrame(
                index=2,
                scene="A generic green cable-snake tangles around the same desk while the bovine recoils.",
                caption="妈——！",
                intent="obstruction",
                speaker="cow",
                delivery="comic shout",
            ),
        ],
        master_prompt="original low-budget 3D workshop comedy",
        negative_prompt="copied film frame, protected character design, glossy AI ad",
        punchlines=["别被蛇绊住。"],
        risk_flags=["original character geometry only"],
        claim_status="satire",
    )


def _config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "software-lowpoly-test",
            "style_profile": "anti-polish",
            "roughness_score": 82,
            "generation_backend": "software-lowpoly-3d",
            "compositor_backend": "external",
            "encoder_backend": "ffmpeg",
            "width": 180,
            "height": 320,
            "fps": 8,
            "duration_seconds": 1.0,
            "shot_policy": {"min_shot_seconds": 0.5, "max_shot_seconds": 0.5},
            "audio": {
                "bgm_style": "original cheap comedy",
                "voice_backend": "none",
                "music_backend": "none",
                "sfx_backend": "none",
                "foley_style": "blunt Foley",
            },
            "text": {},
            "anti_polish": {"enabled": True, "rough_3d": True},
            "software_lowpoly": {"preset": "cow-snake-workshop-v1"},
            "ffmpeg": {
                "video_codec": "libx264",
                "audio_codec": "aac",
                "pixel_format": "yuv420p",
                "movflags": "+faststart",
            },
        }
    )


def test_perspective_projection_shrinks_equal_world_offset_with_distance():
    near = project_point((1.0, 0.0, 3.0), width=200, height=300, focal_length=1.2)
    far = project_point((1.0, 0.0, 6.0), width=200, height=300, focal_length=1.2)

    center_x = 100.0
    assert abs(far[0] - center_x) < abs(near[0] - center_x)
    assert near[2] < far[2]


def test_lowpoly_frames_are_deterministic_but_visibly_move():
    first = render_lowpoly_frame(
        preset="cow-snake-workshop-v1",
        shot_index=1,
        time_seconds=0.0,
        width=96,
        height=160,
    )
    repeated = render_lowpoly_frame(
        preset="cow-snake-workshop-v1",
        shot_index=1,
        time_seconds=0.0,
        width=96,
        height=160,
    )
    later = render_lowpoly_frame(
        preset="cow-snake-workshop-v1",
        shot_index=1,
        time_seconds=0.35,
        width=96,
        height=160,
    )

    assert first == repeated
    assert first.startswith(b"P6\n96 160\n255\n")
    assert first != later


@pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None, reason="ffmpeg required")
def test_lowpoly_shot_is_real_decodable_motion_video(tmp_path: Path):
    output = tmp_path / "shot.mp4"
    render_lowpoly_shot(
        preset="cow-snake-workshop-v1",
        shot_index=2,
        duration_seconds=1.0,
        width=180,
        height=320,
        fps=8,
        output=output,
    )

    report = inspect_video_quality(
        output,
        VideoQualityPolicy(
            min_motion_delta=0.2,
            max_duplicate_ratio=0.8,
            sample_fps=4,
            sample_width=48,
            sample_height=80,
        ),
    )
    assert report.pass_, report.reasons
    assert report.width == 180
    assert report.height == 320
    assert report.duration > 0


def test_video_plan_and_dry_run_treat_software_3d_as_zero_cost_generation(tmp_path: Path):
    config = _config()
    request = _render_request()
    plan = build_video_production_plan(request, config)

    assert plan.generation_backend == "software-lowpoly-3d"
    assert len(plan.generation_command_specs) == len(plan.shots)
    generation = plan.generation_command_specs[0]
    assert generation.args[:2] == ["-m", "hottop.video_lowpoly3d"]
    assert "cow-snake-workshop-v1" in generation.args
    assert "zero-cost deterministic software 3d" in " ".join(plan.execution_notes).lower()

    status = inspect_video_environment(config, project_root=tmp_path)
    assert status.ready is True

    run = run_video_production(
        request,
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )
    commands = [command for command in run.runtime_commands if command.stage == "generation"]
    assert len(commands) == 2
    assert commands[0].args[:2] == ["-m", "hottop.video_lowpoly3d"]
    assert str(Path(run.shots_dir).resolve()) in " ".join(commands[0].args)
