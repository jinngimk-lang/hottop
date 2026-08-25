from pathlib import Path

from hottop.video_execution import inspect_video_environment
from hottop.video_production import load_video_production_config


def _touch(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_video_environment_reports_ready_without_installing(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))
    wan_repo = tmp_path / "integrations" / "Wan2.2"
    model_dir = tmp_path / "models" / "Wan2.2-TI2V-5B"
    motion_dir = tmp_path / "video" / "motion-canvas-executor"
    _touch(wan_repo / "generate.py", "print('stub')")
    model_dir.mkdir(parents=True)
    _touch(motion_dir / "package.json", '{"scripts":{"render":"echo render"}}')

    binaries = {
        "python": "/usr/bin/python",
        "node": "/usr/bin/node",
        "npm": "/usr/bin/npm",
        "ffmpeg": "/usr/bin/ffmpeg",
    }
    monkeypatch.setattr("hottop.video_execution.shutil.which", binaries.get)

    status = inspect_video_environment(config, project_root=tmp_path)

    assert status.schema_version == "hottop.video-execution-status.v1"
    assert status.ready is True
    assert status.wan22.ready is True
    assert status.motion_canvas.ready is True
    assert status.ffmpeg.ready is True
    assert status.actions_required == []
    assert status.auto_install is False
    assert status.auto_download_models is False


def test_video_environment_fails_closed_when_heavy_dependencies_are_missing(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))
    monkeypatch.setattr("hottop.video_execution.shutil.which", lambda _name: None)

    status = inspect_video_environment(config, project_root=tmp_path)

    assert status.ready is False
    assert status.wan22.ready is False
    assert status.motion_canvas.ready is False
    assert status.ffmpeg.ready is False
    assert any("Wan2.2" in action for action in status.actions_required)
    assert any("Motion Canvas" in action for action in status.actions_required)
    assert any("FFmpeg" in action for action in status.actions_required)
    assert status.auto_install is False
    assert status.auto_download_models is False


def test_video_environment_rejects_planning_only_motion_canvas_scaffold(monkeypatch):
    config = load_video_production_config(Path("config/video/anti-polish-short.yml"))
    binaries = {
        "python": "/usr/bin/python",
        "node": "/usr/bin/node",
        "npm": "/usr/bin/npm",
        "ffmpeg": "/usr/bin/ffmpeg",
    }
    monkeypatch.setattr("hottop.video_execution.shutil.which", binaries.get)

    status = inspect_video_environment(config, project_root=Path("."))

    assert status.motion_canvas.ready is False
    assert "Motion Canvas project package.json" in status.motion_canvas.missing
    assert any("Motion Canvas" in action for action in status.actions_required)
