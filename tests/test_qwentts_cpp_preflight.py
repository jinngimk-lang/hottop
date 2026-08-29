import hashlib
import json
from pathlib import Path

from typer.testing import CliRunner

import hottop.qwentts_cpp_preflight as qwentts_preflight
from hottop.model_hub_cli import app
from hottop.qwentts_cpp_preflight import inspect_qwentts_cpp_inputs

RUNNER = CliRunner()
VALID_GGUF = (
    b"GGUF"
    + (3).to_bytes(4, "little")
    + (1).to_bytes(8, "little")
    + (0).to_bytes(8, "little")
    + b"fixture-payload"
)
ZERO_TENSOR_GGUF = (
    b"GGUF"
    + (3).to_bytes(4, "little")
    + (0).to_bytes(8, "little")
    + (0).to_bytes(8, "little")
    + b"fixture-payload"
)


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


def test_qwentts_cpp_preflight_rejects_magic_only_or_truncated_gguf_header(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    truncated_talker = _write(tmp_path / "talker.gguf", b"GGUF\x03\x00\x00\x00")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=truncated_talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is False
    assert any("talker GGUF has truncated GGUF header" in reason for reason in result.blockers)


def test_qwentts_cpp_preflight_rejects_zero_tensor_gguf_model(tmp_path: Path) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    zero_tensor_talker = _write(tmp_path / "talker.gguf", ZERO_TENSOR_GGUF)
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=zero_tensor_talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is False
    assert any("talker GGUF has zero tensors" in reason for reason in result.blockers)


def test_qwentts_cpp_preflight_rejects_artifact_mutated_during_hashing(
    tmp_path: Path, monkeypatch
) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    talker = _write(tmp_path / "talker.gguf", VALID_GGUF + b"-talker")
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")
    original_stream = qwentts_preflight._stream_sha256_and_header

    def mutate_after_stream(path: Path) -> tuple[str, bytes]:
        digest, header = original_stream(path)
        if path == talker:
            with path.open("ab") as handle:
                handle.write(b"-mutated-after-hash")
        return digest, header

    monkeypatch.setattr(
        qwentts_preflight,
        "_stream_sha256_and_header",
        mutate_after_stream,
    )

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is False
    assert any("talker GGUF changed during preflight" in reason for reason in result.blockers)


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


def test_qwentts_cpp_preflight_rejects_executable_reused_as_model_artifact(tmp_path: Path) -> None:
    executable_and_talker = _write(tmp_path / "qwentts-cli", VALID_GGUF + b"-talker")
    executable_and_talker.chmod(0o755)
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")

    result = inspect_qwentts_cpp_inputs(
        executable=executable_and_talker,
        talker_gguf=executable_and_talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is False
    assert any("qwentts executable and model GGUF artifacts must be distinct" in reason for reason in result.blockers)

    executable_and_tokenizer = _write(tmp_path / "qwentts-cli-2", VALID_GGUF + b"-tokenizer-2")
    executable_and_tokenizer.chmod(0o755)
    talker = _write(tmp_path / "talker.gguf", VALID_GGUF + b"-talker-2")

    result = inspect_qwentts_cpp_inputs(
        executable=executable_and_tokenizer,
        talker_gguf=talker,
        tokenizer_gguf=executable_and_tokenizer,
    )

    assert result.ready is False
    assert any("qwentts executable and model GGUF artifacts must be distinct" in reason for reason in result.blockers)


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
