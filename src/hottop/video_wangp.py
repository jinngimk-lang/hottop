from __future__ import annotations

import argparse
import copy
import importlib
import json
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from .video_quality import VideoQualityPolicy, VideoQualityReport, inspect_video_quality
from .video_reference import ReferenceRights

REFERENCE_PLACEHOLDER = "__HOTTOP_REFERENCE_IMAGE__"


class WanGPError(RuntimeError):
    """Raised when an operator-managed WanGP generation cannot be used safely."""


class WanGPAdapterConfig(BaseModel):
    root: Path
    settings_path: Path
    profile: int = Field(default=4, ge=1, le=5)
    attention: str = Field(default="sdpa", min_length=1)
    require_local_model: Literal[True] = True
    auto_download_models: Literal[False] = False
    quality_policy: VideoQualityPolicy = Field(default_factory=VideoQualityPolicy)


def load_wangp_settings(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WanGPError(f"WanGP settings are not readable JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise WanGPError("WanGP settings must contain one JSON object")
    model_type = str(payload.get("model_type") or "").strip()
    if not model_type:
        raise WanGPError("WanGP settings must declare model_type")
    return payload


def _replace_reference_placeholder(value: Any, replacement: str) -> tuple[Any, int]:
    if isinstance(value, dict):
        replaced: dict[Any, Any] = {}
        count = 0
        for key, item in value.items():
            next_item, next_count = _replace_reference_placeholder(item, replacement)
            replaced[key] = next_item
            count += next_count
        return replaced, count
    if isinstance(value, list):
        replaced_items: list[Any] = []
        count = 0
        for item in value:
            next_item, next_count = _replace_reference_placeholder(item, replacement)
            replaced_items.append(next_item)
            count += next_count
        return replaced_items, count
    if value == REFERENCE_PLACEHOLDER:
        return replacement, 1
    return value, 0


def _count_reference_placeholders(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_count_reference_placeholders(item) for item in value.values())
    if isinstance(value, list):
        return sum(_count_reference_placeholders(item) for item in value)
    return int(value == REFERENCE_PLACEHOLDER)


def prepare_wangp_settings(
    template: dict[str, Any],
    *,
    prompt: str,
    duration_seconds: float,
    fps: int,
    reference_image: Path | None = None,
) -> dict[str, Any]:
    """Create one WanGP task from an operator-exported settings template."""

    model_type = str(template.get("model_type") or "").strip()
    if not model_type:
        raise WanGPError("WanGP settings must declare model_type")
    if duration_seconds <= 0:
        raise WanGPError("WanGP shot duration must be greater than zero")
    if fps <= 0:
        raise WanGPError("WanGP shot FPS must be greater than zero")

    settings = copy.deepcopy(template)
    placeholder_count = _count_reference_placeholders(settings)
    if reference_image is None:
        if placeholder_count:
            raise WanGPError(
                "WanGP exported settings contain a Hottop reference placeholder but this shot has no reference image"
            )
    else:
        settings, replaced = _replace_reference_placeholder(
            settings,
            str(reference_image.resolve()),
        )
        if replaced == 0:
            raise WanGPError(
                "WanGP reference image was supplied but exported settings contain no Hottop reference placeholder"
            )

    settings["prompt"] = prompt
    settings["duration_seconds"] = duration_seconds
    settings["video_length"] = f"{duration_seconds:g}s"
    settings["force_fps"] = fps
    return settings


def _create_wangp_session(
    *,
    root: Path,
    output_dir: Path,
    cli_args: list[str],
) -> Any:
    root = root.resolve()
    api_path = root / "shared" / "api.py"
    entrypoint = root / "wgp.py"
    if not api_path.is_file() or not entrypoint.is_file():
        raise WanGPError(
            "WanGP operator installation is incomplete; expected wgp.py and shared/api.py "
            f"under {root}"
        )

    existing = sys.modules.get("shared.api")
    if existing is not None:
        loaded_from = Path(str(getattr(existing, "__file__", ""))).resolve()
        if loaded_from != api_path:
            raise WanGPError(
                f"shared.api is already loaded from {loaded_from}, expected {api_path}"
            )

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    module = importlib.import_module("shared.api")
    loaded_from = Path(str(getattr(module, "__file__", ""))).resolve()
    if loaded_from != api_path:
        raise WanGPError(f"WanGP API loaded from {loaded_from}, expected {api_path}")

    return module.init(
        root=root,
        output_dir=output_dir,
        cli_args=cli_args,
        console_output=True,
    )


def _generated_video_path(result: Any, *, root: Path, output_dir: Path) -> Path:
    if not bool(getattr(result, "success", False)):
        errors = getattr(result, "errors", ()) or ()
        detail = "; ".join(str(error) for error in errors) or "WanGP generation failed"
        raise WanGPError(detail)

    generated_files = getattr(result, "generated_files", ()) or ()
    candidates: list[Path] = []
    for raw in generated_files:
        candidate = Path(str(raw))
        possible = [candidate]
        if not candidate.is_absolute():
            possible.extend([output_dir / candidate, root / candidate])
        for path in possible:
            if path.suffix.lower() in {".mp4", ".webm", ".mov", ".mkv"}:
                candidates.append(path)

    for candidate in candidates:
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate.resolve()
    raise WanGPError("WanGP completed without a readable generated video file")


def _verify_wangp_quality(
    output: Path,
    policy: VideoQualityPolicy,
    inspector: Callable[[Path, VideoQualityPolicy], VideoQualityReport],
) -> None:
    try:
        report = inspector(output, policy)
    except Exception as exc:
        output.unlink(missing_ok=True)
        raise WanGPError(f"WanGP generated video quality inspection failed: {exc}") from exc
    if report.pass_:
        return
    output.unlink(missing_ok=True)
    reason = "; ".join(report.reasons) or "quality policy rejected the generated video"
    raise WanGPError(f"WanGP generated video rejected by quality gate: {reason}")


def run_wangp_shot(
    config: WanGPAdapterConfig,
    *,
    prompt: str,
    duration_seconds: float,
    fps: int,
    output: Path,
    reference_image: Path | None = None,
    reference_rights: ReferenceRights | None = None,
    session_factory: Callable[..., Any] = _create_wangp_session,
    quality_inspector: Callable[
        [Path, VideoQualityPolicy], VideoQualityReport
    ] = inspect_video_quality,
) -> Path:
    """Run one operator-managed WanGP shot without allowing model auto-provisioning."""

    if reference_image is not None:
        reference_image = reference_image.resolve()
        if reference_rights not in {"generated-original", "user-provided-rights-cleared"}:
            raise WanGPError("WanGP reference image requires explicit rights-safe metadata")
        if not reference_image.is_file():
            raise WanGPError(f"WanGP reference image is missing: {reference_image}")
    elif reference_rights is not None:
        raise WanGPError("WanGP reference rights were supplied without a reference image")

    template = load_wangp_settings(config.settings_path)
    settings = prepare_wangp_settings(
        template,
        prompt=prompt,
        duration_seconds=duration_seconds,
        fps=fps,
        reference_image=reference_image,
    )
    root = config.root.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    cli_args = ["--profile", str(config.profile), "--attention", config.attention]
    session = session_factory(root=root, output_dir=output.parent, cli_args=cli_args)

    model_type = str(settings["model_type"])
    availability = session.get_model_availability(model_type)
    if not isinstance(availability, dict) or not bool(availability.get("available", False)):
        status = availability.get("status") if isinstance(availability, dict) else "unknown"
        raise WanGPError(
            f"WanGP model {model_type!r} is not available locally (status={status}); "
            "Hottop will not submit the task because that could trigger model provisioning"
        )

    result = session.submit_task(settings).result()
    source = _generated_video_path(result, root=root, output_dir=output.parent)
    if source != output:
        partial = output.with_suffix(output.suffix + ".part")
        partial.unlink(missing_ok=True)
        try:
            shutil.copyfile(source, partial)
            if partial.stat().st_size <= 0:
                raise WanGPError("WanGP copied output is empty")
            os.replace(partial, output)
        except Exception:
            partial.unlink(missing_ok=True)
            raise

    _verify_wangp_quality(output, config.quality_policy, quality_inspector)
    return output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one shot using operator-managed WanGP")
    parser.add_argument("--root", required=True)
    parser.add_argument("--settings", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--duration-seconds", required=True, type=float)
    parser.add_argument("--fps", required=True, type=int)
    parser.add_argument("--output", required=True)
    parser.add_argument("--profile", type=int, default=4)
    parser.add_argument("--attention", default="sdpa")
    parser.add_argument("--reference-image")
    parser.add_argument(
        "--reference-rights",
        choices=["generated-original", "user-provided-rights-cleared"],
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config = WanGPAdapterConfig(
        root=Path(args.root),
        settings_path=Path(args.settings),
        profile=args.profile,
        attention=args.attention,
    )
    try:
        run_wangp_shot(
            config,
            prompt=args.prompt,
            duration_seconds=args.duration_seconds,
            fps=args.fps,
            output=Path(args.output),
            reference_image=Path(args.reference_image) if args.reference_image else None,
            reference_rights=args.reference_rights,
        )
    except WanGPError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
