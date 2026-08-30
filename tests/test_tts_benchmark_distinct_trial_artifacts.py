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


def test_tts_benchmark_rejects_reusing_one_physical_wav_for_multiple_trials(
    tmp_path: Path,
) -> None:
    shared = _write_wav(tmp_path / "shared.wav")
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
                        "candidate": "qwentts-cpp",
                        "run_kind": "cold",
                        "wav": str(shared),
                        "latency_seconds": 2.0,
                        "runtime_revision": "qwentts@abc",
                    },
                    {
                        "candidate": "crispasr",
                        "run_kind": "warm",
                        "wav": str(shared),
                        "latency_seconds": 0.5,
                        "runtime_revision": "crispasr@def",
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
        "physical WAV artifact is reused across trials" in blocker
        for blocker in result.blockers
    )
