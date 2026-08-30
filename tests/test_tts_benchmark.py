import hashlib
import json
import wave
from pathlib import Path

from typer.testing import CliRunner

from hottop.model_hub_cli import app
from hottop.tts_benchmark import inspect_tts_benchmark

RUNNER = CliRunner()
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


def _write_wav(path: Path, *, frames: int = 24000, sample_rate: int = 24000, sample: int = 1000) -> Path:
    payload = int(sample).to_bytes(2, "little", signed=True) * frames
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(payload)
    return path


def test_tts_benchmark_binds_local_wav_bytes_and_speed_without_execution(tmp_path: Path) -> None:
    qwentts = _write_wav(tmp_path / "qwentts.wav")
    crispasr = _write_wav(tmp_path / "crispasr.wav", sample=1200)
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
                "trials": [
                    {
                        "candidate": "qwentts-cpp",
                        "run_kind": "cold",
                        "wav": str(qwentts),
                        "latency_seconds": 2.0,
                        "runtime_revision": "qwentts@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                    {
                        "candidate": "crispasr",
                        "run_kind": "warm",
                        "wav": str(crispasr),
                        "latency_seconds": 0.5,
                        "runtime_revision": "crispasr@def",
                        "model_revision": "qwen3-tts-customvoice@model-b",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = inspect_tts_benchmark(spec)

    assert result.schema_version == "hottop.tts-benchmark.v1"
    assert result.executed is False
    assert result.network_access is False
    assert result.auto_download is False
    assert result.listening_required is True
    assert result.generation_protocol == GENERATION_PROTOCOL
    assert result.generation_protocol_sha256 is not None
    assert result.hardware_profile == HARDWARE_PROFILE
    assert result.hardware_profile_sha256 is not None
    assert len(result.trials) == 2
    first = result.trials[0]
    assert first.runtime_revision == "qwentts@abc"
    assert first.model_revision == "qwen3-tts-customvoice@model-a"
    assert first.wav.sha256 == hashlib.sha256(qwentts.read_bytes()).hexdigest()
    assert first.wav.duration_seconds == 1.0
    assert first.wav.sample_rate == 24000
    assert first.wav.channels == 1
    assert first.realtime_factor == 2.0
    assert first.realtime_speedup == 0.5
    assert result.trials[1].realtime_factor == 0.5
    assert result.trials[1].realtime_speedup == 2.0


def test_tts_benchmark_fails_closed_for_silent_or_mismatched_trials(tmp_path: Path) -> None:
    silent = _write_wav(tmp_path / "silent.wav", sample=0)
    valid = _write_wav(tmp_path / "valid.wav")
    spec = tmp_path / "bench.json"
    spec.write_text(
        json.dumps(
            {
                "schema_version": "hottop.tts-benchmark-input.v1",
                "text": "同一句话",
                "language": "zh",
                "speaker": "Vivian",
                "generation_protocol": GENERATION_PROTOCOL,
                "hardware_profile": HARDWARE_PROFILE,
                "trials": [
                    {
                        "candidate": "qwentts-cpp",
                        "run_kind": "cold",
                        "wav": str(silent),
                        "latency_seconds": 1.0,
                        "runtime_revision": "qwentts@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                    {
                        "candidate": "qwentts-cpp",
                        "run_kind": "cold",
                        "wav": str(valid),
                        "latency_seconds": 0.0,
                        "runtime_revision": "qwentts@abc",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    result = inspect_tts_benchmark(spec)

    assert result.ready is False
    assert any("digital silence" in blocker for blocker in result.blockers)
    assert any("latency_seconds must be greater than zero" in blocker for blocker in result.blockers)


def test_model_hub_cli_exposes_read_only_tts_benchmark(tmp_path: Path) -> None:
    cold = _write_wav(tmp_path / "voice-cold.wav")
    warm = _write_wav(tmp_path / "voice-warm.wav", sample=1200)
    spec = tmp_path / "bench.json"
    spec.write_text(
        json.dumps(
            {
                "schema_version": "hottop.tts-benchmark-input.v1",
                "text": "你好，世界。",
                "language": "zh",
                "speaker": "Vivian",
                "generation_protocol": GENERATION_PROTOCOL,
                "hardware_profile": HARDWARE_PROFILE,
                "trials": [
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "cold",
                        "wav": str(cold),
                        "latency_seconds": 0.8,
                        "runtime_revision": "audio.cpp@xyz",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                    {
                        "candidate": "audio-cpp",
                        "run_kind": "warm",
                        "wav": str(warm),
                        "latency_seconds": 0.5,
                        "runtime_revision": "audio.cpp@xyz",
                        "model_revision": "qwen3-tts-customvoice@model-a",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = RUNNER.invoke(app, ["inspect-tts-benchmark", "--spec", str(spec)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.tts-benchmark.v1"
    assert payload["ready"] is True
    assert payload["executed"] is False
    assert payload["network_access"] is False
