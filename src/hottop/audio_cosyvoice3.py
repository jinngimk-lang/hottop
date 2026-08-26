from __future__ import annotations

import importlib
import math
import sys
import wave
from array import array
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator

ReferenceRights = Literal["generated-original", "user-provided-rights-cleared"]


class CosyVoice3Error(RuntimeError):
    """Raised when a local CosyVoice3 request cannot be completed safely."""


class CosyVoice3Environment(BaseModel):
    ready: bool
    missing: list[str] = Field(default_factory=list)
    auto_download_models: Literal[False] = False


class CosyVoice3Request(BaseModel):
    root: Path
    model_dir: Path
    text: str = Field(min_length=1)
    output: Path
    reference_audio: Path | None = None
    reference_text: str | None = None
    reference_rights: ReferenceRights | None = None

    @model_validator(mode="after")
    def validate_reference_contract(self) -> CosyVoice3Request:
        if self.reference_audio is not None:
            if self.reference_rights is None:
                raise ValueError("reference audio requires an explicit rights mode")
            if not self.reference_text or not self.reference_text.strip():
                raise ValueError("reference audio requires matching reference text")
        elif self.reference_text is not None or self.reference_rights is not None:
            raise ValueError("reference text/rights require reference audio")
        return self


def inspect_cosyvoice3_environment(
    *,
    root: Path,
    model_dir: Path,
    reference_audio: Path | None = None,
) -> CosyVoice3Environment:
    missing: list[str] = []
    root = root.resolve()
    model_dir = model_dir.resolve()

    if not (root / "cosyvoice" / "cli" / "cosyvoice.py").is_file():
        missing.append("local CosyVoice3 runtime")
    if not model_dir.is_dir():
        missing.append("local CosyVoice3 model directory")
    else:
        if not (model_dir / "cosyvoice3.yaml").is_file():
            missing.append("local CosyVoice3 model config")
        if not any(model_dir.glob("*.pt")) and not any(model_dir.glob("*.safetensors")):
            missing.append("local CosyVoice3 model weights")
    if reference_audio is not None and not reference_audio.resolve().is_file():
        missing.append("reference audio")

    return CosyVoice3Environment(ready=not missing, missing=missing)


@contextmanager
def _runtime_import_path(root: Path):
    root_text = str(root.resolve())
    inserted = root_text not in sys.path
    if inserted:
        sys.path.insert(0, root_text)
    try:
        yield
    finally:
        if inserted:
            try:
                sys.path.remove(root_text)
            except ValueError:
                pass


def _sample_rate(model_dir: Path) -> int:
    config_path = model_dir / "cosyvoice3.yaml"
    try:
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise CosyVoice3Error(f"cannot read CosyVoice3 model config: {config_path}") from exc
    value = payload.get("sample_rate", 24000) if isinstance(payload, dict) else 24000
    try:
        rate = int(value)
    except (TypeError, ValueError) as exc:
        raise CosyVoice3Error("CosyVoice3 sample_rate must be an integer") from exc
    if rate <= 0:
        raise CosyVoice3Error("CosyVoice3 sample_rate must be positive")
    return rate


def _flatten_samples(value: object) -> list[float]:
    current = value
    for attr in ("detach", "cpu"):
        method = getattr(current, attr, None)
        if callable(method):
            current = method()
    numpy_method = getattr(current, "numpy", None)
    if callable(numpy_method):
        current = numpy_method()
    tolist_method = getattr(current, "tolist", None)
    if callable(tolist_method):
        current = tolist_method()

    while isinstance(current, list) and len(current) == 1 and isinstance(current[0], list):
        current = current[0]
    if not isinstance(current, (list, tuple)):
        raise CosyVoice3Error("CosyVoice3 returned unsupported audio samples")
    try:
        return [float(sample) for sample in current]
    except (TypeError, ValueError) as exc:
        raise CosyVoice3Error("CosyVoice3 returned invalid audio samples") from exc


def _write_pcm16_wav(path: Path, samples: list[float], sample_rate: int) -> None:
    if not samples:
        raise CosyVoice3Error("CosyVoice3 returned empty audio")
    if any(not math.isfinite(sample) for sample in samples):
        raise CosyVoice3Error("CosyVoice3 returned non-finite audio samples")
    pcm = array(
        "h",
        (
            int(max(-1.0, min(1.0, sample)) * 32767)
            for sample in samples
        ),
    )
    temporary = path.with_suffix(path.suffix + ".part")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.unlink(missing_ok=True)
    temporary.unlink(missing_ok=True)
    try:
        with wave.open(str(temporary), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(sample_rate)
            handle.writeframes(pcm.tobytes())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def render_cosyvoice3_dialogue(request: CosyVoice3Request) -> Path:
    """Render one rights-safe dialogue line using an already installed local CosyVoice3 runtime."""

    status = inspect_cosyvoice3_environment(
        root=request.root,
        model_dir=request.model_dir,
        reference_audio=request.reference_audio,
    )
    if not status.ready:
        raise CosyVoice3Error("CosyVoice3 environment is not ready: " + ", ".join(status.missing))
    if request.reference_audio is None:
        raise CosyVoice3Error("CosyVoice3 zero-shot dialogue requires reference audio")

    root = request.root.resolve()
    model_dir = request.model_dir.resolve()
    reference_audio = request.reference_audio.resolve()
    sample_rate = _sample_rate(model_dir)

    try:
        with _runtime_import_path(root):
            upstream = importlib.import_module("cosyvoice.cli.cosyvoice")
            auto_model = getattr(upstream, "AutoModel")
            model = auto_model(model_dir=str(model_dir))
            chunks = model.inference_zero_shot(
                request.text.strip(),
                request.reference_text.strip() if request.reference_text else "",
                str(reference_audio),
                stream=False,
            )
            samples: list[float] = []
            for chunk in chunks:
                if not isinstance(chunk, dict) or "tts_speech" not in chunk:
                    raise CosyVoice3Error("CosyVoice3 returned a chunk without tts_speech")
                samples.extend(_flatten_samples(chunk["tts_speech"]))
    except CosyVoice3Error:
        raise
    except Exception as exc:
        raise CosyVoice3Error(f"CosyVoice3 local inference failed: {exc}") from exc

    _write_pcm16_wav(request.output.resolve(), samples, sample_rate)
    return request.output
