import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark

GENERATION_PROTOCOL = {
    "seed": 42,
    "max_new_tokens": 256,
    "temperature": 0.9,
}
HARDWARE_PROFILE = {
    "cpu": "Dual Xeon",
    "backend": "cpu",
    "logical_cpu_count": 24,
}


def _write_wav(path: Path, *, sample: int) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def _write_spec(tmp_path: Path, execution_profile: dict[str, object]) -> Path:
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
                "generation_protocol": GENERATION_PROTOCOL,
                "hardware_profile": HARDWARE_PROFILE,
                "execution_profile": execution_profile,
                "trials": [
                    {
                        "candidate": "pure-c-server",
                        "run_kind": "cold",
                        "wav": str(cold),
                        "latency_seconds": 2.0,
                        "runtime_revision": "pure-c@f1b68657",
                        "model_revision": "qwen3-tts-customvoice@1b7",
                    },
                    {
                        "candidate": "pure-c-server",
                        "run_kind": "warm",
                        "wav": str(warm),
                        "latency_seconds": 1.0,
                        "runtime_revision": "pure-c@f1b68657",
                        "model_revision": "qwen3-tts-customvoice@1b7",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return spec


def test_server_benchmark_requires_worker_and_thread_topology(tmp_path: Path) -> None:
    spec = _write_spec(
        tmp_path,
        {
            "mode": "server",
            "concurrency": 24,
            "batch_size": 1,
            "connection_strategy": "http-keepalive",
        },
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is False
    assert any("worker_count" in blocker for blocker in result.blockers)
    assert any("threads_per_worker" in blocker for blocker in result.blockers)


def test_server_benchmark_accepts_bound_worker_and_thread_topology(tmp_path: Path) -> None:
    spec = _write_spec(
        tmp_path,
        {
            "mode": "server",
            "concurrency": 24,
            "batch_size": 1,
            "connection_strategy": "http-keepalive",
            "worker_count": 12,
            "threads_per_worker": 2,
        },
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is True
