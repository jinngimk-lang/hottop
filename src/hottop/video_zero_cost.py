from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel

from .video_hf_zerogpu import HfZeroGpuRequest, ZeroGpuError, execute_hf_zerogpu
from .video_production import ZeroCostCandidateConfig, ZeroCostConfig
from .video_quality import VideoQualityPolicy, inspect_video_quality
from .video_reference import ReferenceRights

T = TypeVar("T")


class ZeroCostCandidateFailure(BaseModel):
    candidate_id: str
    code: str
    message: str
    retryable: bool


class ZeroCostRouteResult(BaseModel, Generic[T]):
    value: T
    candidate_id: str
    failures: list[ZeroCostCandidateFailure]


class ZeroCostRoutesExhaustedError(RuntimeError):
    """Raised after all permitted free candidates have failed retryably."""

    def __init__(self, failures: list[ZeroCostCandidateFailure]) -> None:
        super().__init__(f"All zero-cost routes failed ({len(failures)})")
        self.failures = failures


def run_zero_cost_candidates(
    candidates: list[ZeroCostCandidateConfig],
    execute: Callable[[ZeroCostCandidateConfig], T],
    *,
    max_attempts: int,
) -> ZeroCostRouteResult[T]:
    """Try only configured cost-zero candidates, in order, within a hard attempt cap."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if not candidates:
        raise ValueError("at least one zero-cost candidate is required")

    failures: list[ZeroCostCandidateFailure] = []
    for candidate in candidates[:max_attempts]:
        if candidate.cost_per_unit != 0:
            raise ValueError(f"zero-cost candidate is not free: {candidate.id}")
        try:
            return ZeroCostRouteResult(
                value=execute(candidate),
                candidate_id=candidate.id,
                failures=failures,
            )
        except ZeroGpuError as exc:
            if not exc.retryable:
                raise
            failures.append(
                ZeroCostCandidateFailure(
                    candidate_id=candidate.id,
                    code=exc.code,
                    message=str(exc),
                    retryable=True,
                )
            )

    raise ZeroCostRoutesExhaustedError(failures)


def load_zero_cost_runtime(path: Path) -> ZeroCostConfig:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ZeroGpuError(
            f"Zero-cost runtime config is not readable JSON: {path}",
            code="zero_cost_invalid_config",
            retryable=False,
        ) from exc
    try:
        return ZeroCostConfig.model_validate(raw)
    except ValueError as exc:
        raise ZeroGpuError(
            f"Zero-cost runtime config is invalid: {path}",
            code="zero_cost_invalid_config",
            retryable=False,
        ) from exc


def _quality_policy(config: ZeroCostConfig) -> VideoQualityPolicy:
    quality = config.quality_gate
    return VideoQualityPolicy(
        min_motion_delta=quality.min_motion_delta,
        max_duplicate_ratio=quality.max_duplicate_ratio,
        sample_fps=quality.sample_fps,
        sample_width=quality.sample_width,
        sample_height=quality.sample_height,
    )


def run_zero_cost_shot(
    config_path: Path,
    *,
    prompt: str,
    duration_seconds: float,
    output: Path,
    env: Mapping[str, str] | None = None,
    reference_image: Path | None = None,
    reference_rights: ReferenceRights | None = None,
) -> Path:
    """Generate one shot through bounded cost-zero candidates only."""

    config = load_zero_cost_runtime(config_path)
    environment = os.environ if env is None else env
    quality_policy = _quality_policy(config)

    def execute(candidate: ZeroCostCandidateConfig) -> Path:
        token = environment.get(candidate.token_env) if candidate.token_env else None
        if not token and not candidate.allow_anonymous:
            raise ZeroGpuError(
                f"required free-route token environment variable is missing: {candidate.token_env}",
                code="zero_cost_missing_token",
                retryable=False,
            )
        request = HfZeroGpuRequest(
            candidate=candidate,
            prompt=prompt,
            duration_seconds=duration_seconds,
            output=output,
            token=token,
            reference_image=reference_image,
            reference_rights=reference_rights,
        )
        generated = execute_hf_zerogpu(request)
        report = inspect_video_quality(generated, quality_policy)
        if not report.pass_:
            generated.unlink(missing_ok=True)
            reasons = "; ".join(report.reasons) or "generated video quality gate failed"
            raise ZeroGpuError(
                f"generated video rejected by quality gate: {reasons}",
                code="zero_cost_quality_rejected",
                retryable=True,
            )
        return generated

    result = run_zero_cost_candidates(
        config.candidates,
        execute,
        max_attempts=config.max_attempts_per_shot,
    )
    return result.value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one video shot through bounded zero-cost routes only"
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--duration-seconds", required=True, type=float)
    parser.add_argument("--output", required=True)
    parser.add_argument("--reference-image")
    parser.add_argument(
        "--reference-rights",
        choices=["generated-original", "user-provided-rights-cleared"],
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        run_zero_cost_shot(
            Path(args.config),
            prompt=args.prompt,
            duration_seconds=args.duration_seconds,
            output=Path(args.output),
            reference_image=Path(args.reference_image) if args.reference_image else None,
            reference_rights=args.reference_rights,
        )
    except (ZeroGpuError, ZeroCostRoutesExhaustedError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
