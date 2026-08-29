import json
from pathlib import Path

from typer.testing import CliRunner

from hottop.model_hub_cli import app


runner = CliRunner()


def _write_gguf(path: Path, *, payload: bytes) -> None:
    header = (
        b"GGUF"
        + (3).to_bytes(4, "little")
        + (1).to_bytes(8, "little")
        + (0).to_bytes(8, "little")
    )
    path.write_bytes(header + payload)


def test_crispasr_probe_binds_local_inputs(tmp_path: Path) -> None:
    executable = tmp_path / "crispasr"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    talker = tmp_path / "talker.gguf"
    tokenizer = tmp_path / "tokenizer.gguf"
    _write_gguf(talker, payload=b"talker")
    _write_gguf(tokenizer, payload=b"tokenizer")

    result = runner.invoke(
        app,
        [
            "probe-crispasr",
            "--executable",
            str(executable),
            "--talker-gguf",
            str(talker),
            "--tokenizer-gguf",
            str(tokenizer),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["schema_version"] == "hottop.crispasr-preflight.v1"
    assert payload["ready"]
    assert not payload["executed"]
    assert not payload["network_access"]
    assert not payload["auto_download"]
    assert payload["executable"]["path"] == str(executable.resolve())
    assert payload["talker_gguf"]["path"] == str(talker.resolve())
    assert payload["tokenizer_gguf"]["path"] == str(tokenizer.resolve())
    assert payload["talker_gguf"]["sha256"] != payload["tokenizer_gguf"]["sha256"]


def test_crispasr_probe_rejects_reused_model_bytes(tmp_path: Path) -> None:
    executable = tmp_path / "crispasr"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    talker = tmp_path / "talker.gguf"
    tokenizer = tmp_path / "tokenizer.gguf"
    _write_gguf(talker, payload=b"same")
    tokenizer.write_bytes(talker.read_bytes())

    result = runner.invoke(
        app,
        [
            "probe-crispasr",
            "--executable",
            str(executable),
            "--talker-gguf",
            str(talker),
            "--tokenizer-gguf",
            str(tokenizer),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert not payload["ready"]
    expected = "talker GGUF and tokenizer GGUF must be distinct"
    assert any(expected in item for item in payload["blockers"])
