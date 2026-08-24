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


def run_zero_cost_shot(
    config_path: Path,
    *,
    prompt: str,
    duration_seconds: float,
    output: Path,
    env: Mapping[str, str] | None = None,
) -> Path:
    """Generate one shot through bounded cost-zero candidates only."""

    config = load_zero_cost_runtime(config_path)
    environment = os.environ if env is None else env

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
        )
        return execute_hf_zerogpu(request)

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
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        run_zero_cost_shot(
            Path(args.config),
            prompt=args.prompt,
            duration_seconds=args.duration_seconds,
            output=Path(args.output),
        )
    except (ZeroGpuError, ZeroCostRoutesExhaustedError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
