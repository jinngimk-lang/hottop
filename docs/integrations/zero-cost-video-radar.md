# Zero-Cost Video Integration Radar

Updated: 2026-08-25

This radar tracks candidate technologies for Hottop's **strictly zero-paid-cost** video path. A candidate listed here is not automatically production-approved. Every adapter must stay isolated, reversible, quality-gated, and compatible with Hottop's provider-neutral `hottop.render.v2 → hottop.video-plan.v1 → video-run` contract.

## Admission rules

1. **Code license and model/weights license are reviewed separately.** A permissive repository license does not prove that every checkpoint, hosted endpoint, dataset, voice, music model, or generated asset is commercially safe.
2. **No paid fallback.** `ZERO_COST_MODE=true` means public/free quota, operator-owned compute, or deterministic CPU degradation only. Billing enrollment, paid credits, automatic overage, and credit-card requirements are not valid fallback routes.
3. **No autonomous heavyweight provisioning.** Hottop does not silently download model weights, install unreviewed custom nodes, provision GPUs, create accounts, or run third-party one-click installers.
4. **Evidence before adoption.** Pin an upstream version/commit, verify source/license, isolate the adapter, add tests, run a real MP4 smoke when execution changes, and require a measurable gain in quality, consistency, speed, or reliability.
5. **Failure must be safe.** Free capacity exhaustion or a rejected artifact must retry within configured bounds or degrade to deterministic production; it must never switch to a paid service.
6. **Interoperate before embedding.** If an upstream application has a restrictive license, Hottop may still interoperate with an operator-provided local executable/service when that license permits the use, but Hottop must not copy, bundle, white-label, or expose the upstream application as a paid backend.

## Current routes and candidates

| Project / route | Role in Hottop | License / rights note | Current decision |
|---|---|---|---|
| `jinngimk-lang/ai-video-director` | Behavior donor for HF ZeroGPU submit/poll/download, bounded free routing, media/motion gates and zero-cost smoke methodology | User-owned project; port behavior into Hottop's Python contracts rather than importing the old app architecture | **Adopted behavior** |
| Hugging Face ZeroGPU | Shared free GPU transport for short high-value shots when a public Space is healthy | Space/model rights are separate from HF platform access; free quota/availability is nondeterministic | **Adopted optional free route** |
| Lightricks LTX family / LTX-2.x | T2V/I2V and newer synchronized audio-video candidate behind a free Space or operator-owned GPU | LTX-2.x uses a Community License; current license requires a paid commercial agreement for entities at/above the stated revenue threshold, while non-commercial testing is separately defined. Never assume the model is commercially free merely because code is public. | **License-gated candidate** |
| `Wan-Video/Wan2.2` | Preferred operator-controlled self-hosted generation family when adequate GPU exists | Repository is Apache-2.0; model/runtime assets remain operator-controlled and must be checked independently | **Adopted optional local route** |
| `DeepBeepMeep/Wan2GP` | Low-VRAM operator-side orchestration across Wan2.2/LTX-2/Qwen/Hunyuan plus queueing, headless execution, RIFE/FlashVSR and audio tooling | WanGP Community License 2.0 permits free internal/company use and output creation, but restricts selling/embedding/exposing WanGP itself as a paid product/service. Third-party model licenses remain separate. Hottop must interoperate externally, not copy/bundle WanGP. | **Adopt external operator adapter candidate** |
| `lllyasviel/FramePack` | Low-VRAM progressive I2V / continuity candidate | Repository license verified Apache-2.0. Official README states RTX 30/40/50 support and at least 6GB VRAM; its standalone flow may automatically download large models. Hottop must not trigger that download automatically. | **Future isolated local adapter** |
| `hao-ai-lab/FastVideo` | Future inference acceleration / training-sidecar option for operator GPU | Repository license verified Apache-2.0; useful only when a concrete self-hosted performance gap is measured | **Observe / benchmark before integration** |
| `HKUDS/ViMax` | Director/screenwriter/producer decomposition and reflection ideas | Repository license verified MIT | **Architecture / planning ideas** |
| `HBAI-Ltd/Toonflow-app` | Persistent character/storyboard/provider-abstraction ideas | Treat application and integrated providers/models separately; do not import the Electron app wholesale | **Architecture ideas only** |
| `calesthio/OpenMontage` | Production decomposition, free/open-footage strategy, approval/quality-gate ideas | AGPL-3.0 code: **architecture only**, no code copying into Hottop | **Architecture only** |
| RIFE | Optional interpolation / motion-smoothing post-process | Verify exact upstream revision/license before adapter work | **Future post-process candidate** |
| Real-ESRGAN | Optional restoration/upscale post-process | Verify exact upstream revision/license before adapter work | **Future post-process candidate** |
| InfiniteTalk / talking-video projects | Character dialogue / lip-sync candidate where rights-cleared reference assets exist | Code, weights, voice/likeness rights and runtime cost must all be reviewed independently | **Observe; not default** |

## What is already implemented in Hottop

- `generation_backend: zero-cost-router` with candidates whose `cost_per_unit` must be `0`.
- `allow_paid_fallback: false` is a validation invariant, not a recommendation.
- HF ZeroGPU Gradio queue adapter with optional environment-only token lookup.
- Bounded candidate failover with structured retryable failures.
- Deterministic FFmpeg/ffprobe video-quality inspection.
- Quality rejection deletes the bad artifact and retries the next configured free candidate rather than accepting a fake-motion/duplicate-heavy MP4.
- MoviePy + local dialogue/music/SFX + FFmpeg remain available independently of free remote GPU capacity.
- Artifact provenance is bound to exact generated bytes and rechecked immediately before composition.

## Near-term experiments

1. **External WanGP interoperability adapter:** add a structured, shell-safe operator command contract for an already-installed WanGP instance. Hottop will pass a shot plan and expected output path without copying WanGP code or silently downloading models. The adapter must remain opt-in, local-only, and outside the default unattended zero-cost cloud route.
2. **Reference-first I2V consistency:** add a rights-safe reference-image contract so character/product keyframes can feed an eligible free/local I2V backend without changing creative semantics.
3. **LTX-2 synchronized audio/video evaluation:** evaluate as a local operator backend only after the current license is accepted for the intended use; compare whether synchronized native audio materially beats Hottop's existing free local voice/music/SFX chain.
4. **Deterministic generation degradation:** when all free generative candidates are unavailable, evaluate a clearly labeled image/recording-motion fallback instead of publishing a mock as generated footage.
5. **FramePack isolation benchmark:** only if an operator GPU is available, compare identity drift, motion quality, latency and installation footprint against the existing Wan/ZeroGPU paths. Do not auto-download its models.
6. **Post-processing adapters:** RIFE/Real-ESRGAN enter only after a measurable failing quality case demonstrates value; do not add heavyweight dependencies speculatively.

## Rejection rules

Do not adopt a project merely because it has many stars, an impressive demo, or advertises “free.” Reject or defer when any of these are unresolved: unclear model/weights rights, mandatory paid API, hidden credit consumption, automatic model downloads outside operator control, insecure one-click installers, unbounded retries, opaque private interfaces, no deterministic test path, or no measurable improvement over existing Hottop routes.
