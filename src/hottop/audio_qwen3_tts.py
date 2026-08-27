from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import math
import os
import wave
from array import array
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

Qwen3Speaker = Literal[
    "Vivian",
    "Serena",
    "Uncle_Fu",
    "Dylan",
    "Eric",
    "Ryan",
    "Aiden",
    "Ono_Anna",
    "Sohee",
]
Qwen3Language = Literal[
    "Chinese",
    "English",
    "Japanese",
    "Korean",
    "German",
    "French",
    "Russian",
    "Portuguese",
    "Spanish",
    "Italian",
]
Qwen3DType = Literal["bfloat16", "float16", "float32"]


class Qwen3TTSError(RuntimeError):
    """Raised when a local Qwen3-TTS request cannot complete safely."""


class Qwen3TTSEnvironment(BaseModel):
    ready: bool
    missing: list[str] = Field(default_factory=list)
    auto_download_models: Literal[False] = False


class Qwen3TTSCustomVoiceRequest(BaseModel):
    model_dir: Path
    text: str = Field(min_length=1)
    speaker: Qwen3Speaker = "Vivian"
    language: Qwen3Language = "Chinese"
    instruct: str = ""
    output: Path
    device: str = Field(default="cuda:0", min_length=1)
    dtype: Qwen3DType = "bfloat16"
    attn_implementation: str | None = "flash_attention_2"

    @model_validator(mode="after")
    def validate_local_request(self) -> Qwen3TTSCustomVoiceRequest:
        if not self.text.strip():
            raise ValueError("Qwen3-TTS text must not be blank")
        if not self.device.strip():
            raise ValueError("Qwen3-TTS device must not be blank")
        model_dir = self.model_dir.expanduser().resolve()
        if not model_dir.is_dir():
            raise ValueError("Qwen3-TTS requires an operator-provisioned local model directory")
        self.model_dir = model_dir
        self.text = self.text.strip()
        self.instruct = self.instruct.strip()
        self.device = self.device.strip()
        if self.attn_implementation is not None:
            normalized = self.attn_implementation.strip()
            self.attn_implementation = normalized or None
        return self


