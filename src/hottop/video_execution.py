from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .audio_qwen3_tts import inspect_qwen3_tts_environment
from .rendering import CreativeRenderRequest
from .video_artifacts import VideoArtifactManifest
from .video_final_output import (
    FinalVideoOutputError,
    assert_final_video_output,
    inspect_final_video_output,
)
from .video_production import (
    ExternalCommandSpec,
    VideoProductionConfig,
    VideoProductionPlan,
    build_video_production_plan,
)
from .video_wangp import REFERENCE_PLACEHOLDER


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
    external: BackendReadiness | None = None
    comfy_api: BackendReadiness | None = None
    zero_cost: BackendReadiness | None = None
    software3d: BackendReadiness | None = None
    lightx2v: BackendReadiness | None = None
    voice: BackendReadiness | None = None
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
    audio_dir: str
    plan_path: str
    compositor_manifest_path: str
    composite_output_path: str
    final_output_path: str
    artifact_manifest_paths: list[str] = Field(default_factory=list)
    runtime_commands: list[ExternalCommandSpec] = Field(default_factory=list)
    command_summaries: list[str] = Field(default_factory=list)
    actions_required: list[str] = Field(default_factory=list)


def _resolve(project_root: Path, configured: str) -> Path:
    path = Path(configured)
    return path if path.is_absolute() else project_root / path


def _resolve_espeak_executable() -> tuple[str | None, str | None]:
    """Resolve the guaranteed local speech fallback, preferring native eSpeak-NG."""

    for name in ("espeak-ng", "espeak"):
        resolved = shutil.which(name)
        if resolved is not None:
            return name, resolved
    return None, None


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


