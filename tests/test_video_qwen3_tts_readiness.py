from __future__ import annotations

import json
from pathlib import Path

from hottop.video_execution import _voice_readiness
from hottop.video_production import VideoProductionConfig


def _config(model_dir: Path) -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "qwen3-local-readiness",
            "style_profile": "cinematic",
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 2.0,
            "shot_policy": {"min_shot_seconds": 1.0, "max_shot_seconds": 3.0},
            "audio": {
                "bgm_style": "original synthetic score",
                "foley_style": "procedural",
                "voice_backend": "qwen3-customvoice",
                "qwen3_custom_voice": {"model_dir": str(model_dir)},
            },
            "text": {},
            "moviepy": {},
            "ffmpeg": {},
        }
    )


def _fake_model(model_dir: Path, *, model_size: str) -> None:
    (model_dir / "speech_tokenizer").mkdir(parents=True)
    (model_dir / "config.json").write_text(
        json.dumps(
            {
                "model_type": "qwen3_tts",
                "tts_model_type": "custom_voice",
                "tts_model_size": model_size,
            }
        ),
        encoding="utf-8",
    )
    (model_dir / "model.safetensors").write_bytes(b"weights")
    (model_dir / "speech_tokenizer" / "model.safetensors").write_bytes(b"tokenizer")


def test_qwen3_video_readiness_rejects_06b_that_silently_ignores_instruct(
    monkeypatch, tmp_path: Path
) -> None:
    model_dir = tmp_path / "qwen-06b"
    _fake_model(model_dir, model_size="0b6")
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda _name: object())

    status = _voice_readiness(_config(model_dir), tmp_path)

    assert status.ready is False
    assert any("instruct" in item.lower() for item in status.missing)


def test_qwen3_video_readiness_accepts_17b_customvoice_with_instruct(
    monkeypatch, tmp_path: Path
) -> None:
    model_dir = tmp_path / "qwen-17b"
    _fake_model(model_dir, model_size="1b7")
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda _name: object())

    status = _voice_readiness(_config(model_dir), tmp_path)

    assert status.ready is True
    assert not any("instruct" in item.lower() for item in status.missing)
