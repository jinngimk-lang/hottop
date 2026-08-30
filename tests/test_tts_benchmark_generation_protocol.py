import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark

HARDWARE_PROFILE = {
    "cpu": "AMD EPYC 7763",
    "backend": "cpu",
    "logical_cpu_count": 4,
}
EXECUTION_PROFILE = {
    "mode": "cli",
    "concurrency": 1,
    "batch_size": 1,
}


def _write_wav(path: Path, *, sample: int) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def _spec(tmp_path: Path, *, generation_protocol: dict[str, object] | None) -> Path:
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm = _write_wav(tmp_path / "warm.wav", sample=1100)
    payload: dict[str, object] = {
        "schema_version": "hottop.tts-benchmark-input.v1",
        "text": "今天我们测试同一句中文对白。",
        "language": "zh",
        "speaker": "Vivian",
        "hardware_profile": HARDWARE_PROFILE,
        "execution_profile": EXECUTION_PROFILE,
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
    if generation_protocol is not None:
        payload["generation_protocol"] = generation_protocol
    spec = tmp_path / "bench.json"
    spec.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return spec


def test_tts_benchmark_fails_closed_without_generation_protocol(tmp_path: Path) -> None:
    result = inspect_tts_benchmark(_spec(tmp_path, generation_protocol=None))

    assert result.ready is False
    assert any("generation_protocol" in blocker for blocker in result.blockers)


def test_tts_benchmark_binds_generation_protocol_as_canonical_digest(tmp_path: Path) -> None:
    protocol = {
        "seed": 42,
        "max_new_tokens": 256,
        "temperature": 0.9,
        "top_p": 1.0,
        "top_k": 50,
        "repetition_penalty": 1.05,
    }
    result = inspect_tts_benchmark(_spec(tmp_path, generation_protocol=protocol))

    assert result.ready is True
    assert result.generation_protocol == protocol
    assert len(result.generation_protocol_sha256) == 64