def _external_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    if config.generation_backend != "external":
        return BackendReadiness(backend="external", ready=True, checks=["not selected"])

    external = config.external_generation
    if external is None:
        return BackendReadiness(
            backend="external",
            ready=False,
            missing=["external generation profile configuration"],
        )

    missing: list[str] = []
    checks: list[str] = [f"python={sys.executable}"]
    if not Path(sys.executable).is_file():
        missing.append("python executable")

    root = _resolve(project_root, external.root).resolve()
    wgp = root / "wgp.py"
    api = root / "shared" / "api.py"
    settings = _resolve(project_root, external.settings_path).resolve()
    checks.extend(
        [
            f"adapter={external.adapter}",
            f"root={root}",
            f"wgp.py={wgp}",
            f"shared/api.py={api}",
            f"settings={settings}",
            f"cost_per_unit={external.cost_per_unit}",
            f"operator_managed={external.operator_managed}",
            f"auto_install={external.auto_install}",
            f"auto_download_models={external.auto_download_models}",
        ]
    )
    if not wgp.is_file():
        missing.append("WanGP wgp.py")
    if not api.is_file():
        missing.append("WanGP shared/api.py")
    if not settings.is_file():
        missing.append("WanGP exported settings JSON")
    else:
        try:
            payload = json.loads(settings.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            missing.append("valid WanGP exported settings JSON")
        else:
            if not isinstance(payload, dict) or not str(payload.get("model_type") or "").strip():
                missing.append("WanGP settings model_type")

    return BackendReadiness(
        backend=external.adapter,
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _comfy_api_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    if config.generation_backend != "comfy-api-v2":
        return BackendReadiness(backend="comfy-api-v2", ready=True, checks=["not selected"])

    missing: list[str] = []
    checks: list[str] = [f"python={sys.executable}"]
    if not Path(sys.executable).is_file():
        missing.append("python executable")

    adapter = config.comfy_api_v2
    if adapter is None:
        missing.append("Comfy API v2 profile configuration")
    else:
        workflow = _resolve(project_root, adapter.workflow_path).resolve()
        checks.append(f"endpoint={adapter.endpoint}")
        checks.append(f"workflow={workflow}")
        checks.append(f"token_env={adapter.token_env}")
        if not workflow.is_file():
            missing.append("Comfy API workflow JSON")
        if not os.environ.get(adapter.token_env):
            missing.append(f"{adapter.token_env} environment variable")

    return BackendReadiness(
        backend="comfy-api-v2",
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _zero_cost_readiness(config: VideoProductionConfig) -> BackendReadiness:
    if config.generation_backend != "zero-cost-router":
        return BackendReadiness(backend="zero-cost-router", ready=True, checks=["not selected"])

    missing: list[str] = []
    checks: list[str] = [f"python={sys.executable}"]
    if not Path(sys.executable).is_file():
        missing.append("python executable")

    route = config.zero_cost
    if route is None:
        missing.append("zero-cost route configuration")
    else:
        checks.append(f"allow_paid_fallback={route.allow_paid_fallback}")
        checks.append(f"deterministic_reference_fallback={route.deterministic_reference_fallback}")
        checks.append(f"candidate_count={len(route.candidates)}")
        for candidate in route.candidates:
            checks.append(
                f"candidate={candidate.id}; profile={candidate.profile}; space={candidate.space_url}; "
                f"anonymous={candidate.allow_anonymous}; token_env={candidate.token_env or 'none'}"
            )
            if candidate.cost_per_unit != 0:
                missing.append(f"cost-zero candidate required: {candidate.id}")
            if not candidate.allow_anonymous:
                if not candidate.token_env:
                    missing.append(f"token environment variable name for {candidate.id}")
                elif not os.environ.get(candidate.token_env):
                    missing.append(f"{candidate.token_env} environment variable")

    return BackendReadiness(
        backend="zero-cost-router",
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _software3d_readiness(config: VideoProductionConfig) -> BackendReadiness:
    if config.generation_backend != "software3d":
        return BackendReadiness(backend="software3d", ready=True, checks=["not selected"])
    missing: list[str] = []
    checks: list[str] = [f"python={sys.executable}"]
    if not Path(sys.executable).is_file():
        missing.append("python executable")
    ffmpeg = shutil.which("ffmpeg")
    checks.append(f"ffmpeg={ffmpeg or 'missing'}")
    if ffmpeg is None:
        missing.append("FFmpeg executable")
    return BackendReadiness(
        backend="software3d",
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _lightx2v_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    if config.generation_backend != "lightx2v-operator":
        return BackendReadiness(backend="lightx2v-operator", ready=True, checks=["not selected"])

    adapter = config.lightx2v
    if adapter is None:
        return BackendReadiness(
            backend="lightx2v-operator",
            ready=False,
            missing=["LightX2V profile configuration"],
        )

    missing: list[str] = []
    checks: list[str] = [f"python={sys.executable}"]
    if not Path(sys.executable).is_file():
        missing.append("python executable")

    root = _resolve(project_root, adapter.root).resolve()
    infer = root / "lightx2v" / "infer.py"
    model_path = _resolve(project_root, adapter.model_path).resolve()
    config_json = _resolve(project_root, adapter.config_json).resolve()
    checks.extend(
        [
            f"root={root}",
            f"infer.py={infer}",
            f"model_path={model_path}",
            f"config_json={config_json}",
            f"model_cls={adapter.model_cls}",
            f"task={adapter.task}",
            f"code_license={adapter.code_license}",
            f"weights_license={adapter.weights_license}",
            f"cost_per_unit={adapter.cost_per_unit}",
            f"operator_managed={adapter.operator_managed}",
            f"auto_install={adapter.auto_install}",
            f"auto_download_models={adapter.auto_download_models}",
        ]
    )
    if not infer.is_file():
        missing.append("LightX2V operator checkout with lightx2v/infer.py")
    if not model_path.is_dir():
        missing.append("LightX2V local model directory")
    if not config_json.is_file():
        missing.append("LightX2V local config JSON")

    return BackendReadiness(
        backend="lightx2v-operator",
        ready=not missing,
        checks=checks,
        missing=missing,
    )


def _voice_readiness(
    config: VideoProductionConfig,
    project_root: Path,
) -> BackendReadiness:
    backend = config.audio.voice_backend
    if backend == "none":
        return BackendReadiness(backend="none", ready=True, checks=["voice disabled"])
    if backend == "espeak":
        executable, resolved = _resolve_espeak_executable()
        return BackendReadiness(
            backend="espeak",
            ready=resolved is not None,
            checks=[f"{executable or 'espeak-ng'}={resolved or 'missing'}"],
            missing=[] if resolved else ["eSpeak-NG or eSpeak executable"],
        )
    if backend == "qwen3-customvoice":
        adapter = config.audio.qwen3_custom_voice
        if adapter is None:
            return BackendReadiness(
                backend=backend,
                ready=False,
                missing=["Qwen3 CustomVoice profile configuration"],
            )
        model_dir = _resolve(project_root, adapter.model_dir).resolve()
        status = inspect_qwen3_tts_environment(model_dir=model_dir)
        return BackendReadiness(
            backend=backend,
            ready=status.ready,
            checks=[
                f"model_dir={model_dir}",
                f"device={adapter.device}",
                f"dtype={adapter.dtype}",
                f"auto_download_models={status.auto_download_models}",
            ],
            missing=list(status.missing),
        )
    return BackendReadiness(
        backend=backend,
        ready=False,
        checks=["external voice adapter requires explicit operator configuration"],
        missing=["configured external voice adapter"],
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
    """Inspect video dependencies without installing, downloading, uploading, or executing them."""

    root = project_root.resolve()
    wan22 = _wan22_readiness(config, root)
    external = _external_readiness(config, root)
    comfy_api = _comfy_api_readiness(config, root)
    zero_cost = _zero_cost_readiness(config)
    software3d = _software3d_readiness(config)
    lightx2v = _lightx2v_readiness(config, root)
    voice = _voice_readiness(config, root)
    motion_canvas = _motion_canvas_readiness(config, root)
    moviepy = _moviepy_readiness(config)
    ffmpeg = _ffmpeg_readiness(config)

    actions: list[str] = []
    if not wan22.ready:
        actions.append(
            "Configure the operator-controlled Wan2.2 repository/model files; Hottop will not download them."
        )
    if not external.ready:
        actions.append(
            "Prepare the operator-managed WanGP installation and exported settings JSON; Hottop will not install WanGP or download models."
        )
    if not comfy_api.ready:
        actions.append(
            "Configure the operator-approved Comfy API v2 HTTPS endpoint, workflow JSON and token environment variable; Hottop will not create credentials or enable paid usage."
        )
    if not zero_cost.ready:
        actions.append(
            "Configure at least one valid cost-zero video candidate. Anonymous candidates need no token; authenticated free routes use environment variables only. Paid fallback is forbidden."
        )
    if not software3d.ready:
        actions.append(
            "Expose FFmpeg for the deterministic software3d shot encoder; software3d requires no GPU or model download."
        )
    if not lightx2v.ready:
        actions.append(
            "Prepare the operator-managed LightX2V checkout, local model directory and config JSON; Hottop will not install LightX2V or download models."
        )
    if not voice.ready:
        actions.append(
            "Prepare/expose the configured local voice backend and its operator-provisioned model/runtime; Hottop will not install packages or download voice models automatically."
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
        ready=(
            wan22.ready
            and external.ready
            and comfy_api.ready
            and zero_cost.ready
            and software3d.ready
            and lightx2v.ready
            and voice.ready
            and motion_canvas.ready
            and moviepy.ready
            and ffmpeg.ready
        ),
        wan22=wan22,
        external=external,
        comfy_api=comfy_api,
        zero_cost=zero_cost,
        software3d=software3d,
        lightx2v=lightx2v,
        voice=voice,
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


def _wan22_runtime_generation_commands(
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


def _external_runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    external = config.external_generation
    if config.generation_backend != "external" or external is None:
        return []
    if external.adapter != "wangp":
        return []

    root = _resolve(project_root, external.root).resolve()
    settings = _resolve(project_root, external.settings_path).resolve()
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        args = [
            "-m",
            "hottop.video_wangp",
            "--root",
            str(root),
            "--settings",
            str(settings),
            "--prompt",
            shot.generation_prompt,
            "--duration-seconds",
            str(shot.duration_seconds),
            "--fps",
            str(config.fps),
            "--output",
            str((shots_dir / f"shot-{shot.index:03d}.mp4").resolve()),
            "--profile",
            str(external.profile),
            "--attention",
            external.attention,
        ]
        if shot.reference is not None:
            reference_path = _resolve(project_root, shot.reference.image_path).resolve()
            args.extend(
                [
                    "--reference-image",
                    str(reference_path),
                    "--reference-rights",
                    shot.reference.rights,
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


def _comfy_runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    if config.generation_backend != "comfy-api-v2" or config.comfy_api_v2 is None:
        return []
    adapter = config.comfy_api_v2
    workflow = _resolve(project_root, adapter.workflow_path).resolve()
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        commands.append(
            ExternalCommandSpec(
                program=sys.executable,
                args=[
                    "-m",
                    "hottop.video_comfy_api",
                    "--endpoint",
                    adapter.endpoint,
                    "--workflow",
                    str(workflow),
                    "--prompt-node-id",
                    adapter.prompt_node_id,
                    "--prompt-input-name",
                    adapter.prompt_input_name,
                    "--prompt",
                    shot.generation_prompt,
                    "--output",
                    str((shots_dir / f"shot-{shot.index:03d}.mp4").resolve()),
                    "--token-env",
                    adapter.token_env,
                    "--poll-interval-seconds",
                    str(adapter.poll_interval_seconds),
                    "--timeout-seconds",
                    str(adapter.timeout_seconds),
                ],
                cwd=str(project_root.resolve()),
                stage="generation",
            )
        )
    return commands


def _zero_cost_runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    if config.generation_backend != "zero-cost-router" or config.zero_cost is None:
        return []
    runtime_config = (shots_dir.parent / "zero-cost-runtime.json").resolve()
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        output_path = (shots_dir / f"shot-{shot.index:03d}.mp4").resolve()
        artifact_path = (shots_dir / f"shot-{shot.index:03d}.artifact.json").resolve()
        args = [
            "-m",
            "hottop.video_zero_cost",
            "--config",
            str(runtime_config),
            "--prompt",
            shot.generation_prompt,
            "--duration-seconds",
            str(shot.duration_seconds),
            "--output",
            str(output_path),
            "--shot-index",
            str(shot.index),
            "--artifact-manifest",
            str(artifact_path),
        ]
        if config.zero_cost.deterministic_reference_fallback:
            args.append("--allow-deterministic-fallback")
        if shot.reference is not None:
            reference_path = _resolve(project_root, shot.reference.image_path).resolve()
            args.extend(
                [
                    "--reference-image",
                    str(reference_path),
                    "--reference-rights",
                    shot.reference.rights,
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


def _software3d_runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    if config.generation_backend != "software3d":
        return []
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        commands.append(
            ExternalCommandSpec(
                program=sys.executable,
                args=[
                    "-m",
                    "hottop.video_software3d_production",
                    "--shot-index",
                    str(shot.index),
                    "--duration-seconds",
                    str(shot.duration_seconds),
                    "--fps",
                    str(config.fps),
                    "--width",
                    str(config.width),
                    "--height",
                    str(config.height),
                    "--output",
                    str((shots_dir / f"shot-{shot.index:03d}.mp4").resolve()),
                ],
                cwd=str(project_root.resolve()),
                stage="generation",
            )
        )
    return commands


def _lightx2v_runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    adapter = config.lightx2v
    if config.generation_backend != "lightx2v-operator" or adapter is None:
        return []

    root = _resolve(project_root, adapter.root).resolve()
    model_path = _resolve(project_root, adapter.model_path).resolve()
    config_json = _resolve(project_root, adapter.config_json).resolve()
    commands: list[ExternalCommandSpec] = []
    for shot in plan.shots:
        output_path = (shots_dir / f"shot-{shot.index:03d}.mp4").resolve()
        artifact_path = (shots_dir / f"shot-{shot.index:03d}.artifact.json").resolve()
        args = [
            "-m",
            "hottop.video_lightx2v",
            "--root",
            str(root),
            "--model-path",
            str(model_path),
            "--config-json",
            str(config_json),
            "--model-cls",
            adapter.model_cls,
            "--task",
            adapter.task,
            "--seed",
            str(adapter.seed),
            "--prompt",
            shot.generation_prompt,
            "--negative-prompt",
            shot.negative_prompt,
            "--output",
            str(output_path),
            "--shot-index",
            str(shot.index),
            "--artifact-manifest",
            str(artifact_path),
        ]
        if shot.reference is not None:
            reference_path = _resolve(project_root, shot.reference.image_path).resolve()
            args.extend(
                [
                    "--reference-image",
                    str(reference_path),
                    "--reference-rights",
                    shot.reference.rights,
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


def _runtime_generation_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    shots_dir: Path,
) -> list[ExternalCommandSpec]:
    if config.generation_backend == "external":
        return _external_runtime_generation_commands(
            plan,
            config,
            project_root=project_root,
            shots_dir=shots_dir,
        )
    if config.generation_backend == "comfy-api-v2":
        return _comfy_runtime_generation_commands(
            plan,
            config,
            project_root=project_root,
            shots_dir=shots_dir,
        )
    if config.generation_backend == "zero-cost-router":
        return _zero_cost_runtime_generation_commands(
            plan,
            config,
            project_root=project_root,
            shots_dir=shots_dir,
        )
    if config.generation_backend == "software3d":
        return _software3d_runtime_generation_commands(
            plan,
            config,
            project_root=project_root,
            shots_dir=shots_dir,
        )
    if config.generation_backend == "lightx2v-operator":
        return _lightx2v_runtime_generation_commands(
            plan,
            config,
            project_root=project_root,
            shots_dir=shots_dir,
        )
    return _wan22_runtime_generation_commands(
        plan,
        config,
        project_root=project_root,
        shots_dir=shots_dir,
    )


def _runtime_audio_commands(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
    audio_dir: Path,
) -> list[ExternalCommandSpec]:
    dialogue = [cue for cue in plan.audio_cues if cue.kind == "dialogue"]
    commands: list[ExternalCommandSpec] = []
    if config.audio.voice_backend == "espeak":
        from .video_espeak_style import resolve_espeak_dialogue_style

        _, voice_program = _resolve_espeak_executable()
        voice_program = voice_program or "espeak-ng"
        for index, cue in enumerate(dialogue, start=1):
            output = (audio_dir / f"dialogue-{index:03d}.wav").resolve()
            style = resolve_espeak_dialogue_style(
                character=cue.character,
                delivery=cue.delivery,
                base_rate_wpm=config.audio.voice_rate_wpm,
            )
            commands.append(
                ExternalCommandSpec(
                    program=voice_program,
                    args=[
                        "-v",
                        config.audio.voice_language,
                        "-p",
                        str(style.pitch),
                        "-s",
                        str(style.rate_wpm),
                        "-w",
                        str(output),
                        cue.text,
                    ],
                    cwd=str(project_root.resolve()),
                    stage="audio",
                )
            )
        return commands

    if config.audio.voice_backend != "qwen3-customvoice":
        return []
    adapter = config.audio.qwen3_custom_voice
    if adapter is None:
        return []
    model_dir = _resolve(project_root, adapter.model_dir).resolve()
    for index, cue in enumerate(dialogue, start=1):
        output = (audio_dir / f"dialogue-{index:03d}.wav").resolve()
        speaker = adapter.speaker_map.get(cue.character or "", adapter.default_speaker)
        args = [
            "-m",
            "hottop.audio_qwen3_tts",
            "--model-dir",
            str(model_dir),
            "--text",
            cue.text,
            "--speaker",
            speaker,
            "--language",
            adapter.language,
            "--instruct",
            (cue.delivery or "").strip(),
            "--output",
            str(output),
            "--device",
            adapter.device,
            "--dtype",
            adapter.dtype,
        ]
        if adapter.attn_implementation is not None:
            args.extend(["--attn-implementation", adapter.attn_implementation])
        commands.append(
            ExternalCommandSpec(
                program=sys.executable,
                args=args,
                cwd=str(project_root.resolve()),
                stage="audio",
            )
        )
    return commands


def _runtime_compositor_command(
    config: VideoProductionConfig,
    *,
    project_root: Path,
    plan_path: Path,
    shots_dir: Path,
    audio_dir: Path,
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
                "--audio-dir",
                str(audio_dir.resolve()),
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
    audio_dir: Path,
    composite_output: Path,
    final_output: Path,
) -> list[ExternalCommandSpec]:
    commands = _runtime_generation_commands(
        plan,
        config,
        project_root=project_root,
        shots_dir=shots_dir,
    )
    commands.extend(
        _runtime_audio_commands(
            plan,
            config,
            project_root=project_root,
            audio_dir=audio_dir,
        )
    )
    compositor = _runtime_compositor_command(
        config,
        project_root=project_root,
        plan_path=plan_path,
        shots_dir=shots_dir,
        audio_dir=audio_dir,
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
        for flag in ("--save_file", "--output"):
            try:
                output_index = command.args.index(flag) + 1
                return Path(command.args[output_index])
            except (ValueError, IndexError):
                continue
        return None
    if command.stage == "audio":
        for flag in ("-w", "--output"):
            try:
                output_index = command.args.index(flag) + 1
                return Path(command.args[output_index])
            except (ValueError, IndexError):
                continue
        return None
    if command.stage == "compositor":
        return composite_output
    if command.stage == "finalization":
        return final_output
    return None


def _artifact_manifest_path(command: ExternalCommandSpec) -> Path | None:
    if command.stage != "generation":
        return None
    try:
        return Path(command.args[command.args.index("--artifact-manifest") + 1])
    except (ValueError, IndexError):
        pass
    if "hottop.video_software3d_production" in command.args:
        try:
            output = Path(command.args[command.args.index("--output") + 1])
        except (ValueError, IndexError):
            return None
        return output.with_suffix(".artifact.json")
    return None


def _shot_index(command: ExternalCommandSpec) -> int | None:
    try:
        return int(command.args[command.args.index("--shot-index") + 1])
    except (ValueError, IndexError):
        return None


def _prepare_stage_output(stage: str, path: Path | None) -> None:
    if path is None:
        raise VideoExecutionError(f"video {stage} stage has unresolved expected output path")
    if path.exists():
        if not path.is_file():
            raise VideoExecutionError(f"video {stage} stage expected output is not a file: {path}")
        path.unlink()


def _verify_stage_output(stage: str, path: Path | None) -> None:
    if path is None or not path.is_file() or path.stat().st_size <= 0:
        rendered = str(path) if path is not None else "unresolved output path"
        if path is not None and path.is_file():
            path.unlink()
        raise VideoExecutionError(
            f"video {stage} stage did not produce expected output; "
            f"fresh expected output missing: {rendered}"
        )


def _verify_artifact_provenance(
    command: ExternalCommandSpec,
    manifest_path: Path | None,
    output_path: Path | None,
    *,
    config: VideoProductionConfig,
) -> None:
    if manifest_path is None:
        return
    if not manifest_path.is_file() or manifest_path.stat().st_size <= 0:
        raise VideoExecutionError(
            f"video generation artifact provenance is missing or empty: {manifest_path}"
        )
    try:
        manifest = VideoArtifactManifest.model_validate_json(
            manifest_path.read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as exc:
        raise VideoExecutionError(
            f"video generation artifact provenance is invalid: {manifest_path}"
        ) from exc

    if manifest.planned_generation_backend != config.generation_backend:
        raise VideoExecutionError(
            f"video generation artifact provenance planned backend mismatch: {manifest_path}"
        )
    expected_shot_index = _shot_index(command)
    if len(manifest.shots) != 1:
        raise VideoExecutionError(
            f"video generation artifact provenance must describe exactly one shot: {manifest_path}"
        )
    artifact = manifest.shots[0]

    if config.generation_backend == "software3d":
        if artifact.artifact_kind != "deterministic-generated" or artifact.backend != "software3d":
            raise VideoExecutionError(
                f"video generation artifact provenance software3d artifact mismatch: {manifest_path}"
            )
    elif config.generation_backend == "lightx2v-operator":
        expected_backend = (
            f"lightx2v:{config.lightx2v.model_cls}" if config.lightx2v is not None else None
        )
        if artifact.artifact_kind != "ai-generated" or artifact.backend != expected_backend:
            raise VideoExecutionError(
                f"video generation artifact provenance LightX2V artifact mismatch: {manifest_path}"
            )
    elif artifact.artifact_kind == "ai-generated":
        allowed_backends = (
            {candidate.id for candidate in config.zero_cost.candidates}
            if config.generation_backend == "zero-cost-router" and config.zero_cost is not None
            else set()
        )
        if artifact.backend not in allowed_backends:
            raise VideoExecutionError(
                f"video generation artifact provenance artifact backend mismatch: {manifest_path}"
            )
    elif artifact.artifact_kind == "deterministic-non-generative":
        if config.zero_cost is None or not config.zero_cost.deterministic_reference_fallback:
            raise VideoExecutionError(
                f"video generation artifact provenance deterministic fallback not enabled: {manifest_path}"
            )
        if (
            artifact.backend != "deterministic-reference-motion"
            or artifact.degraded_from != "zero-cost-router"
            or artifact.degradation_reason != "zero_cost_routes_exhausted"
        ):
            raise VideoExecutionError(
                f"video generation artifact provenance deterministic fallback backend mismatch: {manifest_path}"
            )
    if expected_shot_index is None or artifact.shot_index != expected_shot_index:
        raise VideoExecutionError(
            f"video generation artifact provenance shot identity mismatch: {manifest_path}"
        )
    if output_path is None or Path(artifact.path).resolve() != output_path.resolve():
        raise VideoExecutionError(
            f"video generation artifact provenance output mismatch: {manifest_path}"
        )


def _has_reference_placeholder(value: object) -> bool:
    if isinstance(value, dict):
        return any(_has_reference_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_reference_placeholder(item) for item in value)
    return value == REFERENCE_PLACEHOLDER


def _generation_reference_actions(
    plan: VideoProductionPlan,
    config: VideoProductionConfig,
    *,
    project_root: Path,
) -> list[str]:
    if config.generation_backend not in {"zero-cost-router", "external", "lightx2v-operator"}:
        return []

    actions: list[str] = []
    if (
        config.generation_backend == "external"
        and config.external_generation is not None
        and config.external_generation.adapter == "wangp"
    ):
        settings_path = _resolve(
            project_root,
            config.external_generation.settings_path,
        ).resolve()
        payload: object | None = None
        if settings_path.is_file():
            try:
                payload = json.loads(settings_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = None
        has_placeholder = _has_reference_placeholder(payload)
        referenced_shots = [shot for shot in plan.shots if shot.reference is not None]
        if referenced_shots and not has_placeholder:
            actions.append(
                "WanGP reference image requires an exported settings reference placeholder "
                f"({REFERENCE_PLACEHOLDER}) before GPU execution."
            )
        if has_placeholder:
            for shot in plan.shots:
                if shot.reference is None:
                    actions.append(
                        f"WanGP settings reference placeholder is configured but shot {shot.index} "
                        "has no reference image."
                    )

    if config.generation_backend == "lightx2v-operator" and config.lightx2v is not None:
        for shot in plan.shots:
            if config.lightx2v.task == "i2v" and shot.reference is None:
                actions.append(f"LightX2V I2V shot {shot.index} requires a rights-safe reference image.")
            if config.lightx2v.task == "t2v" and shot.reference is not None:
                actions.append(f"LightX2V T2V shot {shot.index} must not carry reference-image metadata.")

    for shot in plan.shots:
        if shot.reference is None:
            continue
        reference_path = _resolve(project_root, shot.reference.image_path).resolve()
        if not reference_path.is_file():
            actions.append(f"reference image for shot {shot.index} is missing: {reference_path}")
    return actions


def run_video_production(
    render_request: CreativeRenderRequest,
    config: VideoProductionConfig,
    *,
    output_dir: Path,
    project_root: Path = Path("."),
    execute: bool = False,
) -> VideoRunResult:
    """Materialize a config-driven video workspace and optionally execute trusted configured stages."""

    root = project_root.resolve()
    workspace = output_dir.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    shots_dir = workspace / (config.moviepy.shot_dir if config.moviepy else "shots")
    shots_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = workspace / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    plan = build_video_production_plan(render_request, config)
    plan_path = workspace / "hottop-video-plan.json"
    manifest_path = workspace / "compositor-manifest.json"
    composite_name = config.moviepy.composite_name if config.moviepy else "motion-canvas-output.mp4"
    composite_output = workspace / composite_name
    final_output = workspace / f"hottop-output.{config.output_format}"
    _write_json(plan_path, plan)
    _write_json(manifest_path, plan.compositor_manifest)
    if config.generation_backend == "zero-cost-router" and config.zero_cost is not None:
        _write_json(workspace / "zero-cost-runtime.json", config.zero_cost)

    commands = _runtime_commands(
        plan,
        config,
        project_root=root,
        plan_path=plan_path,
        shots_dir=shots_dir,
        audio_dir=audio_dir,
        composite_output=composite_output,
        final_output=final_output,
    )
    artifact_manifest_paths = [
        str(path.resolve())
        for command in commands
        if command.stage == "generation"
        if (path := _artifact_manifest_path(command)) is not None
    ]
    readiness = inspect_video_environment(config, project_root=root)
    reference_actions = _generation_reference_actions(
        plan,
        config,
        project_root=root,
    )
    actions_required = [*readiness.actions_required, *reference_actions]
    ready = readiness.ready and not reference_actions
    summaries: list[str] = []

    if execute and not ready:
        raise VideoExecutionError(
            "video execution environment is not ready: " + "; ".join(actions_required)
        )

    if execute:
        for command in commands:
            expected_output = _expected_stage_output(
                command,
                composite_output=composite_output,
                final_output=final_output,
            )
            artifact_path = _artifact_manifest_path(command)
            _prepare_stage_output(command.stage, expected_output)
            if artifact_path is not None:
                _prepare_stage_output("artifact provenance", artifact_path)
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
                if artifact_path is not None and artifact_path.is_file():
                    artifact_path.unlink()
                raise VideoExecutionError(
                    f"video {command.stage} stage failed with return code {completed.returncode}"
                )
            _verify_stage_output(command.stage, expected_output)
            if command.stage == "finalization" and config.ffmpeg is not None and expected_output is not None:
                report = inspect_final_video_output(
                    expected_output,
                    config.ffmpeg,
                    runner=subprocess.run,
                )
                try:
                    assert_final_video_output(report)
                except FinalVideoOutputError as exc:
                    if expected_output.is_file():
                        expected_output.unlink()
                    raise VideoExecutionError(
                        f"final output media verification failed: {exc}"
                    ) from exc
            _verify_artifact_provenance(
                command,
                artifact_path,
                expected_output,
                config=config,
            )

    return VideoRunResult(
        execute_requested=execute,
        executed=execute,
        ready=ready,
        output_dir=str(workspace),
        shots_dir=str(shots_dir),
        audio_dir=str(audio_dir),
        plan_path=str(plan_path),
        compositor_manifest_path=str(manifest_path),
        composite_output_path=str(composite_output),
        final_output_path=str(final_output),
        artifact_manifest_paths=artifact_manifest_paths,
        runtime_commands=commands,
        command_summaries=summaries,
        actions_required=actions_required,
    )
