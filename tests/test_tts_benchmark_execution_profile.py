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
HARDWARE_PROFILE = {
    "cpu": "AMD EPYC 7763",
    "backend": "cpu",
    "logical_cpu_count": 4,
}


def _write_wav(path: Path, *, sample: int) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def _inspect(tmp_path: Path, execution_profile: dict[str, object] | None):
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm = _write_wav(tmp_path / "warm.wav", sample=1100)
    payload: dict[str, object] = {
        "schema_version": "hottop.tts-benchmark-input.v1",
        "text": "今天我们测试同一句中文对白。",
        "language": "zh",
        "speaker": "Vivian",
        "generation_protocol": GENERATION_PROTOCOL,
        "hardware_profile": HARDWARE_PROFILE,
        "trials": [
            {
                "candidate": "qwentts-cpp",
                "run_kind": "cold",
                "wav": str(cold),
                "latency_seconds": 1.0,
                "runtime_revision": "qwentts.cpp@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
            {
                "candidate": "qwentts-cpp",
                "run_kind": "warm",
                "wav": str(warm),
                "latency_seconds": 0.5,
                "runtime_revision": "qwentts.cpp@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
        ],
    }
    if execution_profile is not None:
        payload["execution_profile"] = execution_profile
    spec = tmp_path / "bench.json"
    spec.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return inspect_tts_benchmark(spec)


def test_tts_benchmark_requires_execution_profile_for_latency_evidence(tmp_path: Path) -> None:
    result = _inspect(tmp_path, None)

    assert result.ready is False
    assert any("execution_profile" in blocker for blocker in result.blockers)


def test_tts_benchmark_rejects_descriptive_execution_profile(tmp_path: Path) -> None:
    result = _inspect(tmp_path, {"note": "same settings"})

    assert result.ready is False
    assert any("execution_profile mode" in blocker for blocker in result.blockers)
    assert any("execution_profile concurrency" in blocker for blocker in result.blockers)
    assert any("execution_profile batch_size" in blocker for blocker in result.blockers)


def test_tts_benchmark_requires_connection_strategy_for_server_mode(tmp_path: Path) -> None:
    result = _inspect(
        tmp_path,
        {"mode": "server", "concurrency": 1, "batch_size": 1},
    )

    assert result.ready is False
    assert any("connection_strategy" in blocker for blocker in result.blockers)


def test_tts_benchmark_accepts_concrete_cli_execution_profile(tmp_path: Path) -> None:
    result = _inspect(
        tmp_path,
        {"mode": "cli", "concurrency": 1, "batch_size": 1},
    )

    assert result.ready is True
    assert result.execution_profile == {
        "mode": "cli",
        "concurrency": 1,
        "batch_size": 1,
    }
    assert result.execution_profile_sha256 is not None
