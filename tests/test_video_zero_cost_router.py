import pytest
from hottop.video_zero_cost import ZeroCostRoutesExhaustedError, run_zero_cost_candidates

from hottop.video_hf_zerogpu import ZeroGpuError
from hottop.video_production import ZeroCostCandidateConfig


def _candidate(candidate_id: str) -> ZeroCostCandidateConfig:
    return ZeroCostCandidateConfig(
        id=candidate_id,
        profile="ltx23",
        space_url=f"https://{candidate_id}.hf.space",
        api_name="generate_video",
        allow_anonymous=True,
        cost_per_unit=0,
        weights_license_review="required",
    )


def test_zero_cost_router_fails_over_only_after_retryable_failure():
    candidates = [_candidate("first"), _candidate("second")]
    calls: list[str] = []

    def execute(candidate: ZeroCostCandidateConfig) -> str:
        calls.append(candidate.id)
        if candidate.id == "first":
            raise ZeroGpuError("quota", code="quota", retryable=True)
        return "ok"

    result = run_zero_cost_candidates(candidates, execute, max_attempts=2)

    assert result.value == "ok"
    assert result.candidate_id == "second"
    assert calls == ["first", "second"]
    assert [failure.candidate_id for failure in result.failures] == ["first"]


def test_zero_cost_router_stops_on_nonretryable_failure():
    candidates = [_candidate("first"), _candidate("second")]
    calls: list[str] = []

    def execute(candidate: ZeroCostCandidateConfig) -> str:
        calls.append(candidate.id)
        raise ZeroGpuError("bad schema", code="bad_schema", retryable=False)

    with pytest.raises(ZeroGpuError):
        run_zero_cost_candidates(candidates, execute, max_attempts=2)

    assert calls == ["first"]


def test_zero_cost_router_exhausts_bounded_free_candidates():
    candidates = [_candidate("first"), _candidate("second")]

    def execute(candidate: ZeroCostCandidateConfig) -> str:
        raise ZeroGpuError(f"{candidate.id} busy", code="busy", retryable=True)

    with pytest.raises(ZeroCostRoutesExhaustedError) as exc_info:
        run_zero_cost_candidates(candidates, execute, max_attempts=2)

    assert [failure.candidate_id for failure in exc_info.value.failures] == ["first", "second"]
    assert all(failure.retryable for failure in exc_info.value.failures)


def test_zero_cost_router_respects_attempt_cap():
    candidates = [_candidate("first"), _candidate("second"), _candidate("third")]
    calls: list[str] = []

    def execute(candidate: ZeroCostCandidateConfig) -> str:
        calls.append(candidate.id)
        raise ZeroGpuError("busy", code="busy", retryable=True)

    with pytest.raises(ZeroCostRoutesExhaustedError):
        run_zero_cost_candidates(candidates, execute, max_attempts=2)

    assert calls == ["first", "second"]
