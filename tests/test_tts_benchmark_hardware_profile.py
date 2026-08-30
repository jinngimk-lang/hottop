import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark

GENERATION_PROTOCOL = {
    "seed": 42,
    "max_new_tokens": 256,
    "temperature": 0.9,
    "top_p": 1.0,
}


def _write_wav(path: Path, *, sample: int) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def _spec(tmp_path: Path, *, hardware_profile: dict[str, object] | None) -> Path:
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm = _write_wav(tmp_path / "warm.wav", sample=1100)
    payload: dict[str, object] = {
        "schema_version": "hottop.tts-benchmark-input.v1",
        "text": "今天我们测试同一句中文对白。",
        "language": "zh",
        "speaker": "Vivian",
        "generation_protocol": GENERATION_PROTOCOL,
        "trials": [
            {
                "candidate": "audio-cpp",
                "run_kind": "cold",
                "wav": str(cold),
                "latency_seconds": 1.0,
                "runtime_revision": "audio.cpp@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
            {
                "candidate": "audio-cpp",
                "run_kind": "warm",
                "wav": str(warm),
                "latency_seconds": 0.5,
                "runtime_revision": "audio.cpp@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
        ],
    }
    if hardware_profile is not None:
        payload["hardware_profile"] = hardware_profile
    spec = tmp_path / "bench.json"
    spec.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return spec


def test_tts_benchmark_fails_closed_without_hardware_profile(tmp_path: Path) -> None:
    result = inspect_tts_benchmark(_spec(tmp_path, hardware_profile=None))

    assert result.ready is False
    assert any("hardware_profile" in blocker for blocker in result.blockers)


def test_tts_benchmark_binds_hardware_profile_as_canonical_digest(tmp_path: Path) -> None:
    profile = {
        "cpu": "AMD EPYC 7763",
        "gpu": "NVIDIA H200 SXM",
        "gpu_count": 1,
        "backend": "cuda",
    }
    result = inspect_tts_benchmark(_spec(tmp_path, hardware_profile=profile))

    assert result.ready is True
    assert result.hardware_profile == profile
    assert len(result.hardware_profile_sha256) == 64
