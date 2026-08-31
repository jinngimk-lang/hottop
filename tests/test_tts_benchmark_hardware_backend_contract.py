import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark


def _write_wav(path: Path) -> Path:
    payload = int(1000).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def test_tts_benchmark_rejects_unknown_hardware_backend(tmp_path: Path) -> None:
    wav_path = _write_wav(tmp_path / "voice.wav")
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
                    "backend": "banana",
                    "accelerator": "mystery-device",
                },
                "execution_profile": {
                    "mode": "cli",
                    "concurrency": 1,
                    "batch_size": 1,
                },
                "trials": [
                    {
                        "candidate": "qwentts-cpp",
                        "run_kind": "cold",
                        "wav": str(wav_path),
                        "latency_seconds": 1.0,
                        "runtime_revision": "qwentts@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is False
    assert any(
        "hardware_profile backend must be one of" in blocker
        for blocker in result.blockers
    )