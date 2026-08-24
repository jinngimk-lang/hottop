from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="anti-polish-cow-snake",
        topic_title="cow meets snake",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="controlled badness rough 3D comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="agent work starts with setup ceremony",
        deleted_constraint="remove deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="a nuisance snake literalizes workflow friction",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="One rough 3D cow codes in the same messy workshop while a snake crawls in.",
                caption="妈——！",
                intent="obstruction and reaction",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The mother cow enters the same workshop and points to InkClawAgent.",
                caption="傻孩子，用 InkClawAgent。",
                intent="deadpan solution",
            ),
        ],
        master_prompt="original intentionally cheap 3D animation with precise comedy timing",
        negative_prompt="glossy AI ad, copied film frame, slideshow",
        punchlines=["别被蛇绊住。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def test_video_run_dry_run_materializes_workspace_without_spawning(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("dry-run must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)

    result = run_video_production(
        _request(),
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    assert result.schema_version == "hottop.video-run.v1"
    assert result.execute_requested is False
    assert result.executed is False
    assert Path(result.plan_path).is_file()
    assert Path(result.compositor_manifest_path).is_file()
    assert Path(result.shots_dir).is_dir()
    assert result.final_output_path.endswith("hottop-output.mp4")
    assert [command.stage for command in result.runtime_commands] == [
        "generation",
        "generation",
        "compositor",
        "finalization",
    ]
    assert "--save_file" in result.runtime_commands[0].args
    assert result.runtime_commands[0].args[-1] != ""


def test_motion_canvas_dry_run_does_not_mutate_project_tree(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("dry-run must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)
    project_manifest = tmp_path / "video/motion-canvas/hottop-video-plan.json"

    result = run_video_production(
        _request(),
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    assert Path(result.compositor_manifest_path).is_file()
    assert not project_manifest.exists()


def test_video_run_execute_fails_closed_before_spawning_when_environment_is_not_ready(
    monkeypatch, tmp_path
):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    monkeypatch.setattr("hottop.video_execution.shutil.which", lambda _name: None)
    monkeypatch.setattr("hottop.video_execution.importlib.util.find_spec", lambda _name: None)

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("not-ready execution must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)

    with pytest.raises(VideoExecutionError, match="not ready"):
        run_video_production(
            _request(),
            config,
            output_dir=tmp_path / "run",
            project_root=tmp_path,
            execute=True,
        )


def test_video_run_execute_fails_closed_when_successful_stage_produces_no_output(
    monkeypatch, tmp_path
):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    monkeypatch.setattr(
        "hottop.video_execution.inspect_video_environment",
        lambda *_args, **_kwargs: SimpleNamespace(ready=True, actions_required=[]),
    )
    monkeypatch.setattr(
        "hottop.video_execution.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout="ok", stderr=""),
    )

    with pytest.raises(VideoExecutionError, match="did not produce expected output"):
        run_video_production(
            _request(),
            config,
            output_dir=tmp_path / "run",
            project_root=tmp_path,
            execute=True,
        )
