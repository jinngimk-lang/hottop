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


def test_tts_benchmark_requires_one_model_revision_per_candidate(tmp_path: Path) -> None:
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
                "trials": [
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "cold",
                        "wav": str(cold),
                        "latency_seconds": 1.1,
                        "runtime_revision": "audio.cpp@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "warm",
                        "wav": str(warm),
                        "latency_seconds": 0.5,
                        "runtime_revision": "audio.cpp@abc",
                        "model_revision": "qwen3-tts-customvoice@model-b",
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
        "candidate audio-cpp mixes model revisions: "
        "qwen3-tts-customvoice@model-a, qwen3-tts-customvoice@model-b" in blocker
        for blocker in result.blockers
    )
