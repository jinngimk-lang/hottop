from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_wangp import (
    WanGPAdapterConfig,
    WanGPError,
    prepare_wangp_settings,
    run_wangp_shot,
)


def test_prepare_wangp_settings_overrides_prompt_duration_and_fps():
    template = {
        "model_type": "wan2.2_i2v",
        "prompt": "old prompt",
        "video_length": 97,
        "duration_seconds": 4,
        "force_fps": 16,
        "num_inference_steps": 8,
    }

    settings = prepare_wangp_settings(
        template,
        prompt="one continuous cinematic comic shot",
        duration_seconds=3.5,
        fps=24,
    )

    assert settings["model_type"] == "wan2.2_i2v"
    assert settings["prompt"] == "one continuous cinematic comic shot"
    assert settings["video_length"] == "3.5s"
    assert settings["duration_seconds"] == 3.5
    assert settings["force_fps"] == 24
    assert settings["num_inference_steps"] == 8
    assert template["prompt"] == "old prompt"


def test_wangp_fails_before_submit_when_model_is_not_local(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        '{"model_type":"wan2.2_i2v","prompt":"template"}',
        encoding="utf-8",
    )
    submitted = []

    class FakeSession:
        def get_model_availability(self, model_type):
            assert model_type == "wan2.2_i2v"
            return {"model_type": model_type, "status": "missing", "available": False}

        def submit_task(self, settings):
            submitted.append(settings)
            raise AssertionError("submit_task must not run when local model files are missing")

    config = WanGPAdapterConfig(root=tmp_path / "WanGP", settings_path=settings_path)

    with pytest.raises(WanGPError, match="not available locally"):
        run_wangp_shot(
            config,
            prompt="test",
            duration_seconds=2.0,
            fps=24,
            output=tmp_path / "shot.mp4",
            session_factory=lambda **_kwargs: FakeSession(),
        )

    assert submitted == []


def test_wangp_copies_successful_generated_video_to_expected_shot_path(tmp_path):
    root = tmp_path / "WanGP"
    root.mkdir()
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        '{"model_type":"wan2.2_i2v","prompt":"template","num_inference_steps":8}',
        encoding="utf-8",
    )
    generated = tmp_path / "wangp-output.mp4"
    generated.write_bytes(b"real-generated-video-bytes")
    captured = {}

    class FakeJob:
        def result(self):
            return SimpleNamespace(success=True, generated_files=[str(generated)], errors=[])

    class FakeSession:
        def get_model_availability(self, model_type):
            return {"model_type": model_type, "status": "available", "available": True}

        def submit_task(self, settings):
            captured["settings"] = settings
            return FakeJob()

    def factory(**kwargs):
        captured["factory"] = kwargs
        return FakeSession()

    output = tmp_path / "shots" / "shot-001.mp4"
    config = WanGPAdapterConfig(
        root=root,
        settings_path=settings_path,
        profile=4,
        attention="sdpa",
    )

    result = run_wangp_shot(
        config,
        prompt="hero crosses the banquet hall",
        duration_seconds=2.5,
        fps=24,
        output=output,
        session_factory=factory,
    )

    assert result == output
    assert output.read_bytes() == b"real-generated-video-bytes"
    assert captured["settings"]["prompt"] == "hero crosses the banquet hall"
    assert captured["settings"]["video_length"] == "2.5s"
    assert captured["settings"]["force_fps"] == 24
    assert captured["factory"]["root"] == root.resolve()
    assert captured["factory"]["output_dir"] == output.parent.resolve()
    assert captured["factory"]["cli_args"] == ["--profile", "4", "--attention", "sdpa"]
    assert config.auto_download_models is False
