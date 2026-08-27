from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from hottop.audio_qwen3_tts import Qwen3TTSCustomVoiceRequest, render_qwen3_custom_voice_dialogue


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


def test_qwen3_planned_duration_bounds_codec_generation_before_inference_completes(
    monkeypatch, tmp_path
):
    model_dir = _fake_model_dir(tmp_path)
    output = tmp_path / "dialogue.wav"
    calls: dict[str, object] = {}

    class FakeModel:
        @classmethod
        def from_pretrained(cls, *_args, **_kwargs):
            return cls()

        def generate_custom_voice(self, **kwargs):
            calls["generate_kwargs"] = kwargs
            return [[0.0, 0.25, -0.25, 0.0]], 24000

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
        text="这活先干完。",
        speaker="Vivian",
        language="Chinese",
        instruct="冷静、克制",
        output=output,
        max_duration_seconds=2.0,
    )

    render_qwen3_custom_voice_dialogue(request)

    generate_kwargs = calls["generate_kwargs"]
    assert isinstance(generate_kwargs, dict)
    # Qwen3-TTS 12Hz tokenizer runs at 12.5 codec frames/s. Permit one extra
    # generated token for EOS/control while bounding missing-EOS runaway work.
    assert generate_kwargs["max_new_tokens"] == 26
