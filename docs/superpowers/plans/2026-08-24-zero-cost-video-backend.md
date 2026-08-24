# Zero-Cost Hybrid Video Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a zero-paid-fallback Hugging Face ZeroGPU generation path with bounded routing/failover and observable video quality gates to Hottop's existing config-driven video pipeline.

**Architecture:** Extend `hottop.video-plan.v1` with a `zero-cost-hybrid` generation backend that invokes one Python per-shot worker. The worker routes only across reviewed zero-cost profiles, calls a dedicated HF ZeroGPU adapter, validates the downloaded MP4, and either succeeds, moves to the next free route, or fails closed without paid fallback. Existing audio → MoviePy → FFmpeg stages remain unchanged.

**Tech Stack:** Python 3.11/3.12, Pydantic, httpx, FFmpeg/ffprobe, Hugging Face Gradio/ZeroGPU HTTP API, pytest, Ruff, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-24-zero-cost-video-backend-design.md`

## Global Constraints

- Zero-paid-fallback is mandatory: no candidate with non-zero or unknown billing state may run under `free-only`.
- `video-run` remains dry-run by default; actual HTTP generation occurs only under explicit `--execute`.
- Secrets remain environment-only and must not appear in `hottop.video-plan.v1`, `ExternalCommandSpec.args`, command summaries, Git, or CI logs.
- Normal PR CI must not depend on public GPU availability.
- Public ZeroGPU failures may wait/fail over only to another reviewed free route; never to paid credits or billing-enabled APIs.
- Code license and model-weight license metadata are tracked separately.
- Existing dialogue/music/SFX semantics remain intact.
- Mock/placeholder output may be used in tests but must not be represented as a production-generated shot.

---

### Task 1: Add zero-cost generation configuration and plan metadata

**Files:**
- Modify: `src/hottop/video_production.py`
- Create: `config/video/zero-cost-cinematic.yml`
- Test: `tests/test_zero_cost_video_config.py`

**Interfaces:**
- Produces: `GenerationBackend` value `"zero-cost-hybrid"`
- Produces: `ZeroCostRouteProfile`, `ZeroCostVideoConfig`
- Produces: `VideoProductionConfig.zero_cost`
- Produces: `VideoProductionPlan.zero_cost_policy`

- [ ] **Step 1: Write the failing config/serialization test**

```python
from pathlib import Path

from hottop.video_production import load_video_production_config


def test_zero_cost_profile_is_free_only_and_contains_no_secret_value():
    config = load_video_production_config(Path("config/video/zero-cost-cinematic.yml"))

    assert config.generation_backend == "zero-cost-hybrid"
    assert config.zero_cost is not None
    assert config.zero_cost.policy == "free-only"
    assert config.zero_cost.max_attempts_per_shot == 2
    assert config.zero_cost.routes[0].id == "hf-zerogpu-wan22-fast"
    assert config.zero_cost.routes[0].cost_per_unit == 0
    assert "token" not in config.model_dump_json().lower() or "token_env" in config.model_dump_json()
```

Add a plan assertion using an existing `CreativeRenderRequest` fixture:

```python
plan = build_video_production_plan(render_request, config)
assert plan.generation_backend == "zero-cost-hybrid"
assert plan.zero_cost_policy == "free-only"
assert all("hf_" not in arg.lower() or "token" not in arg.lower() for spec in plan.generation_command_specs for arg in spec.args)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
pytest tests/test_zero_cost_video_config.py -q
```

Expected: failure because `zero-cost-hybrid`, `ZeroCostVideoConfig`, the profile file, or `zero_cost_policy` do not exist.

- [ ] **Step 3: Add the minimal typed configuration**

Add to `src/hottop/video_production.py`:

```python
GenerationBackend = Literal[
    "wan22-ti2v-5b",
    "wan22-i2v-a14b",
    "comfy-api-v2",
    "zero-cost-hybrid",
    "external",
]


