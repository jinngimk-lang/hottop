from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .video_artifacts import VideoArtifactManifest, VideoShotArtifact
from .video_quality import VideoQualityPolicy, VideoQualityReport, inspect_video_quality
from .video_reference import ReferenceRights

_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_UNTRACKED_IMPORTABLE_SUFFIXES = {".py", ".pyc", ".pyd", ".so", ".pth"}


class LightX2VError(RuntimeError):
    """Raised when operator-managed LightX2V cannot run safely."""


class LightX2VAdapterConfig(BaseModel):
    root: Path
    model_path: Path
    config_json: Path
    model_cls: Literal["wan2.2_moe", "wan2.2_moe_distill"]
    task: Literal["t2v", "i2v"]
    seed: int = 42
    code_license: Literal["Apache-2.0"] = "Apache-2.0"
    weights_license: Literal["Apache-2.0"] = "Apache-2.0"
    python_executable: str = Field(default_factory=lambda: sys.executable)
    require_local_model: Literal[True] = True
    auto_install: Literal[False] = False
    auto_download_models: Literal[False] = False
    quality_policy: VideoQualityPolicy = Field(default_factory=VideoQualityPolicy)


def _resolve_python(executable: str) -> str | None:
    candidate = Path(executable)
    if candidate.is_absolute() or candidate.parent != Path("."):
        return str(candidate.resolve()) if candidate.is_file() else None
    return shutil.which(executable)


def _resolve_git_dir(root: Path) -> Path | None:
    marker = root / ".git"
    if marker.is_dir():
        return marker
    if not marker.is_file():
        return None
    try:
        value = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not value.startswith("gitdir:"):
        return None
    target = Path(value.removeprefix("gitdir:").strip())
    return target.resolve() if target.is_absolute() else (root / target).resolve()


