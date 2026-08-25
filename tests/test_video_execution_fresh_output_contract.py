import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.rendering import CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config


def test_video_run_rejects_stale_preexisting_outputs(monkeypatch, tmp_path):
    render_request = CreativeRenderRequest.model_validate(
        json.loads(Path("examples/video/inkclaw-cow-snake.render.json").read_text(encoding="utf-8"))
    )
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    output_dir = tmp_path / "video-output"
    shots_dir = output_dir / "shots"
    shots_dir.mkdir(parents=True)

    for index in range(1, len(render_request.frames) + 1):
        (shots_dir / f"shot-{index:03d}.mp4").write_bytes(b"stale-shot")
    (output_dir / "hottop-composite.mp4").write_bytes(b"stale-composite")
    (output_dir / "hottop-output.mp4").write_bytes(b"stale-final")

    monkeypatch.setattr(
        "hottop.video_execution.inspect_video_environment",
        lambda *_args, **_kwargs: SimpleNamespace(ready=True, actions_required=[]),
    )
    monkeypatch.setattr(
        "hottop.video_execution.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout="", stderr=""),
    )

    with pytest.raises(VideoExecutionError, match="fresh expected output"):
        run_video_production(
            render_request,
            config,
            output_dir=output_dir,
            project_root=tmp_path,
            execute=True,
        )
