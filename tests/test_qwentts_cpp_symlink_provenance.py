import hashlib
from pathlib import Path

import hottop.qwentts_cpp_preflight as qwentts_preflight
from hottop.qwentts_cpp_preflight import inspect_qwentts_cpp_inputs

VALID_GGUF = (
    b"GGUF"
    + (3).to_bytes(4, "little")
    + (1).to_bytes(8, "little")
    + (0).to_bytes(8, "little")
    + b"fixture-payload"
)


def _write(path: Path, payload: bytes) -> Path:
    path.write_bytes(payload)
    return path


def test_qwentts_cpp_preflight_binds_symlink_target_before_final_identity(
    tmp_path: Path, monkeypatch
) -> None:
    executable = _write(tmp_path / "qwentts-cli", b"binary")
    executable.chmod(0o755)
    target_a = _write(tmp_path / "talker-a.gguf", VALID_GGUF + b"-talker-a")
    target_b = _write(tmp_path / "talker-b.gguf", VALID_GGUF + b"-talker-b")
    talker = tmp_path / "talker.gguf"
    talker.symlink_to(target_a.name)
    tokenizer = _write(tmp_path / "tokenizer.gguf", VALID_GGUF + b"-tokenizer")

    original_snapshot = qwentts_preflight._snapshot_signature
    talker_snapshot_calls = 0

    def retarget_after_second_snapshot(path: Path) -> tuple[int, int, int, int, int, int]:
        nonlocal talker_snapshot_calls
        signature = original_snapshot(path)
        if path == talker:
            talker_snapshot_calls += 1
            if talker_snapshot_calls == 2:
                talker.unlink()
                talker.symlink_to(target_b.name)
        return signature

    monkeypatch.setattr(qwentts_preflight, "_snapshot_signature", retarget_after_second_snapshot)

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker,
        tokenizer_gguf=tokenizer,
    )

    assert result.ready is True
    assert result.talker_gguf is not None
    assert result.talker_gguf.path == str(target_a.resolve())
    assert result.talker_gguf.sha256 == hashlib.sha256(target_a.read_bytes()).hexdigest()
