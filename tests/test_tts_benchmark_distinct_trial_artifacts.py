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


def _write_wav(path: Path) -> Path:
    sample = 1000
    payload = sample.to_bytes(2, "little", signed=True) * 24000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(payload)
    return path


def _write_spec(path: Path, trials: list[dict[str, object]]) -> Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": "hottop.tts-benchmark-input.v1",
                "text": "今天我们测试同一句中文对白。",
                "language": "zh",
                "speaker": "Vivian",
                "generation_protocol": GENERATION_PROTOCOL,
                "trials": trials,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def test_tts_benchmark_rejects_reusing_one_resolved_wav_path_for_multiple_trials(
    tmp_path: Path,
) -> None:
    shared = _write_wav(tmp_path / "shared.wav")
    spec = _write_spec(
        tmp_path / "bench.json",
        [
            {
                "candidate": "qwentts-cpp",
                "run_kind": "cold",
                "wav": str(shared),
                "latency_seconds": 2.0,
                "runtime_revision": "qwentts@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
            {
                "candidate": "crispasr",
                "run_kind": "warm",
                "wav": str(shared),
                "latency_seconds": 0.5,
                "runtime_revision": "crispasr@def",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
        ],
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is False
    assert any("resolved WAV path is reused across trials" in blocker for blocker in result.blockers)


def test_tts_benchmark_allows_independent_files_with_identical_audio_bytes(
    tmp_path: Path,
) -> None:
    first = _write_wav(tmp_path / "first.wav")
    second = tmp_path / "second.wav"
    second.write_bytes(first.read_bytes())
    spec = _write_spec(
        tmp_path / "repeatability.json",
        [
            {
                "candidate": "qwentts-cpp",
                "run_kind": "cold",
                "wav": str(first),
                "latency_seconds": 1.0,
                "runtime_revision": "qwentts@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
            {
                "candidate": "qwentts-cpp",
                "run_kind": "warm",
                "wav": str(second),
                "latency_seconds": 0.8,
                "runtime_revision": "qwentts@abc",
                "model_revision": "qwen3-tts-customvoice@model-a",
            },
        ],
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is True
    assert result.trials[0].wav is not None
    assert result.trials[1].wav is not None
    assert result.trials[0].wav.sha256 == result.trials[1].wav.sha256
    assert result.trials[0].wav.path != result.trials[1].wav.path
