# Zero-Cost Video Runtime Design

## Problem

Hottop already has provider-neutral `hottop.render.v2 → hottop.video-plan.v1 → video-run`, local Wan2.2, optional Comfy API v2, MoviePy/FFmpeg composition, style-routed roughness, and first-class dialogue/music/SFX. The missing production capability is a **strictly zero-paid-cost generation route** that can use free shared GPU capacity when available, fail over safely, and never silently convert a free attempt into a paid request.

A previous user-owned repository, `jinngimk-lang/ai-video-director`, already demonstrates several useful mechanisms: Hugging Face ZeroGPU Gradio submit/poll/download, free-quota routing, bounded provider failover, deterministic FFmpeg motion, media/motion quality gates, and a real zero-cost MP4 smoke workflow. Hottop should reuse those behaviors while preserving its Python/provider-neutral contracts instead of copying the older Node application architecture wholesale.

## Goals

- Make `ZERO_COST_MODE=true` the default unattended video-generation policy.
- Add a Hugging Face ZeroGPU generation backend that supports public Gradio queue endpoints without requiring paid credentials.
- Support an ordered list of free candidates and bounded failover per shot.
- Keep credentials optional and environment-only; authenticated free quota may be used only when the operator explicitly provides a token.
- Never enable paid fallback, billing, credit purchase, commercial-license activation, automatic model downloads, or GPU provisioning.
- Validate generated MP4 artifacts before allowing them to feed composition.
- Preserve deterministic MoviePy/FFmpeg production when free GPU is unavailable; the pipeline may degrade or wait, but must never charge.
- Keep code license and model/weights license as separate integration metadata.

## Non-goals

- Hottop will not register accounts, bypass quotas, rotate identities, scrape private APIs, or evade platform limits.
- GitHub-hosted CI is orchestration/verification CPU, not a generative GPU.
- This increment does not promise unlimited free video generation; free shared capacity is inherently bounded and may queue or disappear.
- This increment does not copy AGPL code from OpenMontage or import entire Electron/Node applications such as Toonflow.
- This increment does not make LTX weights a universally safe commercial default. Model-weight license review remains separate from the Apache-2.0 code repository.

## Architecture

### 1. Zero-cost policy and candidate routing

Add `generation_backend: zero-cost-router` and a `zero_cost` config section. The router owns an ordered list of candidate backends. Initial candidate kind is `hf-zerogpu`; later adapters can include rights-compatible free/self-hosted Wan, FramePack, or other engines without changing creative semantics.

Each candidate records only public/runtime metadata: id, kind, public Space URL, API name, profile, dimensions, optional token environment-variable name, anonymous allowance, and an explicit `cost_per_unit: 0`. Any non-zero cost is invalid configuration in zero-cost mode.

Per shot, the runtime submits candidates in order. Retryable queue/network/quota failures move to the next candidate. Non-retryable schema/license/configuration failures stop immediately. Attempts are bounded by configuration. If all candidates fail, execution fails closed with a structured failure list; no paid backend is consulted.

### 2. Hugging Face ZeroGPU adapter

Port the proven Gradio queue behavior from `ai-video-director` into Python using `httpx`:

1. optionally upload an image reference when a future shot supplies one;
2. `POST /gradio_api/call/{api_name}` with `{"data": [...]}`;
3. require an `event_id`;
4. poll `GET /gradio_api/call/{api_name}/{event_id}` as server-sent events;
5. accept only a terminal `complete` event with a downloadable video URL;
6. write through a `.part` file and atomically replace the requested shot output.

The first implementation supports the two already-tested LTX Space profiles from the user-owned project as configurable candidates, but Hottop does not hard-code either as a commercial-rights guarantee. Profile metadata must carry a `weights_license_review` note.

### 3. Quality gate

Port the mature *behavior*, not the Node implementation, of `ai-video-director/src/server/video-quality.js`.

The Python quality gate uses `ffprobe`/`ffmpeg` to verify at minimum:

- a decodable video stream exists;
- duration is non-zero and within configured tolerance when requested;
- width/height/fps can be checked;
- terminal frame is decodable;
- sampled grayscale frames have non-trivial mean delta and are not dominated by duplicate frames.

A failed generation-quality gate deletes the rejected shot and is treated as a retryable candidate failure so the next free candidate may run. Final-output media validation remains deterministic and does not weaken because a style intentionally uses Anti-Polish.

### 4. Deterministic fallback boundary

Free GPU is reserved for visually valuable T2V/I2V shots. Product UI, captions, overlays, simple camera moves, transitions, dialogue/music/SFX and final encoding remain deterministic MoviePy/FFmpeg work. A later increment may add explicit reference-image motion fallback for a failed generative shot. Hottop must never publish a generic mock placeholder as though it were successful generative footage.

### 5. Mature-project reuse policy

- **Directly port behavior from `ai-video-director`:** zero-cost quota/failover semantics, HF ZeroGPU Gradio protocol, media/motion validation, bounded retries, mock-not-final doctrine.
- **Adopt ideas, not code, from OpenMontage (AGPL-3.0):** agentic production decomposition, free/open footage as a legitimate motion source, production quality gates.
- **Evaluate Toonflow (Apache-2.0):** persistent character/storyboard/provider abstraction ideas; do not import its desktop application.
- **Evaluate ViMax (MIT):** director/screenwriter/producer reflection ideas for planning quality.
- **Evaluate FastVideo (Apache-2.0):** future self-hosted inference acceleration when operator GPU exists.
- **Evaluate FramePack (Apache-2.0):** optional low-VRAM I2V backend only after isolated runtime/quality validation.
- **Wan2.2 (Apache-2.0):** preferred rights-simple self-hosted generation family when an operator GPU exists.
- **LTX:** code and weights licenses are tracked separately; later model releases may have additional commercial conditions.

## Configuration sketch

```yaml
generation_backend: zero-cost-router
zero_cost:
  enabled: true
  allow_paid_fallback: false
  max_attempts_per_shot: 2
  quality_gate:
    min_motion_delta: 2.0
    max_duplicate_ratio: 0.6
  candidates:
    - id: hf-ltx23-public
      kind: hf-zerogpu
      profile: ltx23
      space_url: https://lightricks-ltx-2-3.hf.space
      api_name: generate_video
      token_env: HF_TOKEN
      allow_anonymous: true
      cost_per_unit: 0
      weights_license_review: required
```

The token value is never serialized into `hottop.video-plan.v1`, runtime command arguments, logs, or Git.

## Testing and evidence

Implementation is TDD-first. Unit contracts cover zero-cost configuration rejection, candidate order/failover, retryability, secret non-serialization, Gradio SSE parsing/output selection, atomic output, and quality-gate behavior. Exact-head CI must remain green on Python 3.11 and 3.12. Real remote GPU smoke remains optional/bounded because public shared capacity is nondeterministic; it must never be a requirement for ordinary unit CI.

## Security and cost boundary

- `allow_paid_fallback` must remain false in zero-cost profiles.
- Candidates with `cost_per_unit != 0` are invalid.
- Optional authentication uses environment-variable lookup only.
- No automated token creation, billing enrollment, model download, or GPU provisioning.
- Endpoint errors suggesting quota exhaustion are retryable only within configured bounds; exhausting candidates ends the run instead of reaching a paid provider.
- Third-party model/runtime license metadata is an execution precondition, not an assumption inferred from repository code license alone.