class ZeroCostRouteProfile(BaseModel):
    id: str
    provider: Literal["hf-zerogpu"]
    endpoint: str
    api_name: str
    capability: Literal["text_to_video", "image_to_video"]
    cost_per_unit: float = Field(default=0, ge=0)
    billing_state: Literal["free", "unknown", "paid"] = "free"
    model_id: str
    code_license: str | None = None
    weight_license: str | None = None
    commercial_use: Literal["reviewed", "review-required", "non-commercial-only"] = "review-required"
    token_env: str | None = None


class ZeroCostVideoConfig(BaseModel):
    policy: Literal["free-only"] = "free-only"
    max_attempts_per_shot: int = Field(default=2, ge=1, le=5)
    fallback: Literal["wait", "reference-motion"] = "wait"
    routes: list[ZeroCostRouteProfile] = Field(min_length=1)
```

Add `zero_cost: ZeroCostVideoConfig | None = None` to `VideoProductionConfig` and `zero_cost_policy: str | None = None` to `VideoProductionPlan`.

Set `zero_cost_policy=config.zero_cost.policy if config.zero_cost else None` in `build_video_production_plan()`.

Create `config/video/zero-cost-cinematic.yml` by copying the current cinematic profile's dimensions/audio/MoviePy/FFmpeg settings and replacing generation config with:

```yaml
generation_backend: zero-cost-hybrid
zero_cost:
  policy: free-only
  max_attempts_per_shot: 2
  fallback: wait
  routes:
    - id: hf-zerogpu-wan22-fast
      provider: hf-zerogpu
      endpoint: https://zerogpu-aoti-wan2-2-14b-fast.hf.space
      api_name: image_to_video
      capability: image_to_video
      cost_per_unit: 0
      billing_state: free
      model_id: Wan2.2-14B-I2V
      code_license: Apache-2.0
      weight_license: review-required
      commercial_use: review-required
    - id: hf-zerogpu-ltx
      provider: hf-zerogpu
      endpoint: https://lightricks-ltx-video-distilled.hf.space
      api_name: text_to_video
      capability: text_to_video
      cost_per_unit: 0
      billing_state: free
      model_id: LTX-Video-distilled
      code_license: Apache-2.0
      weight_license: review-required
      commercial_use: review-required
```

The exact endpoint/API metadata must be verified again before promotion to production; tests validate schema, not external availability.

- [ ] **Step 4: Run focused tests GREEN**

Run:

```bash
pytest tests/test_zero_cost_video_config.py -q
ruff check src/hottop/video_production.py tests/test_zero_cost_video_config.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/hottop/video_production.py config/video/zero-cost-cinematic.yml tests/test_zero_cost_video_config.py
git commit -m "feat: add zero-cost video configuration"
```

---

### Task 2: Port the free quota and candidate router

**Files:**
- Create: `src/hottop/video_zero_cost_router.py`
- Test: `tests/test_video_zero_cost_router.py`

**Interfaces:**
- Consumes: `ZeroCostRouteProfile`
- Produces: `ZeroCostCandidate`, `ZeroCostFailure`, `ZeroCostRoutesExhaustedError`
- Produces: `eligible_zero_cost_routes(routes)`
- Produces: `run_zero_cost_candidates(candidates, execute)`

- [ ] **Step 1: Write routing RED tests**

```python
import pytest

from hottop.video_zero_cost_router import (
    ZeroCostRoutesExhaustedError,
    eligible_zero_cost_routes,
    run_zero_cost_candidates,
)
from hottop.video_production import ZeroCostRouteProfile


def route(route_id: str, *, cost: float = 0, billing: str = "free") -> ZeroCostRouteProfile:
    return ZeroCostRouteProfile(
        id=route_id,
        provider="hf-zerogpu",
        endpoint="https://example.hf.space",
        api_name="text_to_video",
        capability="text_to_video",
        cost_per_unit=cost,
        billing_state=billing,
        model_id="example/model",
        commercial_use="reviewed",
    )


def test_free_only_router_rejects_paid_and_unknown_billing():
    selected = eligible_zero_cost_routes([
        route("free"),
        route("paid", cost=0.01, billing="paid"),
        route("unknown", billing="unknown"),
    ])
    assert [item.id for item in selected] == ["free"]


