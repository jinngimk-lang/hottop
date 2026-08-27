from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.audio_qwen3_tts import (
    Qwen3TTSCustomVoiceRequest,
    Qwen3TTSError,
    render_qwen3_custom_voice_dialogue,
)
from hottop.video_execution import _runtime_audio_commands
from hottop.video_production import AudioCue, VideoProductionConfig, VideoProductionPlan


def _fake_model_dir(tmp_path: Path) -> Path:
    model_dir = tmp_path / "Qwen3-TTS-CustomVoice"
    (model_dir / "speech_tokenizer").mkdir(parents=True)
    (model_dir / "config.json").write_text(
        json.dumps(
            {
                "model_type": "qwen3_tts",
                "tts_model_type": "custom_voice",
                "tts_model_size": "1b7",
            }
        ),
        encoding="utf-8",
    )
    (model_dir / "model.safetensors").write_bytes(b"weights")
    (model_dir / "speech_tokenizer" / "model.safetensors").write_bytes(b"tokenizer")
    return model_dir


def test_qwen3_rejects_waveform_longer_than_planned_dialogue_slot(monkeypatch, tmp_path: Path) -> None:
    model_dir = _fake_model_dir(tmp_path)
    output = tmp_path / "dialogue.wav"

    class FakeModel:
        @classmethod
        def from_pretrained(cls, *_args, **_kwargs):
            return cls()

        def generate_custom_voice(self, **_kwargs):
            # 1.25 seconds at 24 kHz for a one-second production slot.
            return [[0.1] * 30_000], 24_000

    fake_qwen = SimpleNamespace(Qwen3TTSModel=FakeModel)
    fake_torch = SimpleNamespace(bfloat16="bfloat16", float16="float16", float32="float32")

    def fake_import(name: str):
        if name == "qwen_tts":
            return fake_qwen
        if name == "torch":
            return fake_torch
        raise AssertionError(f"unexpected import: {name}")

    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda _name: object())
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.import_module", fake_import)

    request = Qwen3TTSCustomVoiceRequest(
        model_dir=model_dir,
        text="短句。",
        speaker="Vivian",
        language="Chinese",
        output=output,
        max_duration_seconds=1.0,
    )

    with pytest.raises(Qwen3TTSError, match="planned duration"):
        render_qwen3_custom_voice_dialogue(request)

    assert not output.exists()


def test_video_routing_passes_dialogue_slot_duration_to_qwen3(tmp_path: Path) -> None:
    model_dir = tmp_path / "qwen3-model"
    model_dir.mkdir()
    config = VideoProductionConfig.model_validate(
        {
            "name": "qwen3-duration-bound",
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
                "qwen3_custom_voice": {
                    "model_dir": str(model_dir),
                    "default_speaker": "Vivian",
                    "language": "Chinese",
                },
            },
            "text": {},
            "moviepy": {},
            "ffmpeg": {},
        }
    )
    plan = VideoProductionPlan.model_validate(
        {
            "config_name": "qwen3-duration-bound",
            "topic_id": "duration-bound",
            "topic_title": "duration-bound",
            "subject_name": "InkClawAgent",
            "style_profile": "cinematic",
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 2.0,
            "output_format": "mp4",
            "in_asset_cta_policy": "no-destination",
            "shots": [
                {
                    "index": 1,
                    "start_seconds": 0.0,
                    "end_seconds": 2.0,
                    "duration_seconds": 2.0,
                    "scene": "scene",
                    "intent": "intent",
                    "continuity_instruction": "same world",
                    "generation_prompt": "prompt",
                    "negative_prompt": "none",
                }
            ],
            "audio_cues": [
                AudioCue(
                    kind="dialogue",
                    start_seconds=0.0,
                    duration_seconds=0.8,
                    text="妈——！",
                    character="young-cow",
                )
            ],
        }
    )

    command = _runtime_audio_commands(
        plan,
        config,
        project_root=tmp_path,
        audio_dir=tmp_path / "audio",
    )[0]

    assert command.args[command.args.index("--max-duration-seconds") + 1] == "0.8"