def _require_clean_tracked_git_checkout(root: Path) -> None:
    if _resolve_git_dir(root) is None:
        return
    git_executable = shutil.which("git")
    if git_executable is None:
        raise LightX2VError(
            "LightX2V Git checkout cannot be provenance-verified because git is unavailable"
        )
    completed = subprocess.run(
        [
            git_executable,
            "-C",
            str(root),
            "status",
            "--porcelain",
            "--untracked-files=no",
        ],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        suffix = f": {detail[:500]}" if detail else ""
        raise LightX2VError(f"LightX2V Git checkout status could not be verified{suffix}")
    if completed.stdout.strip():
        raise LightX2VError(
            "LightX2V Git checkout has uncommitted tracked changes; commit or revert them "
            "before generation so artifact provenance matches the recorded Git revision"
        )

    untracked = subprocess.run(
        [
            git_executable,
            "-C",
            str(root),
            "ls-files",
            "--others",
            "-z",
        ],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if untracked.returncode != 0:
        detail = (untracked.stderr or untracked.stdout or "").strip()
        suffix = f": {detail[:500]}" if detail else ""
        raise LightX2VError(
            f"LightX2V untracked-file provenance could not be verified{suffix}"
        )
    importable = [
        path
        for path in untracked.stdout.split("\0")
        if path and Path(path).suffix.lower() in _UNTRACKED_IMPORTABLE_SUFFIXES
    ]
    if importable:
        preview = ", ".join(importable[:5])
        raise LightX2VError(
            "LightX2V Git checkout contains untracked importable source/runtime files "
            f"that are not represented by the recorded Git revision: {preview}"
        )

    tracked = subprocess.run(
        [
            git_executable,
            "-C",
            str(root),
            "ls-files",
            "-s",
            "-z",
        ],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if tracked.returncode != 0:
        detail = (tracked.stderr or tracked.stdout or "").strip()
        suffix = f": {detail[:500]}" if detail else ""
        raise LightX2VError(
            f"LightX2V tracked-file provenance could not be verified{suffix}"
        )
    root = root.resolve()
    escaping_symlinks: list[str] = []
    for record in tracked.stdout.split("\0"):
        if not record:
            continue
        try:
            metadata, relative_path = record.split("\t", 1)
        except ValueError as exc:
            raise LightX2VError(
                "LightX2V tracked-file provenance returned an unexpected Git record"
            ) from exc
        mode = metadata.split(" ", 1)[0]
        if mode != "120000":
            continue
        link_path = root / relative_path
        try:
            target = link_path.resolve(strict=False)
            target.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            escaping_symlinks.append(relative_path)
    if escaping_symlinks:
        preview = ", ".join(escaping_symlinks[:5])
        raise LightX2VError(
            "LightX2V Git checkout contains a tracked symlink that resolves outside the "
            f"checkout and is not fully bound by the recorded Git revision: {preview}"
        )


def _preflight(config: LightX2VAdapterConfig) -> None:
    root = config.root.resolve()
    if not (root / "lightx2v" / "infer.py").is_file():
        raise LightX2VError(
            f"LightX2V operator checkout is incomplete: {root / 'lightx2v' / 'infer.py'}"
        )
    _require_clean_tracked_git_checkout(root)
    if not config.model_path.resolve().is_dir():
        raise LightX2VError(f"LightX2V model path is not available locally: {config.model_path}")
    if not config.config_json.resolve().is_file():
        raise LightX2VError(f"LightX2V config JSON is not available locally: {config.config_json}")
    if _resolve_python(config.python_executable) is None:
        raise LightX2VError(f"LightX2V Python executable is not available: {config.python_executable}")


def build_lightx2v_command(
    config: LightX2VAdapterConfig,
    *,
    prompt: str,
    negative_prompt: str,
    output: Path,
    reference_image: Path | None = None,
) -> list[str]:
    command = [
        config.python_executable,
        "-m",
        "lightx2v.infer",
        "--model_cls",
        config.model_cls,
        "--task",
        config.task,
        "--model_path",
        str(config.model_path.resolve()),
        "--config_json",
        str(config.config_json.resolve()),
        "--prompt",
        prompt,
        "--negative_prompt",
        negative_prompt,
        "--seed",
        str(config.seed),
        "--save_result_path",
        str(output.resolve()),
    ]
    if reference_image is not None:
        command.extend(["--image_path", str(reference_image.resolve())])
    return command


def _offline_environment(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    env["HF_DATASETS_OFFLINE"] = "1"
    env["HF_HUB_DISABLE_TELEMETRY"] = "1"
    return env


def _verify_quality(
    output: Path,
    policy: VideoQualityPolicy,
    inspector: Callable[[Path, VideoQualityPolicy], VideoQualityReport],
) -> None:
    try:
        report = inspector(output, policy)
    except Exception as exc:
        output.unlink(missing_ok=True)
        raise LightX2VError(f"LightX2V generated video quality inspection failed: {exc}") from exc
    if report.pass_:
        return
    output.unlink(missing_ok=True)
    reason = "; ".join(report.reasons) or "quality policy rejected the generated video"
    raise LightX2VError(f"LightX2V generated video rejected by quality gate: {reason}")


def _byte_identity(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size_bytes = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size_bytes += len(chunk)
    return digest.hexdigest(), size_bytes


def _generation_request_identity(
    config: LightX2VAdapterConfig,
    *,
    prompt: str,
    negative_prompt: str,
) -> tuple[str, int]:
    payload = json.dumps(
        {
            "schema_version": "hottop.lightx2v-generation-request.v1",
            "model_cls": config.model_cls,
            "task": config.task,
            "seed": config.seed,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest(), len(payload)


def _read_git_revision(root: Path) -> str | None:
    if _resolve_git_dir(root) is None:
        return None
    git_executable = shutil.which("git")
    if git_executable is None:
        return None
    completed = subprocess.run(
        [git_executable, "-C", str(root), "rev-parse", "--verify", "HEAD"],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    revision = completed.stdout.strip()
    return revision if _GIT_SHA_RE.fullmatch(revision) else None


def _local_source_revision(root: Path) -> str:
    git_dir = _resolve_git_dir(root)
    if git_dir is not None:
        git_revision = _read_git_revision(root)
        if git_revision is None:
            raise LightX2VError(
                "LightX2V Git checkout revision could not be provenance-verified"
            )
        return git_revision
    entrypoint = root / "lightx2v" / "infer.py"
    digest, _ = _byte_identity(entrypoint)
    return f"source-sha256:{digest}"


def _require_source_unchanged(root: Path, expected_revision: str) -> None:
    try:
        _require_clean_tracked_git_checkout(root)
        actual_revision = _local_source_revision(root)
    except LightX2VError as exc:
        raise LightX2VError(f"LightX2V source changed during generation: {exc}") from exc
    if actual_revision != expected_revision:
        raise LightX2VError(
            "LightX2V source changed during generation; discard the output and rerun "
            "against one stable operator checkout"
        )


def _require_config_unchanged(
    path: Path,
    expected_sha256: str,
    expected_size_bytes: int,
) -> None:
    try:
        actual_sha256, actual_size_bytes = _byte_identity(path)
    except OSError as exc:
        raise LightX2VError(f"LightX2V config changed during generation: {exc}") from exc
    if actual_sha256 != expected_sha256 or actual_size_bytes != expected_size_bytes:
        raise LightX2VError(
            "LightX2V config changed during generation; discard the output and rerun "
            "against one stable generation config"
        )


def _require_reference_unchanged(
    path: Path,
    expected_sha256: str,
    expected_size_bytes: int,
) -> None:
    try:
        actual_sha256, actual_size_bytes = _byte_identity(path)
    except OSError as exc:
        raise LightX2VError(
            f"LightX2V reference image changed during generation: {exc}"
        ) from exc
    if actual_sha256 != expected_sha256 or actual_size_bytes != expected_size_bytes:
        raise LightX2VError(
            "LightX2V reference image changed during generation; discard the output and rerun "
            "against one stable rights-safe reference image"
        )


def _candidate_id(config: LightX2VAdapterConfig) -> str:
    return f"lightx2v-wan22-{config.task}"


def _write_artifact_manifest(
    *,
    config: LightX2VAdapterConfig,
    candidate_revision: str,
    generation_config_sha256: str,
    generation_config_size_bytes: int,
    generation_request_sha256: str,
    generation_request_size_bytes: int,
    reference_sha256: str | None,
    reference_size_bytes: int | None,
    reference_rights: ReferenceRights | None,
    output: Path,
    shot_index: int,
    manifest_path: Path,
) -> None:
    sha256, size_bytes = _byte_identity(output)
    manifest = VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            VideoShotArtifact(
                shot_index=shot_index,
                path=str(output.resolve()),
                artifact_kind="ai-generated",
                backend=f"lightx2v:{config.model_cls}",
                candidate_id=_candidate_id(config),
                candidate_revision=candidate_revision,
                sha256=sha256,
                size_bytes=size_bytes,
                generation_config_sha256=generation_config_sha256,
                generation_config_size_bytes=generation_config_size_bytes,
                generation_request_sha256=generation_request_sha256,
                generation_request_size_bytes=generation_request_size_bytes,
                reference_sha256=reference_sha256,
                reference_size_bytes=reference_size_bytes,
                reference_rights=reference_rights,
            )
        ],
    )
    manifest_path = manifest_path.resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix(manifest_path.suffix + ".part")
    try:
        temporary.write_text(manifest.model_dump_json(indent=2) + "\n", encoding="utf-8")
        temporary.replace(manifest_path)
    except OSError as exc:
        output.unlink(missing_ok=True)
        manifest_path.unlink(missing_ok=True)
        temporary.unlink(missing_ok=True)
        raise LightX2VError(f"LightX2V artifact provenance write failed: {manifest_path}") from exc


def run_lightx2v_shot(
    config: LightX2VAdapterConfig,
    *,
    prompt: str,
    negative_prompt: str,
    output: Path,
    reference_image: Path | None = None,
    reference_rights: ReferenceRights | None = None,
    shot_index: int | None = None,
    artifact_manifest: Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    quality_inspector: Callable[
        [Path, VideoQualityPolicy], VideoQualityReport
    ] = inspect_video_quality,
) -> Path:
    """Run one already-installed LightX2V Wan2.2 shot in network-offline mode."""

    root = config.root.resolve()
    config = config.model_copy(update={"root": root})
    _preflight(config)
    source_revision = _local_source_revision(root)
    config_json = config.config_json.resolve()
    try:
        generation_config_sha256, generation_config_size_bytes = _byte_identity(config_json)
    except OSError as exc:
        raise LightX2VError(
            f"LightX2V generation config could not be provenance-verified: {config_json}"
        ) from exc
    generation_request_sha256, generation_request_size_bytes = _generation_request_identity(
        config,
        prompt=prompt,
        negative_prompt=negative_prompt,
    )
    output = output.resolve()
    if (shot_index is None) != (artifact_manifest is None):
        raise LightX2VError("LightX2V artifact provenance requires shot_index and artifact_manifest together")
    if shot_index is not None and shot_index < 1:
        raise LightX2VError("LightX2V shot_index must be positive")
    if artifact_manifest is not None:
        artifact_manifest = artifact_manifest.resolve()
        artifact_manifest.unlink(missing_ok=True)

    reference_sha256: str | None = None
    reference_size_bytes: int | None = None
    if config.task == "i2v":
        if reference_image is None or reference_rights not in {
            "generated-original",
            "user-provided-rights-cleared",
        }:
            raise LightX2VError("LightX2V I2V requires one rights-safe reference image")
        reference_image = reference_image.resolve()
        if not reference_image.is_file():
            raise LightX2VError(f"LightX2V reference image is missing: {reference_image}")
        try:
            reference_sha256, reference_size_bytes = _byte_identity(reference_image)
        except OSError as exc:
            raise LightX2VError(
                f"LightX2V reference image could not be provenance-verified: {reference_image}"
            ) from exc
    elif reference_image is not None or reference_rights is not None:
        raise LightX2VError("LightX2V T2V does not accept reference-image metadata")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    command = build_lightx2v_command(
        config,
        prompt=prompt,
        negative_prompt=negative_prompt,
        output=output,
        reference_image=reference_image,
    )
    completed = runner(
        command,
        cwd=root,
        env=_offline_environment(root),
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        output.unlink(missing_ok=True)
        detail = (completed.stderr or completed.stdout or "").strip()
        suffix = f": {detail[:500]}" if detail else ""
        raise LightX2VError(
            f"LightX2V generation failed with return code {completed.returncode}{suffix}"
        )
    try:
        _require_source_unchanged(root, source_revision)
        _require_config_unchanged(
            config_json,
            generation_config_sha256,
            generation_config_size_bytes,
        )
        if reference_image is not None:
            if reference_sha256 is None or reference_size_bytes is None:
                raise LightX2VError(
                    "LightX2V reference image provenance was not captured before generation"
                )
            _require_reference_unchanged(
                reference_image,
                reference_sha256,
                reference_size_bytes,
            )
    except LightX2VError:
        output.unlink(missing_ok=True)
        raise
    if not output.is_file() or output.stat().st_size <= 0:
        output.unlink(missing_ok=True)
        raise LightX2VError("LightX2V completed without the expected non-empty video output")

    _verify_quality(output, config.quality_policy, quality_inspector)
    if artifact_manifest is not None and shot_index is not None:
        _write_artifact_manifest(
            config=config,
            candidate_revision=source_revision,
            generation_config_sha256=generation_config_sha256,
            generation_config_size_bytes=generation_config_size_bytes,
            generation_request_sha256=generation_request_sha256,
            generation_request_size_bytes=generation_request_size_bytes,
            reference_sha256=reference_sha256,
            reference_size_bytes=reference_size_bytes,
            reference_rights=reference_rights,
            output=output,
            shot_index=shot_index,
            manifest_path=artifact_manifest,
        )
    return output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one shot with operator-managed LightX2V")
    parser.add_argument("--root", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--config-json", required=True)
    parser.add_argument("--model-cls", choices=["wan2.2_moe", "wan2.2_moe_distill"], required=True)
    parser.add_argument("--task", choices=["t2v", "i2v"], required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--shot-index", type=int)
    parser.add_argument("--artifact-manifest")
    parser.add_argument("--reference-image")
    parser.add_argument(
        "--reference-rights",
        choices=["generated-original", "user-provided-rights-cleared"],
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config = LightX2VAdapterConfig(
        root=Path(args.root),
        model_path=Path(args.model_path),
        config_json=Path(args.config_json),
        model_cls=args.model_cls,
        task=args.task,
        seed=args.seed,
    )
    try:
        run_lightx2v_shot(
            config,
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            output=Path(args.output),
            reference_image=Path(args.reference_image) if args.reference_image else None,
            reference_rights=args.reference_rights,
            shot_index=args.shot_index,
            artifact_manifest=Path(args.artifact_manifest) if args.artifact_manifest else None,
        )
    except LightX2VError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
