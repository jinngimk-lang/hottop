import json
from pathlib import Path

from pytest import MonkeyPatch

from hottop import pure_c_qwen3_tts_preflight as pure_c_preflight


def test_safetensors_preflight_rejects_header_above_safety_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    path = tmp_path / "model.safetensors"
    header = json.dumps(
        {
            "weight": {
                "dtype": "U8",
                "shape": [1],
                "data_offsets": [0, 1],
            }
        },
        separators=(",", ":"),
    ).encode()
    path.write_bytes(len(header).to_bytes(8, "little") + header + b"\x01")
    monkeypatch.setattr(
        pure_c_preflight,
        "SAFETENSORS_MAX_HEADER_SIZE_BYTES",
        32,
        raising=False,
    )

    identity, blockers = pure_c_preflight._safetensors_identity(
        path,
        label="Pure-C Qwen3-TTS model.safetensors",
    )

    assert identity is not None
    assert "too large" in " ".join(blockers).lower()