def test_retryable_failure_advances_but_never_paid():
    attempts = []

    def execute(candidate):
        attempts.append(candidate.id)
        if candidate.id == "a":
            error = RuntimeError("queue busy")
            error.retryable = True
            raise error
        return "ok"

    result = run_zero_cost_candidates([route("a"), route("b")], execute)
    assert result.value == "ok"
    assert attempts == ["a", "b"]


def test_all_free_routes_exhausted_is_structured_failure():
    def execute(candidate):
        error = RuntimeError("busy")
        error.retryable = True
        raise error

    with pytest.raises(ZeroCostRoutesExhaustedError) as exc:
        run_zero_cost_candidates([route("a")], execute)
    assert exc.value.failures[0].candidate_id == "a"
```

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_video_zero_cost_router.py -q
```

Expected: import/module failure.

- [ ] **Step 3: Implement the pure routing module**

Implement dataclasses/Pydantic models with no HTTP calls:

```python
class ZeroCostFailure(BaseModel):
    candidate_id: str
    message: str
    code: str | None = None
    retryable: bool = False


class ZeroCostRoutesExhaustedError(RuntimeError):
    def __init__(self, failures: list[ZeroCostFailure]):
        super().__init__(f"all zero-cost routes failed ({len(failures)})")
        self.failures = failures


def eligible_zero_cost_routes(routes: list[ZeroCostRouteProfile]) -> list[ZeroCostRouteProfile]:
    return [
        route for route in routes
        if route.cost_per_unit == 0 and route.billing_state == "free"
    ]
```

`run_zero_cost_candidates()` must stop immediately on non-retryable error and never inject or discover a paid candidate.

- [ ] **Step 4: Run GREEN**

```bash
pytest tests/test_video_zero_cost_router.py -q
ruff check src/hottop/video_zero_cost_router.py tests/test_video_zero_cost_router.py
```

- [ ] **Step 5: Commit**

```bash
git add src/hottop/video_zero_cost_router.py tests/test_video_zero_cost_router.py
git commit -m "feat: add free-only video route selection"
```

---

### Task 3: Add the Hugging Face ZeroGPU Gradio adapter

**Files:**
- Create: `src/hottop/video_hf_zerogpu.py`
- Test: `tests/test_video_hf_zerogpu.py`

**Interfaces:**
- Consumes: `ZeroCostRouteProfile`, `VideoShot`, optional environment token
- Produces: `HfZeroGpuTask`, `HfZeroGpuResult`
- Produces: `submit_hf_zero_gpu(...)`, `poll_hf_zero_gpu(...)`, `download_hf_zero_gpu_output(...)`

- [ ] **Step 1: Write mocked HTTP RED tests**

Use `httpx.MockTransport` so normal CI has no network dependency.

```python
def test_submit_poll_download_without_token(tmp_path):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, str(request.url)))
        if request.url.path.endswith("/gradio_api/call/text_to_video"):
            return httpx.Response(200, json={"event_id": "evt-1"})
        if request.url.path.endswith("/gradio_api/call/text_to_video/evt-1"):
            return httpx.Response(
                200,
                text='event: complete\ndata: [{"url":"https://files.example/out.mp4"}]\n\n',
                headers={"content-type": "text/event-stream"},
            )
        if request.url.host == "files.example":
            return httpx.Response(200, content=b"fake-mp4-bytes")
        raise AssertionError(request.url)

    output = tmp_path / "shot.mp4"
    result = execute_hf_zero_gpu_profile(..., client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert result == output
    assert output.read_bytes() == b"fake-mp4-bytes"
```

Add a test that a token value passed via environment becomes only an `Authorization` header and is never returned by `repr()`/metadata.

Add retryability classification tests for HTTP 408/409/429/5xx versus hard 4xx.

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_video_hf_zerogpu.py -q
```

- [ ] **Step 3: Implement the adapter**

Port the stable semantics from the user's `ai-video-director` implementation:

```python
RETRYABLE_STATUS = {408, 409, 429}


