# Zero-Cost Video Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a strictly free-only, bounded, quality-gated video generation route that reuses proven ZeroGPU/failover ideas from `ai-video-director` without permitting paid fallback.

**Architecture:** Hottop keeps `render.v2 → video-plan.v1 → video-run` as the stable contract. A new `zero-cost-router` generation backend materializes one trusted Python command per shot; that command tries configured free candidates in order, using an HF ZeroGPU Gradio adapter first, validates the generated MP4, and returns success only for a fresh quality-passing artifact. Existing MoviePy/audio/FFmpeg stages remain unchanged.

**Tech Stack:** Python 3.11/3.12, Pydantic, httpx, FFmpeg/ffprobe, pytest, Ruff, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-24-zero-cost-video-runtime-design.md`

## Global Constraints

- `ZERO_COST_MODE=true` behavior must never enable or imply paid fallback.
- `allow_paid_fallback` is false for the zero-cost route; non-zero candidate cost is invalid.
- Secrets remain environment-only; no token value may appear in plan JSON, runtime arguments, Git, or logs.
- No automatic account creation, billing enrollment, model download, GPU provisioning, or quota bypass.
- Public/free endpoint exhaustion is a bounded failure/degradation condition, never a reason to call a paid backend.
- Code license and model/weights license metadata remain separate.
- Ordinary CI must not depend on nondeterministic public GPU availability.

---

### Task 1: Zero-cost configuration and routing contract

**Files:**
- Modify: `src/hottop/video_production.py`
- Create: `tests/test_zero_cost_video_config.py`

**Interfaces:**
- Produces: `ZeroCostCandidateConfig`, `ZeroCostQualityConfig`, `ZeroCostConfig` and `generation_backend="zero-cost-router"`.
- `ZeroCostCandidateConfig` fields: `id`, `kind="hf-zerogpu"`, `profile`, `space_url`, `api_name`, `token_env`, `allow_anonymous`, `cost_per_unit`, `weights_license_review`, `width`, `height`.
- `ZeroCostConfig` fields: `enabled=True`, `allow_paid_fallback=False`, `max_attempts_per_shot`, `candidates`, `quality_gate`.

- [ ] **Step 1: Write the failing tests**

```python
from pydantic import ValidationError
from hottop.video_production import VideoProductionConfig


def test_zero_cost_router_accepts_only_free_candidates(base_video_config):
    raw = {**base_video_config, "generation_backend": "zero-cost-router", "zero_cost": {
        "enabled": True,
        "allow_paid_fallback": False,
        "max_attempts_per_shot": 2,
        "quality_gate": {"min_motion_delta": 2.0, "max_duplicate_ratio": 0.6},
        "candidates": [{
            "id": "hf-ltx23-public", "kind": "hf-zerogpu", "profile": "ltx23",
            "space_url": "https://example.hf.space", "api_name": "generate_video",
            "token_env": "HF_TOKEN", "allow_anonymous": True, "cost_per_unit": 0,
            "weights_license_review": "required", "width": 768, "height": 512,
        }],
    }}
    config = VideoProductionConfig.model_validate(raw)
    assert config.zero_cost.candidates[0].cost_per_unit == 0


def test_zero_cost_router_rejects_paid_fallback(base_video_config):
    raw = {**base_video_config, "generation_backend": "zero-cost-router", "zero_cost": {
        "enabled": True, "allow_paid_fallback": True, "max_attempts_per_shot": 2,
        "candidates": []
    }}
    with pytest.raises(ValidationError):
        VideoProductionConfig.model_validate(raw)
