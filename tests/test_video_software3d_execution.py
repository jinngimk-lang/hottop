from pathlib import Path
from types import SimpleNamespace

import hottop.video_software3d_production as production
from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import VideoProductionConfig


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="software3d-runtime",
        topic_title="software 3d runtime",
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
        bridge="snake is workflow friction",
        frames=[
            CreativeRenderFrame(index=i, scene=f"scene {i}", caption=f"line {i}", intent="story")
            for i in range(1, 6)
        ],
        master_prompt="original low-poly comedy",
        negative_prompt="copied film frame",
        punchlines=["payoff"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "software3d-runtime",
            "style_profile": "anti-polish",
            "roughness_score": 78,
            "generation_backend": "software3d",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 10,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 3},
            "audio": {
                "bgm_style": "cheap original score",
                "foley_style": "crude foley",
                "voice_backend": "none",
                "music_backend": "none",
                "sfx_backend": "none",
            },
            "text": {},
        }
    )


def test_video_run_materializes_software3d_generation_into_workspace(tmp_path: Path):
    result = run_video_production(
        _request(),
        _config(),
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 5
    for index, command in enumerate(generation, start=1):
        assert command.args[:2] == ["-m", "hottop.video_software3d_production"]
        output_index = command.args.index("--output") + 1
        output = Path(command.args[output_index])
        assert output.is_absolute()
        assert output == (tmp_path / "run" / "shots" / f"shot-{index:03d}.mp4").resolve()
        assert command.cwd == str(tmp_path.resolve())


def test_odyssey_runtime_output_routes_renderer_to_workspace_story(monkeypatch, tmp_path: Path):
    request = _request().model_copy(update={"topic_id": "odyssey-witch-pigs"})
    result = run_video_production(
        request,
        _config(),
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )
    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    output_index = generation[0].args.index("--output") + 1
    output = Path(generation[0].args[output_index])
    captured = []
    monkeypatch.setattr(production, "render_scene_frame", lambda scene, _path: captured.append(scene))

    def fake_runner(args, **_kwargs):
        Path(args[-1]).write_bytes(b"fake-mp4")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    production.render_story_shot_video(
        shot_index=1,
        output=output,
        duration_seconds=1.0,
        width=180,
        height=320,
        fps=2,
        runner=fake_runner,
    )

    names = {mesh.name for mesh in captured[0].meshes}
    assert "witch-body" in names
    assert any(name.startswith("sailor-") for name in names)
    assert "young-cow-body" not in names


def test_software3d_readiness_requires_ffmpeg_for_shot_encoding(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("hottop.video_execution.shutil.which", lambda _name: None)

    status = inspect_video_environment(_config(), project_root=tmp_path)

    assert status.ready is False
    assert status.software3d is not None
    assert status.software3d.ready is False
    assert "FFmpeg executable" in status.software3d.missing
    assert any("software3d" in action.lower() for action in status.actions_required)
