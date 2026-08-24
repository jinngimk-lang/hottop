from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .rendering import CreativeRenderRequest
from .video_production import (
    ExternalCommandSpec,
    VideoProductionConfig,
    VideoProductionPlan,
    build_video_production_plan,
)


class VideoExecutionError(RuntimeError):
    """Raised when a trusted video execution stage cannot proceed safely."""


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
    moviepy: BackendReadiness | None = None
    ffmpeg: BackendReadiness
    actions_required: list[str] = Field(default_factory=list)
    auto_install: bool = False
    auto_download_models: bool = False


class VideoRunResult(BaseModel):
    schema_version: Literal["hottop.video-run.v1"] = "hottop.video-run.v1"
    execute_requested: bool
    executed: bool
    ready: bool
    output_dir: str
    shots_dir: str
    plan_path: str
    compositor_manifest_path: str
    composite_output_path: str
    final_output_path: str
    runtime_commands: list[ExternalCommandSpec] = Field(default_factory=list)
    command_summaries: list[str] = Field(default_factory=list)
    actions_required: list[str] = Field(default_factory=list)


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
        return BackendReadiness(backend="motion-canvas", ready=True, checks=["not selected"])

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
        backend="motion-canvas",
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _moviepy_readiness(config: VideoProductionConfig) -> BackendReadiness:
    if config.compositor_backend != "moviepy":
        return BackendReadiness(backend="moviepy", ready=True, checks=["not selected"])
    available = importlib.util.find_spec("moviepy") is not None
    return BackendReadiness(
        backend="moviepy",
        ready=available and config.moviepy is not None,
        checks=[f"moviepy={'available' if available else 'missing'}"],
        missing=(
            []
            if available and config.moviepy is not None
            else [
                "MoviePy optional dependency"
                if not available
                else "MoviePy profile configuration"
            ]
        ),
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
    moviepy = _moviepy_readiness(config)
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
    if not moviepy.ready:
        actions.append(
            "Install Hottop's optional video dependencies (MoviePy) in the operator-controlled environment."
        )
    if not ffmpeg.ready:
        actions.append(
            "Install or expose FFmpeg in PATH using an operator-approved build before video execution."
        )

    return VideoExecutionStatus(
        ready=wan22.ready and motion_canvas.ready and moviepy.ready and ffmpeg.ready,
        wan22=wan22,
        motion_canvas=motion_canvas,
        moviepy=moviepy,
        ffmpeg=ffmpeg,
        actions_required=actions,
    )


def _write_json(path: Path, value: object) -> None:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    if not config.generation_backend.startswith("wan22") or config.wan22 is None:
        return []
    generator = (project_root / "integrations" / "Wan2.2" / "generate.py").resolve()
    model_dir = _resolve(project_root, config.wan22.model_dir).resolve()
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        args = [
            str(generator),
            "--task",
            config.wan22.task,
            "--size",
            config.wan22.size,
            "--ckpt_dir",
            str(model_dir),
        ]
        if config.wan22.offload_model:
            args.extend(["--offload_model", "True"])
        if config.wan22.convert_model_dtype:
            args.append("--convert_model_dtype")
        args.extend(
            [
                "--prompt",
                shot.generation_prompt,
                "--save_file",
                str((shots_dir / f"shot-{shot.index:03d}.mp4").resolve()),
            ]
        )
        commands.append(
            ExternalCommandSpec(
                program=sys.executable,
                args=args,
                cwd=str(project_root.resolve()),
                stage="generation",
            )
        )
    return commands


def _runtime_compositor_command(
    config: VideoProductionConfig,
    *,
    project_root: Path,
    plan_path: Path,
    shots_dir: Path,
    composite_output: Path,
) -> ExternalCommandSpec | None:
    if config.compositor_backend == "moviepy" and config.moviepy is not None:
        return ExternalCommandSpec(
            program=sys.executable,
            args=[
                "-m",
                "hottop.video_moviepy",
                "--plan",
                str(plan_path.resolve()),
                "--shots-dir",
                str(shots_dir.resolve()),
                "--output",
                str(composite_output.resolve()),
            ],
            cwd=str(project_root.resolve()),
            stage="compositor",
        )
    if config.compositor_backend == "motion-canvas" and config.motion_canvas is not None:
        return ExternalCommandSpec(
            program="npm",
            args=["run", "render", "--", "--plan", str(plan_path.resolve())],
            cwd=str(_resolve(project_root, config.motion_canvas.project_dir).resolve()),
            stage="compositor",
        )
    return None


def _runtime_finalization_command(
    config: VideoProductionConfig,
    *,
    project_root: Path,
    composite_output: Path,
    final_output: Path,
) -> ExternalCommandSpec | None:
    if config.encoder_backend != "ffmpeg" or config.ffmpeg is None:
        return None
    return ExternalCommandSpec(
        program="ffmpeg",
        args=[
            "-y",
            "-i",
            str(composite_output.resolve()),
            "-c:v",
            config.ffmpeg.video_codec,
            "-pix_fmt",
            config.ffmpeg.pixel_format,
            "-c:a",
            config.ffmpeg.audio_codec,
            "-movflags",
            config.ffmpeg.movflags,
            str(final_output.resolve()),
        ],
        cwd=str(project_root.resolve()),
        stage="finalization",
    )


def _runtime_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    plan_path: Path,
    shots_dir: Path,
    composite_output: Path,
    final_output: Path,
) -> list[ExternalCommandSpec]:
    commands = _runtime_generation_commands(
        plan,
        config,
        project_root=project_root,
        shots_dir=shots_dir,
    )
    compositor = _runtime_compositor_command(
        config,
        project_root=project_root,
        plan_path=plan_path,
        shots_dir=shots_dir,
        composite_output=composite_output,
    )
    if compositor is not None:
        commands.append(compositor)
    finalizer = _runtime_finalization_command(
        config,
        project_root=project_root,
        composite_output=composite_output,
        final_output=final_output,
    )
    if finalizer is not None:
        commands.append(finalizer)
    return commands


