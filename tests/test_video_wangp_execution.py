from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="wangp-runtime",
        topic_title="operator-managed WanGP runtime",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="One continuous original mythic banquet hall shot.",
                caption="先把活干完。",
                intent="setup and payoff",
                speaker="hero",
                delivery="calm, dry",
            )
        ],
        master_prompt="original cinematic mythic meme, believable faces and practical light",
        negative_prompt="actor likeness, copied film frame, official character design",
        punchlines=["先把活干完。"],
        risk_flags=["original characters only"],
        claim_status="satire",
    )


def _prepare_operator_install(root: Path) -> None:
    install = root / "integrations" / "WanGP-operator"
    (install / "shared").mkdir(parents=True)
    (install / "wgp.py").write_text("# operator-managed stub\n", encoding="utf-8")
    (install / "shared" / "api.py").write_text("# operator-managed stub\n", encoding="utf-8")
    (install / "hottop-settings.json").write_text(
        '{"model_type":"wan2.2_i2v","prompt":"template"}\n',
        encoding="utf-8",
    )


def test_video_doctor_reports_selected_wangp_operator_installation(monkeypatch, tmp_path):
    _prepare_operator_install(tmp_path)
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        lambda name: f"/usr/bin/{name}" if name in {"espeak", "ffmpeg"} else None,
    )
    monkeypatch.setattr("hottop.video_execution.importlib.util.find_spec", lambda _name: object())

    status = inspect_video_environment(config, project_root=tmp_path)

    assert status.external is not None
    assert status.external.backend == "wangp"
    assert status.external.ready is True
    assert status.ready is True
    assert not any("WanGP" in action for action in status.actions_required)
    assert status.auto_install is False
    assert status.auto_download_models is False


def test_video_doctor_fails_closed_when_wangp_operator_files_are_missing(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        lambda name: f"/usr/bin/{name}" if name in {"espeak", "ffmpeg"} else None,
    )
    monkeypatch.setattr("hottop.video_execution.importlib.util.find_spec", lambda _name: object())

    status = inspect_video_environment(config, project_root=tmp_path)

    assert status.external is not None
    assert status.external.ready is False
    assert "WanGP wgp.py" in status.external.missing
    assert "WanGP shared/api.py" in status.external.missing
    assert "WanGP exported settings JSON" in status.external.missing
    assert any("WanGP" in action for action in status.actions_required)


def test_video_run_dry_run_materializes_absolute_wangp_commands(monkeypatch, tmp_path):
    _prepare_operator_install(tmp_path)
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        lambda name: f"/usr/bin/{name}" if name in {"espeak", "ffmpeg"} else None,
    )
    monkeypatch.setattr("hottop.video_execution.importlib.util.find_spec", lambda _name: object())

    result = run_video_production(
        _request(),
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 1
    command = generation[0]
    assert command.program
    assert command.args[:3] == ["-m", "hottop.video_wangp", "--root"]
    root_arg = Path(command.args[3])
    settings_arg = Path(command.args[command.args.index("--settings") + 1])
    output_arg = Path(command.args[command.args.index("--output") + 1])
    assert root_arg == (tmp_path / "integrations" / "WanGP-operator").resolve()
    assert settings_arg == (
        tmp_path / "integrations" / "WanGP-operator" / "hottop-settings.json"
    ).resolve()
    assert output_arg == (tmp_path / "run" / "shots" / "shot-001.mp4").resolve()
    assert result.executed is False
    assert result.ready is True
