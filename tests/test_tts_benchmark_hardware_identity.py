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


def _inspect(tmp_path: Path, hardware_profile: dict[str, object]):
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm = _write_wav(tmp_path / "warm.wav", sample=1100)
    spec = tmp_path / "bench.json"
    spec.write_text(
        json.dumps(
            {
                "schema_version": "hottop.tts-benchmark-input.v1",
                "text": "今天我们测试同一句中文对白。",
                "language": "zh",
                "speaker": "Vivian",
                "generation_protocol": GENERATION_PROTOCOL,
                "hardware_profile": hardware_profile,
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
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return inspect_tts_benchmark(spec)


def test_tts_benchmark_rejects_hardware_profile_without_backend(tmp_path: Path) -> None:
    result = _inspect(tmp_path, {"cpu": "AMD EPYC 7763", "logical_cpu_count": 4})

    assert result.ready is False
    assert any("hardware_profile backend" in blocker for blocker in result.blockers)


def test_tts_benchmark_rejects_hardware_profile_without_device_identity(tmp_path: Path) -> None:
    result = _inspect(tmp_path, {"backend": "cpu", "logical_cpu_count": 4})

    assert result.ready is False
    assert any("hardware_profile device identity" in blocker for blocker in result.blockers)


def test_tts_benchmark_accepts_generic_accelerator_identity(tmp_path: Path) -> None:
    result = _inspect(
        tmp_path,
        {"backend": "vulkan", "accelerator": "AMD Radeon PRO", "device_count": 1},
    )

    assert result.ready is True
