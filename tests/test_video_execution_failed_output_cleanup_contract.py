import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.rendering import CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config


def test_video_run_removes_partial_output_from_failed_stage(monkeypatch, tmp_path):
    render_request = CreativeRenderRequest.model_validate(
        json.loads(
            Path("examples/video/inkclaw-cow-snake.render.json").read_text(
                encoding="utf-8"
            )
        )
    )
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    output_dir = tmp_path / "video-output"
    partial_output: Path | None = None

    monkeypatch.setattr(
        "hottop.video_execution.inspect_video_environment",
        lambda *_args, **_kwargs: SimpleNamespace(ready=True, actions_required=[]),
    )

    def fail_after_writing_partial(command, **_kwargs):
        nonlocal partial_output
        save_index = command.index("--save_file") + 1
        partial_output = Path(command[save_index])
        partial_output.parent.mkdir(parents=True, exist_ok=True)
        partial_output.write_bytes(b"partial-corrupt-video")
        return SimpleNamespace(returncode=1, stdout="", stderr="generation failed")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", fail_after_writing_partial)

    with pytest.raises(VideoExecutionError, match="generation stage failed"):
        run_video_production(
            render_request,
            config,
            output_dir=output_dir,
            project_root=tmp_path,
            execute=True,
        )

    assert partial_output is not None
    assert not partial_output.exists()
