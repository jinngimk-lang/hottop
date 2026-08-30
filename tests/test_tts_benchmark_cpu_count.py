import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark


def _write_wav(path: Path, *, sample: int) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def test_cpu_benchmark_requires_logical_cpu_count(tmp_path: Path) -> None:
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm = _write_wav(tmp_path / "warm.wav", sample=1200)
    spec = tmp_path / "bench.json"
    spec.write_text(
        json.dumps(
            {
                "schema_version": "hottop.tts-benchmark-input.v1",
                "text": "今天我们测试同一句中文对白。",
                "language": "zh",
                "speaker": "Vivian",
                "generation_protocol": {
                    "seed": 42,
                    "max_new_tokens": 256,
                    "temperature": 0.9,
                },
                "hardware_profile": {
                    "backend": "cpu",
                    "cpu": "dual Xeon test host",
                },
                "execution_profile": {
                    "mode": "server",
                    "concurrency": 24,
                    "batch_size": 1,
                    "connection_strategy": "prefork",
                    "worker_count": 12,
                    "threads_per_worker": 2,
                },
                "trials": [
                    {
                        "candidate": "pure-c",
                        "run_kind": "cold",
                        "wav": str(cold),
                        "latency_seconds": 2.0,
                        "runtime_revision": "pure-c@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                    {
                        "candidate": "pure-c",
                        "run_kind": "warm",
                        "wav": str(warm),
                        "latency_seconds": 1.0,
                        "runtime_revision": "pure-c@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is False
    assert any(
        "hardware_profile cpu backend requires positive integer logical_cpu_count"
        in blocker
        for blocker in result.blockers
    )