class HfZeroGpuError(RuntimeError):
    def __init__(self, message: str, *, code: str, retryable: bool):
        super().__init__(message)
        self.code = code
        self.retryable = retryable


def _auth_headers(token: str | None, **extra: str) -> dict[str, str]:
    headers = dict(extra)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers
```

Use the public Gradio lifecycle:

```text
POST {space}/gradio_api/call/{api_name}
GET  {space}/gradio_api/call/{api_name}/{event_id}
```

Parse SSE `complete` and `error` events. Resolve relative file paths against the Space base URL. Write output through `.part` then atomic replace. Never write token values to exception messages.

For milestone 1, support text-to-video request data for the proven LTX-style profile. Wan I2V profile remains config-visible but execution must fail closed with `reference_asset_required` until Task 7/follow-up adds explicit reference assets; do not guess an input image.

- [ ] **Step 4: Run GREEN**

```bash
pytest tests/test_video_hf_zerogpu.py -q
ruff check src/hottop/video_hf_zerogpu.py tests/test_video_hf_zerogpu.py
```

- [ ] **Step 5: Commit**

```bash
git add src/hottop/video_hf_zerogpu.py tests/test_video_hf_zerogpu.py
git commit -m "feat: add Hugging Face ZeroGPU video adapter"
```

---

### Task 4: Add observable media and motion quality gates

**Files:**
- Create: `src/hottop/video_quality.py`
- Test: `tests/test_video_quality.py`
- Test fixtures: generate temporary MP4s inside tests with FFmpeg when available; skip only FFmpeg-dependent cases when binary is absent.

**Interfaces:**
- Produces: `VideoMediaReport`, `VideoMotionReport`
- Produces: `inspect_video_media(path, ...)`
- Produces: `inspect_video_motion(path, ...)`
- Produces: `assert_video_quality(media_report, motion_report | None)`

- [ ] **Step 1: Write RED tests for corrupt, static, and valid clips**

```python
def test_missing_or_corrupt_video_is_rejected(tmp_path):
    bad = tmp_path / "bad.mp4"
    bad.write_bytes(b"not-a-video")
    report = inspect_video_media(bad)
    assert report.pass_ is False


def test_duplicate_ratio_rejects_nearly_static_clip(static_clip):
    motion = inspect_video_motion(static_clip, min_mean_delta=2, max_duplicate_ratio=0.6)
    assert motion.pass_ is False


def test_compatible_clip_with_audio_passes(valid_clip):
    report = inspect_video_media(
        valid_clip,
        require_audio=True,
        allowed_video_codecs={"h264"},
        expected_pixel_format="yuv420p",
    )
    assert report.pass_ is True
```

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_video_quality.py -q
```

- [ ] **Step 3: Implement FFprobe/FFmpeg-based inspection**

Port the old observable checks using `subprocess.run(..., shell=False)` only.

`inspect_video_media()` must parse:

```bash
ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,duration -of json INPUT
```

It must separately decode the terminal frame:

```bash
ffmpeg -hide_banner -loglevel error -sseof -0.25 -i INPUT -frames:v 1 -f null -
```

`inspect_video_motion()` must sample grayscale frames with a bounded low resolution and compute mean absolute frame delta plus duplicate ratio. Keep the first Python port minimal; camera/subject/environment residual analysis may be added in the same file only if the direct port remains understandable and covered.

- [ ] **Step 4: Run GREEN**

```bash
pytest tests/test_video_quality.py -q
ruff check src/hottop/video_quality.py tests/test_video_quality.py
```

- [ ] **Step 5: Commit**

```bash
git add src/hottop/video_quality.py tests/test_video_quality.py
git commit -m "feat: add video media and motion quality gates"
```

---

### Task 5: Add the bounded per-shot zero-cost worker

**Files:**
- Create: `src/hottop/video_zero_cost_worker.py`
- Test: `tests/test_video_zero_cost_worker.py`