def _expected_stage_output(
    command: ExternalCommandSpec,
    *,
    composite_output: Path,
    final_output: Path,
) -> Path | None:
    if command.stage == "generation":
        try:
            save_index = command.args.index("--save_file") + 1
            return Path(command.args[save_index])
        except (ValueError, IndexError):
            return None
    if command.stage == "compositor":
        return composite_output
    if command.stage == "finalization":
        return final_output
    return None


def _prepare_stage_output(stage: str, path: Path | None) -> None:
    if path is None:
        raise VideoExecutionError(
            f"video {stage} stage has unresolved expected output path"
        )
    if path.exists():
        if not path.is_file():
            raise VideoExecutionError(
                f"video {stage} stage expected output is not a file: {path}"
            )
        path.unlink()


def _verify_stage_output(stage: str, path: Path | None) -> None:
    if path is None or not path.is_file() or path.stat().st_size <= 0:
        rendered = str(path) if path is not None else "unresolved output path"
        raise VideoExecutionError(
            f"video {stage} stage did not produce expected output; "
            f"fresh expected output missing: {rendered}"
        )


def run_video_production(
    render_request: CreativeRenderRequest,
    config: VideoProductionConfig,
    *,
    output_dir: Path,
    project_root: Path = Path("."),
    execute: bool = False,
) -> VideoRunResult:
    """Materialize a config-driven video workspace and optionally execute trusted local stages."""

    root = project_root.resolve()
    workspace = output_dir.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    shots_dir = workspace / (config.moviepy.shot_dir if config.moviepy else "shots")
    shots_dir.mkdir(parents=True, exist_ok=True)

    plan = build_video_production_plan(render_request, config)
    plan_path = workspace / "hottop-video-plan.json"
    manifest_path = workspace / "compositor-manifest.json"
    composite_name = config.moviepy.composite_name if config.moviepy else "motion-canvas-output.mp4"
    composite_output = workspace / composite_name
    final_output = workspace / f"hottop-output.{config.output_format}"
    _write_json(plan_path, plan)
    _write_json(manifest_path, plan.compositor_manifest)

    commands = _runtime_commands(
        plan,
        config,
        project_root=root,
        plan_path=plan_path,
        shots_dir=shots_dir,
        composite_output=composite_output,
        final_output=final_output,
    )
    readiness = inspect_video_environment(config, project_root=root)
    summaries: list[str] = []

    if execute and not readiness.ready:
        raise VideoExecutionError(
            "video execution environment is not ready: " + "; ".join(readiness.actions_required)
        )

    if execute:
        for command in commands:
            expected_output = _expected_stage_output(
                command,
                composite_output=composite_output,
                final_output=final_output,
            )
            _prepare_stage_output(command.stage, expected_output)
            completed = subprocess.run(
                [command.program, *command.args],
                cwd=command.cwd,
                shell=False,
                capture_output=True,
                text=True,
                check=False,
            )
            summaries.append(
                f"{command.stage}: returncode={completed.returncode}; "
                f"stdout={completed.stdout[-400:]!r}; stderr={completed.stderr[-400:]!r}"
            )
            if completed.returncode != 0:
                if expected_output is not None and expected_output.is_file():
                    expected_output.unlink()
                raise VideoExecutionError(
                    f"video {command.stage} stage failed with return code {completed.returncode}"
                )
            _verify_stage_output(command.stage, expected_output)

    return VideoRunResult(
        execute_requested=execute,
        executed=execute,
        ready=readiness.ready,
        output_dir=str(workspace),
        shots_dir=str(shots_dir),
        plan_path=str(plan_path),
        compositor_manifest_path=str(manifest_path),
        composite_output_path=str(composite_output),
        final_output_path=str(final_output),
        runtime_commands=commands,
        command_summaries=summaries,
        actions_required=readiness.actions_required,
    )
