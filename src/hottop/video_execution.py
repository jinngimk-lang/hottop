from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .video_production import VideoProductionConfig


class BackendReadiness(BaseModel):
    backend: str
    ready: bool
    checks: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class VideoExecutionStatus(BaseModel):
    schema_version: Literal["hottop.video-execution-status.v1"] = (
        "hottop.video-execution-status.v1"
    )
    ready: bool
    wan22: BackendReadiness
    motion_canvas: BackendReadiness
    ffmpeg: BackendReadiness
    actions_required: list[str] = Field(default_factory=list)
    auto_install: bool = False
    auto_download_models: bool = False


def _resolve(project_root: Path, configured: str) -> Path:
    path = Path(configured)
    return path if path.is_absolute() else project_root / path


def _wan22_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    if not config.generation_backend.startswith("wan22"):
        return BackendReadiness(backend=config.generation_backend, ready=True)

    missing: list[str] = []
    checks: list[str] = []
    python = shutil.which("python")
    checks.append(f"python={python or 'missing'}")
    if python is None:
        missing.append("python executable")

    repo_dir = project_root / "integrations" / "Wan2.2"
    generator = repo_dir / "generate.py"
    checks.append(f"generate.py={generator}")
    if not generator.is_file():
        missing.append("Wan2.2 repository with generate.py")

    if config.wan22 is None:
        missing.append("Wan2.2 profile configuration")
    else:
        model_dir = _resolve(project_root, config.wan22.model_dir)
        checks.append(f"model_dir={model_dir}")
        if not model_dir.is_dir():
            missing.append("Wan2.2 model directory")

    return BackendReadiness(
        backend=config.generation_backend,
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _motion_canvas_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    if config.compositor_backend != "motion-canvas":
        return BackendReadiness(backend=config.compositor_backend, ready=True)

    missing: list[str] = []
    checks: list[str] = []
    for binary in ("node", "npm"):
        resolved = shutil.which(binary)
        checks.append(f"{binary}={resolved or 'missing'}")
        if resolved is None:
            missing.append(f"{binary} executable")

    if config.motion_canvas is None:
        missing.append("Motion Canvas profile configuration")
    else:
        project_dir = _resolve(project_root, config.motion_canvas.project_dir)
        package_json = project_dir / "package.json"
        checks.append(f"package.json={package_json}")
        if not package_json.is_file():
            missing.append("Motion Canvas project package.json")

    return BackendReadiness(
        backend=config.compositor_backend,
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _ffmpeg_readiness(config: VideoProductionConfig) -> BackendReadiness:
    if config.encoder_backend != "ffmpeg":
        return BackendReadiness(backend=config.encoder_backend, ready=True)
    ffmpeg = shutil.which("ffmpeg")
    return BackendReadiness(
        backend="ffmpeg",
        ready=ffmpeg is not None,
        checks=[f"ffmpeg={ffmpeg or 'missing'}"],
        missing=[] if ffmpeg else ["FFmpeg executable"],
    )


def inspect_video_environment(
    config: VideoProductionConfig,
    *,
    project_root: Path = Path("."),
) -> VideoExecutionStatus:
    """Inspect local video dependencies without installing, downloading, or executing them."""

    root = project_root.resolve()
    wan22 = _wan22_readiness(config, root)
    motion_canvas = _motion_canvas_readiness(config, root)
    ffmpeg = _ffmpeg_readiness(config)

    actions: list[str] = []
    if not wan22.ready:
        actions.append(
            "Configure the operator-controlled Wan2.2 repository/model files; Hottop will not download them."
        )
    if not motion_canvas.ready:
        actions.append(
            "Prepare the Motion Canvas project and Node/npm runtime; Hottop will not install packages automatically."
        )
    if not ffmpeg.ready:
        actions.append(
            "Install or expose FFmpeg in PATH using an operator-approved build before video execution."
        )

    return VideoExecutionStatus(
        ready=wan22.ready and motion_canvas.ready and ffmpeg.ready,
        wan22=wan22,
        motion_canvas=motion_canvas,
        ffmpeg=ffmpeg,
        actions_required=actions,
    )