def inspect_qwen3_tts_environment(
    *,
    model_dir: Path,
    require_instruct: bool = True,
) -> Qwen3TTSEnvironment:
    """Inspect a local Qwen3 CustomVoice runtime without installing or downloading anything."""

    missing: list[str] = []
    resolved = model_dir.expanduser().resolve()
    if importlib.util.find_spec("qwen_tts") is None:
        missing.append("qwen-tts Python package")
    if importlib.util.find_spec("torch") is None:
        missing.append("PyTorch runtime")
    if not resolved.is_dir():
        missing.append("local Qwen3-TTS model directory")
    else:
        required = [
            resolved / "config.json",
            resolved / "model.safetensors",
            resolved / "speech_tokenizer" / "model.safetensors",
        ]
        for path in required:
            if not path.is_file() or path.stat().st_size <= 0:
                missing.append(f"local Qwen3-TTS model file: {path.relative_to(resolved)}")
        config_path = resolved / "config.json"
        if config_path.is_file() and config_path.stat().st_size > 0:
            try:
                model_config = json.loads(config_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                missing.append("valid local Qwen3-TTS config.json")
            else:
                if model_config.get("model_type") != "qwen3_tts":
                    missing.append("Qwen3-TTS model config with model_type=qwen3_tts")
                if model_config.get("tts_model_type") != "custom_voice":
                    missing.append("Qwen3-TTS CustomVoice model config")
                model_size = model_config.get("tts_model_size")
                if model_size not in {"0b6", "1b7"}:
                    missing.append("supported Qwen3-TTS CustomVoice model size (0.6B or 1.7B)")
                if require_instruct and model_size != "1b7":
                    missing.append(
                        "Qwen3-TTS CustomVoice model with instruct support (1.7B required; 0.6B ignores instruct)"
                    )
    return Qwen3TTSEnvironment(ready=not missing, missing=missing)


@contextmanager
def _offline_huggingface_environment():
    names = ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_HUB_DISABLE_TELEMETRY")
    previous = {name: os.environ.get(name) for name in names}
    for name in names:
        os.environ[name] = "1"
    try:
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _flatten_samples(value: object) -> list[float]:
    current = value
    for attr in ("detach", "cpu"):
        method = getattr(current, attr, None)
        if callable(method):
            current = method()
    numpy_method = getattr(current, "numpy", None)
    if callable(numpy_method):
        current = numpy_method()
    tolist_method = getattr(current, "tolist", None)
    if callable(tolist_method):
        current = tolist_method()
    while isinstance(current, list) and len(current) == 1 and isinstance(current[0], list):
        current = current[0]
    if not isinstance(current, (list, tuple)):
        raise Qwen3TTSError("Qwen3-TTS returned unsupported audio samples")
    try:
        return [float(sample) for sample in current]
    except (TypeError, ValueError) as exc:
        raise Qwen3TTSError("Qwen3-TTS returned invalid audio samples") from exc


def _write_pcm16_wav(path: Path, samples: list[float], sample_rate: int) -> None:
    if not samples:
        raise Qwen3TTSError("Qwen3-TTS returned empty audio")
    if sample_rate <= 0:
        raise Qwen3TTSError("Qwen3-TTS returned invalid sample rate")
    if any(not math.isfinite(sample) for sample in samples):
        raise Qwen3TTSError("Qwen3-TTS returned non-finite audio samples")
    if not any(sample != 0.0 for sample in samples):
        raise Qwen3TTSError("Qwen3-TTS returned silent audio")
    pcm = array(
        "h",
        (int(max(-1.0, min(1.0, sample)) * 32767) for sample in samples),
    )
    if not any(sample != 0 for sample in pcm):
        raise Qwen3TTSError("Qwen3-TTS returned silent audio")
    temporary = path.with_suffix(path.suffix + ".part")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.unlink(missing_ok=True)
    temporary.unlink(missing_ok=True)
    try:
        with wave.open(str(temporary), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(sample_rate)
            handle.writeframes(pcm.tobytes())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def render_qwen3_custom_voice_dialogue(request: Qwen3TTSCustomVoiceRequest) -> Path:
    """Render one line with a preinstalled local Qwen3-TTS CustomVoice model."""

    status = inspect_qwen3_tts_environment(
        model_dir=request.model_dir,
        require_instruct=bool(request.instruct),
    )
    if not status.ready:
        raise Qwen3TTSError("Qwen3-TTS environment is not ready: " + ", ".join(status.missing))

    output = request.output.expanduser().resolve()
    output.unlink(missing_ok=True)
    try:
        qwen_tts = importlib.import_module("qwen_tts")
        torch = importlib.import_module("torch")
        model_type = getattr(torch, request.dtype)
        load_kwargs: dict[str, object] = {
            "device_map": request.device,
            "dtype": model_type,
            "local_files_only": True,
        }
        if request.attn_implementation is not None:
            load_kwargs["attn_implementation"] = request.attn_implementation
        with _offline_huggingface_environment():
            model = qwen_tts.Qwen3TTSModel.from_pretrained(
                str(request.model_dir),
                **load_kwargs,
            )
            wavs, sample_rate = model.generate_custom_voice(
                text=request.text,
                language=request.language,
                speaker=request.speaker,
                instruct=request.instruct,
            )
        if not isinstance(wavs, (list, tuple)) or len(wavs) != 1:
            raise Qwen3TTSError("Qwen3-TTS must return exactly one dialogue waveform")
        samples = _flatten_samples(wavs[0])
        _write_pcm16_wav(output, samples, int(sample_rate))
    except Qwen3TTSError:
        output.unlink(missing_ok=True)
        raise
    except Exception as exc:
        output.unlink(missing_ok=True)
        raise Qwen3TTSError(f"Qwen3-TTS local inference failed: {exc}") from exc
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render one dialogue line with an operator-provisioned local Qwen3-TTS CustomVoice model."
    )
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker", default="Vivian")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--instruct", default="")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--dtype", default="bfloat16")
    parser.add_argument("--attn-implementation", default="flash_attention_2")
    args = parser.parse_args()
    request = Qwen3TTSCustomVoiceRequest(
        model_dir=args.model_dir,
        text=args.text,
        speaker=args.speaker,
        language=args.language,
        instruct=args.instruct,
        output=args.output,
        device=args.device,
        dtype=args.dtype,
        attn_implementation=args.attn_implementation,
    )
    render_qwen3_custom_voice_dialogue(request)


if __name__ == "__main__":
    main()
