from pathlib import Path

from hottop.qwentts_cpp_preflight import inspect_qwentts_cpp_inputs

VALID_GGUF = (
    b"GGUF"
    + (3).to_bytes(4, "little")
    + (0).to_bytes(8, "little")
    + (0).to_bytes(8, "little")
    + b"fixture-payload"
)


def _make_executable(tmp_path: Path) -> Path:
    executable = tmp_path / "qwentts-cli"
    executable.write_bytes(b"binary")
    executable.chmod(0o755)
    return executable


def test_qwentts_cpp_preflight_rejects_same_gguf_for_talker_and_tokenizer(
    tmp_path: Path,
) -> None:
    executable = _make_executable(tmp_path)
    shared_gguf = tmp_path / "shared.gguf"
    shared_gguf.write_bytes(VALID_GGUF)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=shared_gguf,
        tokenizer_gguf=shared_gguf,
    )

    assert result.ready is False
    assert any(
        "talker GGUF and tokenizer GGUF must be distinct artifacts" in reason
        for reason in result.blockers
    )


def test_qwentts_cpp_preflight_rejects_identical_gguf_bytes_under_distinct_paths(
    tmp_path: Path,
) -> None:
    executable = _make_executable(tmp_path)
    talker_gguf = tmp_path / "talker.gguf"
    tokenizer_gguf = tmp_path / "tokenizer.gguf"
    talker_gguf.write_bytes(VALID_GGUF)
    tokenizer_gguf.write_bytes(VALID_GGUF)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker_gguf,
        tokenizer_gguf=tokenizer_gguf,
    )

    assert result.ready is False
    assert any(
        "talker GGUF and tokenizer GGUF must be distinct artifacts" in reason
        for reason in result.blockers
    )