**Interfaces:**
- Consumes: serialized route profiles, one shot prompt, expected output path
- Uses: `eligible_zero_cost_routes()`, `run_zero_cost_candidates()`, HF adapter, `inspect_video_media()`, `inspect_video_motion()`
- Produces: fresh validated `shot-NNN.mp4` and `shot-NNN.route.json`

- [ ] **Step 1: Write RED failover and no-fake-success tests**

Inject a fake provider executor:

```python
def test_worker_retries_retryable_free_route_then_succeeds(tmp_path):
    calls = []

    def execute(route, shot, output):
        calls.append(route.id)
        if route.id == "a":
            error = RuntimeError("queue busy")
            error.retryable = True
            raise error
        output.write_bytes(VALID_FIXTURE_BYTES)
        return output

    result = run_zero_cost_shot(..., provider_executor=execute, quality_checker=lambda _: None)
    assert calls == ["a", "b"]
    assert result.output.exists()


def test_worker_never_turns_mock_or_empty_file_into_success(tmp_path):
    ...
    with pytest.raises(ZeroCostRoutesExhaustedError):
        run_zero_cost_shot(...)
```

Add metadata assertion:

```python
metadata = json.loads(result.metadata_path.read_text())
assert metadata["cost"] == 0
assert metadata["route_id"] == "b"
assert "token" not in result.metadata_path.read_text().lower()
```

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_video_zero_cost_worker.py -q
```

- [ ] **Step 3: Implement the worker and CLI**

Primary function:

```python
def run_zero_cost_shot(
    *,
    routes: list[ZeroCostRouteProfile],
    shot: VideoShot,
    output: Path,
    max_attempts: int,
    provider_executor=execute_hf_zero_gpu_profile,
    quality_checker=check_generated_shot,
) -> ZeroCostShotResult:
    ...
