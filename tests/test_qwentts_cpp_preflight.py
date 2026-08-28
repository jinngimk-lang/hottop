import hashlib
import json
from pathlib import Path

from typer.testing import CliRunner

from hottop.model_hub_cli import app
from hottop.qwentts_cpp_preflight import inspect_qwentts_cpp_inputs

RUNNER = CliRunner()
VALID_GGUF = b"GGUF\x03\x00\x00\x00fixture-payload"


def _write(path: Path, payload: bytes) -> Path:
    path.write_bytes(payload)
    return path


def test_qwentts_cpp_preflight_binds_local_bytes_without_execution(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"local-qwentts-binary")
    executable.chmod(0o755)
    talker = _write(tmp_path / "talker.gguf", VALID_GGUF + b"-talker")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is True
    assert result.executed is False
    assert result.network_access is False
    assert result.auto_download is False
    assert result.executable is not None
    assert result.talker_gguf is not None
    assert result.tokenizer_gguf is not None
    assert result.executable.sha256 == hashlib.sha256(b"local-qwentts-binary").hexdigest()
    assert result.talker_gguf.sha256 == hashlib.sha256(VALID_GGUF + b"-talker").hexdigest()
    assert result.tokenizer_gguf.sha256 == hashlib.sha256(VALID_GGUF + b"-tokenizer").hexdigest()
    assert result.executable.size_bytes == len(b"local-qwentts-binary")


def test_qwentts_cpp_preflight_fails_closed_for_missing_or_empty_assets(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    empty_talker = _write(tmp_path / "talker.gguf", b"")
    missing_tokenizer = tmp_path / "tokenizer.gguf"

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=empty_talker,
        tokenizer_gguf=missing_tokenizer,
    )

    assert result.ready is False
    assert result.executed is False
    assert any("talker GGUF is empty" in reason for reason in result.blockers)
    assert any("tokenizer GGUF does not exist" in reason for reason in result.blockers)


def test_qwentts_cpp_preflight_rejects_non_gguf_model_bytes(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    fake_talker = _write(tmp_path / "talker.gguf", b"not-a-gguf-model")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=fake_talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is False
    assert any("talker GGUF has invalid GGUF header" in reason for reason in result.blockers)


def test_qwentts_cpp_preflight_streams_artifact_hashing(tmp_path: Path, monkeypatch) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    talker = _write(tmp_path / "talker.gguf", VALID_GGUF + b"-talker")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")

    def forbid_read_bytes(self: Path) -> bytes:
        raise AssertionError(f"whole-file read is not allowed for benchmark artifacts: {self}")

    monkeypatch.setattr(Path, "read_bytes", forbid_read_bytes)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is True
    assert result.talker_gguf is not None
    assert result.talker_gguf.sha256 == hashlib.sha256(VALID_GGUF + b"-talker").hexdigest()


def test_model_hub_cli_exposes_read_only_qwentts_cpp_preflight(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    talker = _write(tmp_path / "talker.gguf", VALID_GGUF + b"-talker")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")

    result = RUNNER.invoke(
        app,
        [
            "probe-qwentts-cpp",
            "--executable",
            str(executable),
            "--talker-gguf",
            str(talker),
            "--tokenizer-gguf",
            str(tokenizer),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["ready"] is True
    assert payload["executed"] is False
    assert payload["network_access"] is False
    assert payload["auto_download"] is False
