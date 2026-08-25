# ruff: noqa
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.audio_qwen3_tts import (
    Qwen3TTSCustomVoiceRequest,
    Qwen3TTSError,
    inspect_qwen3_tts_environment,
    render_qwen3_custom_voice_dialogue,
)


def _fake_model_dir(tmp_path: Path) -> Path:
    model_dir = tmp_path / "Qwen3-TTS-12Hz-0.6B-CustomVoice"
    (model_dir / "speech_tokenizer").mkdir(parents=True)
    (model_dir / "config.json").write_text('{"model_type":"qwen3_tts"}', encoding="utf-8")
    (model_dir / "model.safetensors").write_bytes(b"weights")
    (model_dir / "speech_tokenizer" / "model.safetensors").write_bytes(b"tokenizer")
    return model_dir


def test_qwen3_environment_requires_operator_provisioned_local_model(monkeypatch, tmp_path):
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda name: object())

    missing = inspect_qwen3_tts_environment(model_dir=tmp_path / "missing")

    assert missing.ready is False
    assert "local Qwen3-TTS model directory" in missing.missing
    assert missing.auto_download_models is False


def test_qwen3_environment_accepts_complete_local_customvoice_model(monkeypatch, tmp_path):
    model_dir = _fake_model_dir(tmp_path)
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda name: object())

    status = inspect_qwen3_tts_environment(model_dir=model_dir)

    assert status.ready is True
    assert status.missing == []
    assert status.auto_download_models is False


def test_qwen3_request_rejects_remote_model_identifier():
    with pytest.raises(ValueError, match="local model directory"):
        Qwen3TTSCustomVoiceRequest(
            model_dir=Path("Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            text="你好",
            speaker="Vivian",
            language="Chinese",
            output=Path("out.wav"),
        )


def test_qwen3_render_uses_offline_local_model_and_delivery_instruction(monkeypatch, tmp_path):
    model_dir = _fake_model_dir(tmp_path)
    output = tmp_path / "dialogue.wav"
    calls: dict[str, object] = {}

    class FakeModel:
        @classmethod
        def from_pretrained(cls, model_path: str, **kwargs):
            calls["model_path"] = model_path
            calls["load_kwargs"] = kwargs
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

    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda name: object())
    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.import_module", fake_import)

    request = Qwen3TTSCustomVoiceRequest(
        model_dir=model_dir,
        text="这活先干完。",
        speaker="Vivian",
        language="Chinese",
        instruct="冷静、克制、略带无语",
        output=output,
        device="cuda:0",
        dtype="bfloat16",
        attn_implementation="flash_attention_2",
    )
    result = render_qwen3_custom_voice_dialogue(request)

    assert result == output
    assert output.is_file() and output.stat().st_size > 44
    assert calls["model_path"] == str(model_dir.resolve())
    assert calls["load_kwargs"] == {
        "device_map": "cuda:0",
        "dtype": "bfloat16",
        "attn_implementation": "flash_attention_2",
        "local_files_only": True,
    }
    assert calls["generate_kwargs"] == {
        "text": "这活先干完。",
        "language": "Chinese",
        "speaker": "Vivian",
        "instruct": "冷静、克制、略带无语",
    }


def test_qwen3_render_deletes_partial_output_on_failure(monkeypatch, tmp_path):
    model_dir = _fake_model_dir(tmp_path)
    output = tmp_path / "dialogue.wav"
    output.write_bytes(b"stale")

    class BrokenModel:
        @classmethod
        def from_pretrained(cls, *_args, **_kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr("hottop.audio_qwen3_tts.importlib.util.find_spec", lambda name: object())
    monkeypatch.setattr(
        "hottop.audio_qwen3_tts.importlib.import_module",
        lambda name: SimpleNamespace(Qwen3TTSModel=BrokenModel)
        if name == "qwen_tts"
        else SimpleNamespace(bfloat16="bfloat16", float16="float16", float32="float32"),
    )

    request = Qwen3TTSCustomVoiceRequest(
        model_dir=model_dir,
        text="你好",
        speaker="Vivian",
        language="Chinese",
        output=output,
    )
    with pytest.raises(Qwen3TTSError, match="local inference failed"):
        render_qwen3_custom_voice_dialogue(request)

    assert not output.exists()
