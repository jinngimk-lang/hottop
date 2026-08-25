# Zero-Cost Hybrid Video Backend Design

## Goal

Add a production-capable **zero-paid-fallback video generation path** to Hottop that can use shared free GPU capacity when available, degrade safely when it is not, and preserve Hottop's existing config-driven story, style, audio, composition, encoding, and quality contracts.

The first implementation milestone is deliberately narrow: migrate the proven zero-cost routing ideas from `jinngimk-lang/ai-video-director` into Hottop's Python architecture and prove `render.v2 → video-plan → zero-cost shot generation → audio → MoviePy → FFmpeg → quality gate` without introducing a billing-enabled provider.

## Accepted direction

Use a **Zero-Cost Hybrid** architecture rather than a single free endpoint or a pure-local-only architecture.

- Shared Hugging Face ZeroGPU routes are optional free generation workers, not a guaranteed service.
- Scarce free GPU time is reserved for high-value action, transformation, character, or hero shots.
- Deterministic CPU/local stages remain responsible for captions, product UI, simple camera motion, transitions, audio mixing, and final encoding.
- When all verified free GPU routes are exhausted or unavailable, Hottop waits/fails closed or degrades only to an explicitly configured deterministic local route. It never changes to paid credits, billing-enabled API calls, account registration, quota bypass, or undocumented/private endpoints.
- Existing `comfy-api-v2` stays as an optional self-hosted/operator-controlled adapter. It is not the default zero-cost cloud route.

## Why this approach

### Option A — Zero-Cost Hybrid — selected

Pros: works without the user owning a GPU, does not spend shared GPU on every second of footage, survives endpoint churn, preserves deterministic audio/composition, and fits the existing provider-neutral Hottop plan/execution design.

Cons: free endpoints can queue, disappear, or change their Gradio schema; production latency is not guaranteed.

### Option B — Pure local open models

Pros: strongest privacy and determinism after setup.

Cons: requires user-controlled GPU/model storage and therefore cannot be Hottop's universal zero-cost default.

### Option C — Free-cloud swarm only

Pros: no local GPU requirement.

Cons: too brittle to be the sole architecture because public Spaces can pause, queue, or change API shapes.

## Existing assets to reuse

The private `ai-video-director` project already proves several mechanisms worth porting semantically:

- Hugging Face ZeroGPU Gradio submit/poll/download handling;
- free quota ledger and provider routing;
- bounded retry/failover per shot;
- deterministic FFmpeg camera-motion fallback;
- output media/motion quality inspection;
- a separate real ZeroGPU smoke workflow that does not weaken normal CI.

Hottop will **port the behavior into focused Python modules** instead of importing the old Node application wholesale. This keeps Hottop's `pydantic` schemas, `hottop.video-plan.v1`, `video-run`, dry-run-first safety contract, and Python test suite canonical.

## Architecture

```text
hottop.render.v2
      ↓
VideoProductionConfig
      ↓
hottop.video-plan.v1
      ↓
zero-cost shot router
  ├── verified HF ZeroGPU candidate A
  ├── verified HF ZeroGPU candidate B
  └── explicit deterministic fallback / wait
      ↓
shot-NNN.mp4
      ↓
media + motion quality gate
      ↓
voice / music / SFX
      ↓
MoviePy headless composition
      ↓
FFmpeg H.264 + AAC + yuv420p + fast-start
      ↓
final media quality gate
      ↓
hottop-output.mp4
```

## Component boundaries

### 1. Zero-cost configuration

Extend `VideoProductionConfig` with a new generation backend `zero-cost-hybrid` and a `ZeroCostVideoConfig` object.

The config contains only non-secret routing data:

- `policy = free-only`;
- ordered route profile ids;
- max attempts per shot;
- wait/fallback behavior;
- provider-specific endpoint/profile metadata;
- license-review metadata separate from code license metadata.

No token value, cookie, billing account, or credential may be serialized into `hottop.video-plan.v1`.

### 2. Provider-neutral zero-cost router

Create a focused Python routing module responsible for:

- candidate eligibility;
- free-capacity accounting;
- fixed priority/quality ordering;
- bounded retry and failure records;
- rejecting any candidate with non-zero declared cost or unknown billing state when `free-only` is active.

It must not perform HTTP requests itself.

### 3. Hugging Face ZeroGPU adapter

Create a provider module with one responsibility: execute one approved Gradio/ZeroGPU profile.

The adapter supports the same lifecycle as the proven old implementation:

```text
submit → remote event id → poll → completed video URL → download
```

The first profiles may include currently running public ZeroGPU video Spaces discovered by the technology radar, including Wan2.2 image-to-video routes and the previously proven LTX route. A route is selectable only after its exact endpoint/API schema and model-weight license metadata are recorded. Endpoint discovery is not mixed into generation execution.

Authentication, when a free account token is optionally used, is environment-only. Anonymous execution must remain supported for profiles that allow it.

### 4. Per-shot zero-cost worker

Add one executable Python module invoked by the existing structured `ExternalCommandSpec` runtime.

