import hashlib
import json
from pathlib import Path

from typer.testing import CliRunner

from hottop import pure_c_qwen3_tts_preflight as pure_c_preflight
from hottop.model_hub_cli import app

runner = CliRunner()


def _write_model_dir(root: Path) -> Path:
    model_dir = root / "qwen3-tts-1.7b"
    for relative_path in pure_c_preflight.REQUIRED_MODEL_FILES:
        path = model_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative_path == "config.json":
            path.write_text(
                json.dumps(
                    {
                        "model_type": "qwen3_tts",
                        "tts_model_size": "1b7",
                        "tts_model_type": "custom_voice",
                    }
                ),
                encoding="utf-8",
            )
        else:
            path.write_bytes(f"fixture:{relative_path}".encode())
    return model_dir


def _write_executable(root: Path) -> Path:
    executable = root / "qwen3-tts"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    return executable


def test_pure_c_preflight_binds_operator_provisioned_model_tree_without_execution(tmp_path: Path) -> None:
    executable = _write_executable(tmp_path)
    model_dir = _write_model_dir(tmp_path)

    result = pure_c_preflight.inspect_pure_c_qwen3_tts_inputs(
        executable=executable,
        model_dir=model_dir,
    )

    assert result.ready is True
    assert result.executed is False
    assert result.network_access is False
    assert result.auto_download is False
    assert result.model_dir == str(model_dir.resolve())
    assert result.executable is not None
    assert result.executable.sha256 == hashlib.sha256(executable.read_bytes()).hexdigest()
    assert set(result.artifacts) == set(pure_c_preflight.REQUIRED_MODEL_FILES)
    assert result.blockers == []


def test_pure_c_preflight_fails_closed_when_required_model_file_is_missing(tmp_path: Path) -> None:
    executable = _write_executable(tmp_path)
    model_dir = _write_model_dir(tmp_path)
    missing = model_dir / "speech_tokenizer" / "model.safetensors"
    missing.unlink()

    result = pure_c_preflight.inspect_pure_c_qwen3_tts_inputs(
        executable=executable,
        model_dir=model_dir,
    )

    assert result.ready is False
    assert "speech_tokenizer/model.safetensors" in " ".join(result.blockers)


def test_pure_c_preflight_rejects_reused_talker_and_speech_tokenizer_bytes(tmp_path: Path) -> None:
    executable = _write_executable(tmp_path)
    model_dir = _write_model_dir(tmp_path)
    talker = model_dir / "model.safetensors"
    speech_tokenizer = model_dir / "speech_tokenizer" / "model.safetensors"
    speech_tokenizer.write_bytes(talker.read_bytes())

    result = pure_c_preflight.inspect_pure_c_qwen3_tts_inputs(
        executable=executable,
        model_dir=model_dir,
    )

    assert result.ready is False
    assert "distinct" in " ".join(result.blockers).lower()


def test_pure_c_preflight_rejects_non_custom_voice_checkpoint(tmp_path: Path) -> None:
    executable = _write_executable(tmp_path)
    model_dir = _write_model_dir(tmp_path)
    (model_dir / "config.json").write_text(
        json.dumps(
            {
                "model_type": "qwen3_tts",
                "tts_model_size": "1b7",
                "tts_model_type": "base",
            }
        ),
        encoding="utf-8",
    )

    result = pure_c_preflight.inspect_pure_c_qwen3_tts_inputs(
        executable=executable,
        model_dir=model_dir,
    )

    assert result.ready is False
    assert "custom_voice" in " ".join(result.blockers).lower()


def test_model_hub_cli_exposes_read_only_pure_c_preflight(tmp_path: Path) -> None:
    executable = _write_executable(tmp_path)
    model_dir = _write_model_dir(tmp_path)

    result = runner.invoke(
        app,
        [
            "probe-qwen3-tts-pure-c",
            "--executable",
            str(executable),
            "--model-dir",
            str(model_dir),
        ],
    )

    assert result.exit_code == 0
    assert '"schema_version": "hottop.qwen3-tts-pure-c-preflight.v1"' in result.stdout
    assert '"ready": true' in result.stdout
    assert '"executed": false' in result.stdout
    assert '"network_access": false' in result.stdout
    assert '"auto_download": false' in result.stdout
