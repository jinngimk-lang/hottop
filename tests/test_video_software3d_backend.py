from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import VideoProductionConfig, build_video_production_plan


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="software3d-backend",
        topic_title="software 3d backend",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="original low-poly comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="a nuisance snake embodies setup friction",
        frames=[
            CreativeRenderFrame(index=1, scene="cow types", caption="哎呀", intent="setup"),
            CreativeRenderFrame(index=2, scene="cow recoils", caption="妈", intent="escalate"),
            CreativeRenderFrame(index=3, scene="mother enters", caption="用 InkClawAgent", intent="reverse"),
            CreativeRenderFrame(index=4, scene="snake loosens", caption="这么直接", intent="solve"),
            CreativeRenderFrame(index=5, scene="snake leaves", caption="别被蛇绊住", intent="payoff"),
        ],
        master_prompt="original low-poly 3d comedy",
        negative_prompt="copied film frame",
        punchlines=["别被蛇绊住"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "software3d-test",
            "style_profile": "anti-polish",
            "roughness_score": 78,
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 10,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 3},
            "audio": {"bgm_style": "cheap original score", "foley_style": "crude foley"},
            "text": {},
            "moviepy": {"shot_dir": "shots", "composite_name": "composite.mp4"},
            "ffmpeg": {
                "video_codec": "libx264",
                "audio_codec": "aac",
                "pixel_format": "yuv420p",
                "movflags": "+faststart",
            },
        }
    )


def test_software3d_backend_emits_one_generation_command_per_shot():
    plan = build_video_production_plan(_request(), _config())

    assert plan.generation_backend == "software3d"
    assert len(plan.generation_command_specs) == 5
    for shot, command in zip(plan.shots, plan.generation_command_specs, strict=True):
        assert command.stage == "generation"
        assert command.args[:2] == ["-m", "hottop.video_software3d_production"]
        assert "--shot-index" in command.args
        assert str(shot.index) in command.args
        assert "--output" in command.args
        assert f"shots/shot-{shot.index:03d}.mp4" in command.args


def test_software3d_backend_is_explicitly_zero_cost_and_deterministic():
    plan = build_video_production_plan(_request(), _config())

    notes = " ".join(plan.execution_notes).lower()
    assert "zero-cost" in notes
    assert "deterministic" in notes
    assert "no model" in notes or "model download" in notes