```

CLI args:

```text
--routes-json PATH
--shot-json PATH
--output PATH
--max-attempts N
--metadata PATH
```

Delete stale `.part`/output before each attempt. Success requires provider completion **and** quality checker PASS. Quality failure is retryable to the next free candidate unless the report identifies a deterministic configuration error.

- [ ] **Step 4: Run GREEN**

```bash
pytest tests/test_video_zero_cost_worker.py -q
ruff check src/hottop/video_zero_cost_worker.py tests/test_video_zero_cost_worker.py
```

- [ ] **Step 5: Commit**

```bash
git add src/hottop/video_zero_cost_worker.py tests/test_video_zero_cost_worker.py
git commit -m "feat: add zero-cost per-shot generation worker"
```

---

### Task 6: Integrate zero-cost worker with video-plan, video-doctor, and video-run

**Files:**
- Modify: `src/hottop/video_execution.py`
- Modify: `src/hottop/video_production.py`
- Test: `tests/test_video_zero_cost_execution.py`
- Test: `tests/test_video_cli.py`

**Interfaces:**
- Produces: zero-cost runtime `ExternalCommandSpec` for each `VideoShot`
- Extends: `VideoExecutionStatus` with `zero_cost`
- Keeps: `run_video_production(..., execute=False)` side-effect-free with respect to network/process execution

- [ ] **Step 1: Write RED dry-run/runtime command tests**

```python
def test_zero_cost_dry_run_materializes_worker_inputs_without_network(tmp_path, monkeypatch):
    called = False

    def forbidden(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("network/process execution during dry-run")

    monkeypatch.setattr(subprocess, "run", forbidden)
    result = run_video_production(render_request, config, output_dir=tmp_path, execute=False)

    assert called is False
    assert all(spec.program == sys.executable for spec in result.runtime_commands if spec.stage == "generation")
    assert all("hottop.video_zero_cost_worker" in spec.args for spec in result.runtime_commands if spec.stage == "generation")
```

Add a secret regression test where an environment variable contains `super-secret` and assert it never appears in `result.model_dump_json()`, plan JSON, or command summaries.

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_video_zero_cost_execution.py tests/test_video_cli.py -q
```

- [ ] **Step 3: Implement readiness and runtime files**

Add `_zero_cost_readiness()` that checks only:

- Python executable;
- non-empty eligible free route list;
- route metadata validity;
- FFmpeg/ffprobe availability required by the quality gate;
- optional token environment variable only when a selected route explicitly declares that token is required.

Do **not** ping remote endpoints during `video-doctor`; network availability belongs to execution/smoke evidence.

During workspace materialization write:

```text
zero-cost/
  routes.json
  shot-001.json
  shot-002.json
  ...
```

Generation command shape:

```python
ExternalCommandSpec(
    program=sys.executable,
    args=[
        "-m", "hottop.video_zero_cost_worker",
        "--routes-json", str(routes_path),
        "--shot-json", str(shot_path),
        "--output", str(output_path),
        "--metadata", str(metadata_path),
        "--max-attempts", str(config.zero_cost.max_attempts_per_shot),
    ],
    cwd=str(project_root.resolve()),
    stage="generation",
)
```

Ensure `_expected_stage_output()` recognizes `--output` as it already does.

- [ ] **Step 4: Run focused GREEN**

```bash
pytest tests/test_video_zero_cost_execution.py tests/test_video_cli.py -q
ruff check src/hottop/video_execution.py src/hottop/video_production.py tests/test_video_zero_cost_execution.py
```

- [ ] **Step 5: Run the full deterministic test suite**

```bash
pytest -q
ruff check .
```

Expected: full PASS without public network access.

- [ ] **Step 6: Commit**

```bash
git add src/hottop/video_execution.py src/hottop/video_production.py tests/test_video_zero_cost_execution.py tests/test_video_cli.py
git commit -m "feat: route video-run through zero-cost workers"
```

---

### Task 7: Add a separate real ZeroGPU smoke workflow and route provenance

**Files:**
- Create: `.github/workflows/zero-cost-video-smoke.yml`
- Create: `integrations/zero-cost-video-routes.yml`
- Create: `scripts/zero_cost_video_smoke.py`
- Test: `tests/test_zero_cost_route_manifest.py`

**Interfaces:**
- Manifest is discovery/provenance input, not secrets.
- Smoke writes: `result.json`, generated/rejected `smoke.mp4`, `media-report.json`, `motion-report.json`.

- [ ] **Step 1: Write manifest RED test**

```python
def test_route_manifest_separates_code_and_weight_license():
    data = yaml.safe_load(Path("integrations/zero-cost-video-routes.yml").read_text())
    for route in data["routes"]:
        assert route["code_license"]
        assert route["weight_license"]
        assert route["billing_state"] == "free"
        assert route["cost_per_unit"] == 0
        assert route["last_verified"]
```

- [ ] **Step 2: Run RED**

```bash
pytest tests/test_zero_cost_route_manifest.py -q
```

- [ ] **Step 3: Add route manifest**

Use records like:

```yaml
schema_version: hottop.zero-cost-routes.v1
routes:
  - id: hf-zerogpu-ltx
    provider: hf-zerogpu
    endpoint: https://lightricks-ltx-video-distilled.hf.space
    api_name: text_to_video
    capabilities: [text_to_video]
    cost_per_unit: 0
    billing_state: free
    code_license: Apache-2.0
    weight_license: review-required
    commercial_use: review-required
    last_verified: 2026-08-24
    source: jinngimk-lang/ai-video-director proven adapter + fresh Hottop verification
```

Add currently discovered Wan2.2 ZeroGPU candidates as `status: candidate` until their exact API payload and weight license are verified; the worker must not select candidate-only routes.

- [ ] **Step 4: Add a real smoke script**

`scripts/zero_cost_video_smoke.py` must:

1. load one `status: verified` anonymous/free route;
2. generate a 1.5–2 second generic original motion prompt;
3. call `run_zero_cost_shot()`;
4. run media/motion quality checks;
5. write JSON reports;
6. exit non-zero on provider or quality failure;
7. never substitute mock media.

- [ ] **Step 5: Add a non-blocking workflow**

Workflow triggers:

```yaml
on:
  workflow_dispatch:
  push:
    paths:
      - 'src/hottop/video_hf_zerogpu.py'
      - 'src/hottop/video_zero_cost_router.py'
      - 'src/hottop/video_zero_cost_worker.py'
      - 'src/hottop/video_quality.py'
      - 'integrations/zero-cost-video-routes.yml'
      - 'scripts/zero_cost_video_smoke.py'
      - '.github/workflows/zero-cost-video-smoke.yml'
```

Install only project dependencies plus `ffmpeg`; run the smoke; always upload result/rejected evidence via `actions/upload-artifact@v4`. Do not add this workflow as a required PR status check.

- [ ] **Step 6: Run deterministic manifest tests**

```bash
pytest tests/test_zero_cost_route_manifest.py -q
ruff check scripts/zero_cost_video_smoke.py tests/test_zero_cost_route_manifest.py
```

- [ ] **Step 7: Commit**

```bash
git add .github/workflows/zero-cost-video-smoke.yml integrations/zero-cost-video-routes.yml scripts/zero_cost_video_smoke.py tests/test_zero_cost_route_manifest.py
git commit -m "ci: add real zero-cost video smoke"
```

---

### Task 8: Persist doctrine, migration provenance, and exact-head evidence

**Files:**
- Modify: `PROJECT.md`
- Modify: `STATUS.md`
- Modify: `skills/brand-metaphor-creative/SKILL.md`
- Modify: `integrations/versions.yml` or the existing integration provenance file used by current video backends
- Modify: PR #1 body

**Interfaces:**
- Recovery order must expose Zero-Cost Hybrid before future video work.
- Documentation must distinguish verified implementation evidence from route availability assumptions.

- [ ] **Step 1: Update durable doctrine**

Add the stable rule:

> Hottop's preferred no-paid video architecture is Zero-Cost Hybrid: shared free GPU only for high-value generated shots, deterministic local composition/audio/encoding for the rest, and fail-closed wait/degrade behavior when free routes are unavailable. Zero-cost never means license-free, secret-free, or quality-gate-free.

Record `ai-video-director` as a migration/reference source, not a runtime dependency.

- [ ] **Step 2: Update STATUS with exact implementation evidence**

Record only verified commits/workflow runs. If the real ZeroGPU smoke is queued/unavailable, say so explicitly instead of claiming live free generation is green.

- [ ] **Step 3: Run full exact-head verification**

```bash
ruff check .
pytest -q
```

Then verify the exact GitHub Actions run for the current head on Python 3.11 and 3.12.

- [ ] **Step 4: Inspect real smoke evidence separately**

If the ZeroGPU smoke ran:

- fetch workflow jobs;
- fetch artifact metadata;
- confirm the artifact contains the generated/rejected MP4 and reports;
- never call a failed/queued route a production success.

- [ ] **Step 5: Synchronize PR #1**

Update the PR body with:

- zero-cost architecture;
- migrated `ai-video-director` concepts;
- no-paid-fallback invariant;
- quality gate;
- exact deterministic CI run;
- real ZeroGPU smoke status and limitations.

Keep PR draft until Foundation closure criteria are independently reviewed.

- [ ] **Step 6: Commit documentation if tree files changed**

```bash
git add PROJECT.md STATUS.md skills/brand-metaphor-creative/SKILL.md integrations/versions.yml
git commit -m "docs: adopt zero-cost hybrid video production"
```

---

## Plan self-review

- Spec coverage: configuration, free routing, HF provider, bounded worker, deterministic fallback semantics, observable quality, CI smoke, licensing/provenance, docs are each mapped to a task.
- Placeholder scan: implementation steps name concrete functions/files/tests; follow-on reference-asset and higher-quality TTS/music work is explicitly outside milestone 1 rather than left as an in-plan TODO.
- Type consistency: `ZeroCostRouteProfile` is defined in Task 1 and consumed by Tasks 2–7; `run_zero_cost_candidates()` is defined in Task 2; HF execution is Task 3; quality gates are Task 4; `run_zero_cost_shot()` is Task 5; runtime integration is Task 6.
- Safety: no task requires credentials, paid API activation, account creation, model download, or GPU provisioning.