```

- [ ] **Step 2: Run tests and verify RED**

Run: `pytest tests/test_zero_cost_video_config.py -q`
Expected: collection/import/model validation fails because the zero-cost types/backend do not exist.

- [ ] **Step 3: Implement minimal Pydantic models and validation**

Add the exact interfaces above. Validate HTTPS Space URLs, `cost_per_unit == 0`, `allow_paid_fallback is False`, at least one candidate when selected, and positive dimensions/attempt count.

- [ ] **Step 4: Run focused tests and full lint/test**

Run: `ruff check . && pytest tests/test_zero_cost_video_config.py -q && pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add zero-cost video routing config`

---

### Task 2: HF ZeroGPU candidate adapter and bounded free-only router

**Files:**
- Create: `src/hottop/video_hf_zerogpu.py`
- Create: `src/hottop/video_zero_cost.py`
- Modify: `src/hottop/video_execution.py`
- Create: `tests/test_video_hf_zerogpu.py`
- Create: `tests/test_video_zero_cost_router.py`

**Interfaces:**
- `ZeroGpuError(message, *, code: str, retryable: bool)`.
- `HfZeroGpuRequest(candidate, prompt, duration_seconds, output, token)`.
- `execute_hf_zerogpu(request, *, client=None) -> Path`.
- `ZeroCostCandidateFailure(candidate_id, code, message, retryable)`.
- `run_zero_cost_shot(config_path: Path, prompt: str, duration_seconds: float, output: Path, *, client_factory=None) -> Path`.
- Runtime execution creates a workspace `zero-cost-runtime.json` containing only public candidate metadata and token environment-variable names.

- [ ] **Step 1: Write adapter RED tests**

Test a fake httpx client that returns `{event_id}` for submit, SSE `event: complete` for result, and MP4 bytes for download. Assert output is written atomically and token is used only as an Authorization header when present. Add a retryable `429` test and a non-retryable malformed-response test.

- [ ] **Step 2: Verify adapter RED**

Run: `pytest tests/test_video_hf_zerogpu.py -q`
Expected: FAIL because module/API is missing.

- [ ] **Step 3: Implement minimal Gradio queue adapter**

Use `/gradio_api/call/{api_name}` and `/gradio_api/call/{api_name}/{event_id}`. Parse SSE lines without adding a new dependency. Resolve the first video/file URL from the terminal complete payload. Write `.part` then replace output. Never serialize token.

- [ ] **Step 4: Write router RED tests**

Use injected candidate executor: first candidate raises retryable quota error, second writes a valid output; assert order and success. Assert non-retryable first failure stops. Assert all retryable failures produce a structured terminal `ZeroCostRoutesExhaustedError` and never consult any paid backend.

- [ ] **Step 5: Verify router RED**

Run: `pytest tests/test_video_zero_cost_router.py -q`
Expected: FAIL because router API is missing.

- [ ] **Step 6: Implement minimal bounded router**

Load only the generated runtime JSON, resolve optional token by environment-variable name, cap attempts to `max_attempts_per_shot`, and call `execute_hf_zerogpu`. No paid provider registry exists in this module.

- [ ] **Step 7: Integrate runtime command generation**

For `generation_backend == "zero-cost-router"`, `run_video_production` writes `zero-cost-runtime.json` to the workspace and creates one `python -m hottop.video_zero_cost --config ... --prompt ... --duration-seconds ... --output ...` generation command per shot. `inspect_video_environment` requires Python plus candidate metadata but does not require a token when `allow_anonymous=true`.

- [ ] **Step 8: Run focused and full tests**

Run: `ruff check . && pytest tests/test_video_hf_zerogpu.py tests/test_video_zero_cost_router.py -q && pytest -q`
Expected: PASS.

- [ ] **Step 9: Commit**

Commit message: `feat: add free ZeroGPU video router`

---

### Task 3: Generated-video quality gate

**Files:**
- Create: `src/hottop/video_quality.py`
- Modify: `src/hottop/video_zero_cost.py`
- Create: `tests/test_video_quality.py`

**Interfaces:**
- `VideoQualityPolicy(min_motion_delta, max_duplicate_ratio, sample_fps=4, sample_width=96, sample_height=54)`.
- `VideoQualityReport(pass_, duration, width, height, fps, terminal_frame_decodable, mean_motion_delta, duplicate_ratio, reasons)`.
- `inspect_video_quality(path: Path, policy: VideoQualityPolicy, *, runner=subprocess.run) -> VideoQualityReport`.
- `assert_video_quality(report) -> None` raising `VideoQualityError`.

- [ ] **Step 1: Write RED unit tests for pure frame-delta logic and runner contracts**

Test duplicate frames fail, changing frames pass, missing video stream fails, and terminal-frame decode failure is reported.

- [ ] **Step 2: Verify RED**

Run: `pytest tests/test_video_quality.py -q`
Expected: FAIL because module/API is missing.

- [ ] **Step 3: Implement minimal ffprobe/ffmpeg quality inspection**

Use `ffprobe -of json` for media metadata; decode a terminal frame with `ffmpeg -sseof -0.25`; sample grayscale rawvideo at bounded dimensions/fps and compute mean absolute deltas plus duplicate ratio. Do not require OpenCV/Numpy.

- [ ] **Step 4: Integrate with free router**

After each candidate writes a shot, run the quality gate. Delete rejected output and convert quality rejection into a retryable candidate failure so the next free candidate may run. Do not weaken thresholds according to `roughness_score`.

- [ ] **Step 5: Run focused/full verification**

Run: `ruff check . && pytest tests/test_video_quality.py tests/test_video_zero_cost_router.py -q && pytest -q`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: gate free video outputs by media quality`

