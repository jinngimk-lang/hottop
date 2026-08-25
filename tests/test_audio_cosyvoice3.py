from pathlib import Path

import pytest
from pydantic import ValidationError

from hottop.audio_cosyvoice3 import (
    CosyVoice3Error,
    CosyVoice3Request,
    inspect_cosyvoice3_environment,
    render_cosyvoice3_dialogue,
)


def _prepare_runtime(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "CosyVoice"
    model = tmp_path / "models" / "Fun-CosyVoice3-0.5B-2512"
    reference = tmp_path / "voice.wav"
    (root / "cosyvoice" / "cli").mkdir(parents=True)
    (root / "cosyvoice" / "cli" / "cosyvoice.py").write_text("# stub", encoding="utf-8")
    model.mkdir(parents=True)
    (model / "cosyvoice3.yaml").write_text("sample_rate: 24000", encoding="utf-8")
    (model / "llm.pt").write_bytes(b"weights")
    reference.write_bytes(b"wav")
    return root, model, reference


def test_reference_audio_requires_explicit_rights_mode(tmp_path: Path):
    root, model, reference = _prepare_runtime(tmp_path)

    with pytest.raises(ValidationError):
        CosyVoice3Request(
            root=root,
            model_dir=model,
            text="你好，直接开始干活。",
            output=tmp_path / "dialogue.wav",
            reference_audio=reference,
            reference_text="这是原始参考声音。",
        )


def test_readiness_fails_closed_before_upstream_import_when_model_is_missing(tmp_path: Path):
    root, model, reference = _prepare_runtime(tmp_path)
    for path in model.iterdir():
        path.unlink()
    model.rmdir()

    status = inspect_cosyvoice3_environment(
        root=root,
        model_dir=model,
        reference_audio=reference,
    )

    assert status.ready is False
    assert "local CosyVoice3 model directory" in status.missing
    assert status.auto_download_models is False


def test_render_rejects_missing_reference_before_import(tmp_path: Path, monkeypatch):
    root, model, reference = _prepare_runtime(tmp_path)
    reference.unlink()
    imported = False

    def fake_import(*_args, **_kwargs):
        nonlocal imported
        imported = True
        raise AssertionError("upstream import must not happen")

    monkeypatch.setattr("hottop.audio_cosyvoice3.importlib.import_module", fake_import)
    request = CosyVoice3Request(
        root=root,
        model_dir=model,
        text="你好。",
        output=tmp_path / "dialogue.wav",
        reference_audio=reference,
        reference_text="参考文本。",
        reference_rights="generated-original",
    )

    with pytest.raises(CosyVoice3Error, match="reference audio"):
        render_cosyvoice3_dialogue(request)

    assert imported is False


def test_render_uses_local_model_path_and_writes_upstream_audio(tmp_path: Path, monkeypatch):
    root, model, reference = _prepare_runtime(tmp_path)
    seen: dict[str, object] = {}

    class FakeAutoModel:
        def __init__(self, *, model_dir: str):
            seen["model_dir"] = model_dir

        def inference_zero_shot(self, text, reference_text, reference_audio, stream=False):
            seen["call"] = (text, reference_text, reference_audio, stream)
            yield {"tts_speech": [0.0, 0.25, -0.25, 0.0]}

    class FakeModule:
        AutoModel = FakeAutoModel

    monkeypatch.setattr(
        "hottop.audio_cosyvoice3.importlib.import_module",
        lambda name: FakeModule if name == "cosyvoice.cli.cosyvoice" else None,
    )

    output = tmp_path / "dialogue.wav"
    result = render_cosyvoice3_dialogue(
        CosyVoice3Request(
            root=root,
            model_dir=model,
            text="你好，开始工作。",
            output=output,
            reference_audio=reference,
            reference_text="这是一段参考文本。",
            reference_rights="user-provided-rights-cleared",
        )
    )

    assert result == output
    assert seen["model_dir"] == str(model.resolve())
    assert seen["call"] == (
        "你好，开始工作。",
        "这是一段参考文本。",
        str(reference.resolve()),
        False,
    )
    assert output.read_bytes().startswith(b"RIFF")
