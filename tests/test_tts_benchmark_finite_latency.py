import json
import math
import wave
from pathlib import Path

from hottop.tts_benchmark import inspect_tts_benchmark


def _write_wav(path: Path) -> Path:
    payload = (1000).to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def test_tts_benchmark_rejects_non_finite_latency_metrics(tmp_path: Path) -> None:
    wav = _write_wav(tmp_path / "voice.wav")

    for latency in (math.nan, math.inf, -math.inf):
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
                            "run_kind": "warm",
                            "wav": str(wav),
                            "latency_seconds": latency,
                            "runtime_revision": "qwentts@abc",
                        }
                    ],
                },
                allow_nan=True,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = inspect_tts_benchmark(spec)

        assert result.ready is False
        assert any(
            "latency_seconds must be finite and greater than zero" in blocker
            for blocker in result.blockers
        )
        assert result.trials[0].realtime_factor is None
        assert result.trials[0].realtime_speedup is None
