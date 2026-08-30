import json
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark


def _write_wav(path: Path, *, sample: int = 1000) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def test_tts_benchmark_requires_cold_and_warm_trial_per_candidate(tmp_path: Path) -> None:
    warm = _write_wav(tmp_path / "warm.wav")
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
                        "run_kind": "warm",
                        "wav": str(warm),
                        "latency_seconds": 0.5,
                        "runtime_revision": "audio.cpp@abc",
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
        "candidate audio-cpp requires both cold and warm trials; missing cold" in blocker
        for blocker in result.blockers
    )


def test_tts_benchmark_allows_multiple_warm_trials_when_cold_is_present(tmp_path: Path) -> None:
    cold = _write_wav(tmp_path / "cold.wav", sample=1000)
    warm_one = _write_wav(tmp_path / "warm-1.wav", sample=1100)
    warm_two = _write_wav(tmp_path / "warm-2.wav", sample=1200)
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
                        "latency_seconds": 1.2,
                        "runtime_revision": "audio.cpp@abc",
                    },
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "warm",
                        "wav": str(warm_one),
                        "latency_seconds": 0.6,
                        "runtime_revision": "audio.cpp@abc",
                    },
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "warm",
                        "wav": str(warm_two),
                        "latency_seconds": 0.5,
                        "runtime_revision": "audio.cpp@abc",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is True
