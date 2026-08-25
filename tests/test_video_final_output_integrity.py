import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.rendering import CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config


def test_video_run_rejects_non_media_final_output_even_when_finalizer_returns_zero(
    monkeypatch, tmp_path
):
    render_request = CreativeRenderRequest.model_validate(
        json.loads(
            Path("examples/video/inkclaw-cow-snake.render.json").read_text(
                encoding="utf-8"
            )
        )
    )
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    output_dir = tmp_path / "video-output"

    monkeypatch.setattr(
        "hottop.video_execution.inspect_video_environment",
        lambda *_args, **_kwargs: SimpleNamespace(ready=True, actions_required=[]),
    )

    def fake_stage(command, **_kwargs):
        if "--save_file" in command:
            output = Path(command[command.index("--save_file") + 1])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(b"generated-shot")
        elif "-w" in command and Path(command[0]).name in {"espeak-ng", "espeak"}:
            output = Path(command[command.index("-w") + 1])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(b"dialogue-wav")
        elif "hottop.video_moviepy" in command and "--output" in command:
            output = Path(command[command.index("--output") + 1])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(b"composite-mp4")
        elif command[0] == "ffmpeg":
            output = Path(command[-1])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(b"not-a-real-mp4")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", fake_stage)

    with pytest.raises(VideoExecutionError, match="final output media verification failed"):
        run_video_production(
            render_request,
            config,
            output_dir=output_dir,
            project_root=tmp_path,
            execute=True,
        )