For one shot it:

1. loads the selected zero-cost profile set;
2. tries eligible candidates in deterministic order;
3. submits/polls/downloads;
4. validates fresh non-empty media;
5. runs the shot quality gate;
6. records route/failure metadata;
7. returns success only after a valid MP4 exists.

Retry count is bounded. Retryable provider failures may advance to the next verified free candidate. Non-retryable errors fail immediately.

### 5. Deterministic fallback

The first milestone will not fabricate a fake generated scene when all GPU routes fail. Safe fallback behavior is one of:

- `wait`: fail with structured `zero_cost_routes_exhausted` and preserve the workspace for a later retry;
- `reference-motion`: only when a rights-cleared/local image or video reference is explicitly available for that shot, use deterministic FFmpeg/MoviePy camera motion.

A text placeholder/mock may exist for tests and previews, but it must never be marked as a production-generated shot.

### 6. Quality gate

Port the observable checks from `ai-video-director` into Python rather than trusting provider success.

Minimum production gate:

- output file exists and is non-empty;
- video stream exists and is decodable;
- expected duration tolerance;
- expected width/height/fps when the profile guarantees them;
- H.264/yuv420p final compatibility after Hottop finalization;
- terminal frame decodes;
- frame-change mean delta;
- duplicate-frame ratio;
- optional camera/subject/environment motion checks for prompts whose domain requires movement;
- final output has decodable audio when audio is required.

Generation output and final Hottop output are checked separately. A deliberately rough visual style may pass; a broken/static/corrupt file may not.

### 7. Audio remains first-class

This milestone does not replace the existing free audio baseline:

- `espeak` Mandarin dialogue;
- Hottop synthetic/original music;
- procedural Foley/SFX;
- MoviePy mixing and dialogue ducking.

The zero-cost generation layer must preserve the existing `speaker`, `delivery`, `music_profile`, `sfx_profile`, timing, and `original_music_only` semantics. Higher-quality genuinely free/local voice and music adapters are a follow-on subsystem after the generation path is proven.

## Route licensing and provenance

Code license and model-weight license are tracked separately.

Every production-eligible route record must include:

- upstream project/repository;
- endpoint/Space identifier;
- code license when relevant;
- model/checkpoint identifier;
- model-weight license or `review-required` state;
- capabilities (`text_to_video`, `image_to_video`, audio support, first/last-frame support);
- anonymous/free-token behavior;
- last verified date.

`free-only` means **zero monetary charge**, not "ignore licensing." A route with unresolved commercial-use terms may be used only for explicitly non-commercial smoke/research until reviewed for the intended promotional use.

## Security and cost invariants

- No paid fallback.
- No credit-card or billing activation.
- No account creation or Sybil/quota bypass.
- No private/undocumented API scraping.
- No secrets in Git, plan JSON, runtime command summaries, or CI logs.
- No automatic model downloads or GPU provisioning.
- No arbitrary local-file upload to a remote provider; image references must be explicit rights-cleared inputs under a later reference-asset contract.
- `video-run` stays dry-run by default; network execution only happens under explicit `--execute`.

## CI and real smoke strategy

Normal PR CI remains deterministic and does not depend on public GPU availability. It uses mocked HTTP/provider contracts and fixture MP4s.

A separate **Zero-Cost Video Smoke** workflow may call one explicitly verified public ZeroGPU route with paid fallback disabled. It uploads generated/rejected artifacts and quality reports. External queue exhaustion is reported as route unavailability, not converted into a passing fake video.

The smoke workflow is evidence, not a required merge check unless Hottop later has a sufficiently stable free route.

## Rollout

### Milestone 1 — this design

- zero-cost config and routing core;
- HF ZeroGPU adapter;
- per-shot worker;
- integration with `video-run`;
- media/motion quality gate;
- separate real smoke workflow;
- route/license metadata.

### Follow-on milestones

- explicit keyframe/reference-asset contract for character consistency;
- Wan2.2 first/last-frame and identity-aware I2V profiles;
- optional FramePack/self-hosted low-VRAM route;
- higher-quality free/local Mandarin voice adapters;
- higher-quality free/local music and Foley generation;
- route latency/quality telemetry and automatic hero-shot allocation.

## Success criteria

Milestone 1 is complete when:

1. `hottop video-run` can plan a `zero-cost-hybrid` generation route without serializing secrets or paid options;
2. unit tests prove free-only candidate filtering, bounded failover, and no paid fallback;
3. the HF adapter can submit/poll/download a mocked Gradio job and produce a fresh MP4;
4. `video-run --execute` can invoke the zero-cost per-shot worker through structured commands;
5. a corrupt/static/repeated-frame output can be rejected by the quality gate;
6. normal Python 3.11/3.12 CI remains green;
7. a separate real ZeroGPU smoke workflow exists and records evidence when a public free endpoint is available;
8. PROJECT/STATUS/Skill/PR documentation identifies Zero-Cost Hybrid as the preferred no-paid video route.