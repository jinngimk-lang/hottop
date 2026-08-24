from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

from pydantic import BaseModel

from .video_hf_zerogpu import ZeroGpuError
from .video_production import ZeroCostCandidateConfig

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