---

### Task 4: Production profile, upstream radar, doctrine and exact-head CI

**Files:**
- Create: `config/video/cinematic-zero-cost.yml`
- Create: `docs/integrations/zero-cost-video-radar.md`
- Modify: `integrations/versions.yml`
- Modify: `PROJECT.md`
- Modify: `skills/brand-metaphor-creative/SKILL.md`
- Modify: `STATUS.md`
- Modify: PR #1 body
- Create: `tests/test_zero_cost_video_doctrine.py`

**Interfaces:**
- Profile chooses `generation_backend: zero-cost-router`, `style_profile: cinematic`, moderate `roughness_score`, MoviePy, FFmpeg, first-class local audio fallback, and at least one HF ZeroGPU candidate with `cost_per_unit: 0` and explicit weights-license review metadata.

- [ ] **Step 1: Write doctrine/profile RED test**

Assert the profile is free-only, has no paid fallback, preserves audio, and PROJECT/skill state the zero-cost hybrid invariant plus mature-project adoption policy.

- [ ] **Step 2: Verify RED**

Run: `pytest tests/test_zero_cost_video_doctrine.py -q`
Expected: FAIL because profile/doctrine/radar is missing.

- [ ] **Step 3: Add profile and integration radar**

Record: `ai-video-director` behavior sources; HF ZeroGPU; Wan2.2; FramePack; ViMax; Toonflow; FastVideo; OpenMontage architecture-only due AGPL; RIFE/Real-ESRGAN; LTX code-vs-weights license split. Do not claim a candidate production-ready without evidence.

- [ ] **Step 4: Persist project doctrine**

Add the zero-cost hybrid route to PROJECT/skill and STATUS: free GPU for high-value shots, deterministic CPU for the rest, bounded retry/degrade, no paid fallback, quality gates, and ongoing mature-project scanning.

- [ ] **Step 5: Run full exact-head verification**

Run through GitHub Actions on the exact branch head. Require Ruff + pytest success on Python 3.11 and 3.12. A public remote ZeroGPU smoke may be run only as a separately bounded non-required workflow; ordinary CI must remain deterministic.

- [ ] **Step 6: Synchronize PR #1**

Update PR body with exact tested head/run only after exact-head CI is green. Keep PR draft until Foundation closure review is complete.

- [ ] **Step 7: Commit**

Commit message: `docs: persist zero-cost video production path`
