import json
from pathlib import Path

from typer.testing import CliRunner

from hottop.model_hub_cli import app

runner = CliRunner()


def _write_gguf(path: Path, *, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        b"GGUF"
        + (3).to_bytes(4, "little")
        + (1).to_bytes(8, "little")
        + (0).to_bytes(8, "little")
    )
    path.write_bytes(header + payload)


def test_audio_cpp_probe_binds_customvoice_model_directory(tmp_path: Path) -> None:
    executable = tmp_path / "audiocpp_cli"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    model_dir = tmp_path / "Qwen3-TTS-12Hz-1.7B-CustomVoice"
    talker = model_dir / "model.gguf"
    tokenizer = model_dir / "speech_tokenizer" / "model.gguf"
    _write_gguf(talker, payload=b"talker")
    _write_gguf(tokenizer, payload=b"tokenizer")

    result = runner.invoke(
        app,
        [
            "probe-audio-cpp",
            "--executable",
            str(executable),
            "--model-dir",
            str(model_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["schema_version"] == "hottop.audio-cpp-preflight.v1"
    assert payload["ready"]
    assert not payload["executed"]
    assert not payload["network_access"]
    assert not payload["auto_download"]
    assert payload["model_dir"] == str(model_dir.resolve())
    assert payload["executable"]["path"] == str(executable.resolve())
    assert payload["talker_gguf"]["path"] == str(talker.resolve())
    assert payload["tokenizer_gguf"]["path"] == str(tokenizer.resolve())
    assert payload["talker_gguf"]["sha256"] != payload["tokenizer_gguf"]["sha256"]


def test_audio_cpp_probe_fails_closed_when_nested_tokenizer_is_missing(tmp_path: Path) -> None:
    executable = tmp_path / "audiocpp_cli"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    model_dir = tmp_path / "Qwen3-TTS-12Hz-1.7B-CustomVoice"
    _write_gguf(model_dir / "model.gguf", payload=b"talker")

    result = runner.invoke(
        app,
        [
            "probe-audio-cpp",
            "--executable",
            str(executable),
            "--model-dir",
            str(model_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert not payload["ready"]
    assert any("speech_tokenizer/model.gguf" in blocker for blocker in payload["blockers"])
