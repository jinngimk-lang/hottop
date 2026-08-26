# Zero-Cost Video Integration Radar

Updated: 2026-08-27

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
| `ModelTC/LightX2V` | Maintained operator-owned inference framework for Hottop's tested Wan2.2/local path | Repository is Apache-2.0; model/checkpoint rights are separate. Keep the tested pin unless a newer revision produces measured Hottop value. | **Adopted tested local framework; no freshness-only repin** |
| `ernie-research/Memento` | Wan2.2-based long/multi-shot subject-memory candidate that directly targets cross-shot identity drift | Exact GitHub revision `eafe8aa6811d7f27477801c23c54faa33fa4659c` has inference/training code and a README Apache-2.0 badge, but the exact root tree does not contain the linked `LICENSE` file. Hugging Face Memento LoRA/KeyframeQuery weights declare Apache-2.0; base Wan2.2 rights remain separate. Upstream recommends 8×A100 80GB for inference, so dual-DGX-Spark feasibility is unproven. | **Gated continuity benchmark candidate; no download/routing yet** |
| `DeepBeepMeep/Wan2GP` | Low-VRAM operator-side orchestration across Wan2.2/LTX-2/Qwen/Hunyuan plus queueing, headless execution, RIFE/FlashVSR and audio tooling | WanGP Community License 2.0 permits free internal/company use and output creation, but restricts selling/embedding/exposing WanGP itself as a paid product/service. Third-party model licenses remain separate. Hottop must interoperate externally, not copy/bundle WanGP. | **Adopt external operator adapter candidate** |
| `lllyasviel/FramePack` | Low-VRAM progressive I2V / continuity candidate | Repository license verified Apache-2.0. Official README states RTX 30/40/50 support and at least 6GB VRAM; its standalone flow may automatically download large models. Hottop must not trigger that download automatically. | **Future isolated local adapter** |
| `hao-ai-lab/FastVideo` | Future inference acceleration / training-sidecar option for operator GPU | Repository license verified Apache-2.0; useful only when a concrete self-hosted performance gap is measured | **Observe / benchmark before integration** |
| `HKUDS/ViMax` | Director/screenwriter/producer decomposition and reflection ideas | Repository license verified MIT | **Architecture / planning ideas** |
| `HBAI-Ltd/Toonflow-app` | Persistent character/storyboard/provider-abstraction ideas | Treat application and integrated providers/models separately; do not import the Electron app wholesale | **Architecture ideas only** |
| `calesthio/OpenMontage` | Production decomposition, free/open-footage strategy, approval/quality-gate ideas | AGPL-3.0 code: **architecture only**, no code copying into Hottop | **Architecture only** |
| RIFE | Optional interpolation / motion-smoothing post-process | Verify exact upstream revision/license before adapter work | **Future post-process candidate** |
| Real-ESRGAN | Optional restoration/upscale post-process | Verify exact upstream revision/license before adapter work | **Future post-process candidate** |
| InfiniteTalk / talking-video projects | Character dialogue / lip-sync candidate where rights-cleared reference assets exist | Code, weights, voice/likeness rights and runtime cost must all be reviewed independently | **Observe; not default** |

## 2026-08-27 targeted identity-continuity check

The current generated-video gap remains **real multi-shot subject continuity evidence**, so this scan focused on projects that change that mechanism rather than adding generic model coverage.

- `ernie-research/Memento@eafe8aa6811d7f27477801c23c54faa33fa4659c` is directly relevant: it extends Wan2.2-A14B with subject reconstruction plus local/global keyframe queries and is designed to preserve recurring subjects across shots/scenes. The released model card declares Apache-2.0 for the Memento adapter weights and separately identifies Wan2.2 T2V/I2V base models. This is a better mechanism match to Hottop's identity gap than another ordinary I2V wrapper.
- It **does not clear Hottop's admission gate yet**. The exact GitHub tree does not contain the README-linked root `LICENSE` file even though the README badge says Apache-2.0, and official inference guidance recommends `8× A100 80GB`. Hottop has no evidence that the current dual-DGX-Spark topology can execute it safely or efficiently.
- Therefore Memento is tracked as a gated benchmark candidate only. Do not clone/install it from normal `video-run`, do not download its two ~3.2GB adapter weight files or Wan2.2 base checkpoints automatically, and do not claim it improves Hottop until an operator-controlled hardware/license review plus same-story continuity benchmark exists.
- LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069`; its current opt-in MiniMax-H3 weight-residency change does not provide measured Hottop continuity gains, so the tested Wan2.2 route is not repinned merely for freshness.
- Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no upstream change removes the operator-local 1.7B A/B requirement.

No candidate in this refresh is admitted for unattended execution, heavy provisioning or paid fallback.

## 2026-08-26 targeted freshness check

The measured generated-video gap remains real reference-conditioned multi-shot identity evidence, not lack of another provider abstraction.

- LightX2V's recent visible maintenance includes InfiniteTalk cancellation handling and new-model requests. None supplies Hottop evidence that a newer revision materially improves the already-tested Wan2.2 path, so the tested pin remains preferable to freshness-only churn.
- MiniMax H3 support/low-step requests remain interesting for operator benchmarking, but requests are not admission evidence. Model/checkpoint/output-rights, local hardware, exact revision, quality and provenance gates remain unresolved.
- Wan2.2 community inference work continues to expose expert/LoRA routing correctness hazards. This reinforces Hottop's rule that a nominally successful MP4 is not enough: exact runtime/model configuration plus generated-artifact provenance and quality evidence remain mandatory.

No candidate in this refresh clears the gate strongly enough to replace the guaranteed software3d baseline or the existing tested LightX2V/Wan2.2 operator route. The next useful integration event is therefore a **real operator-provisioned reference-conditioned benchmark**, not another speculative adapter.

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

1. **Reference-conditioned operator benchmark:** when a rights-safe reference pack plus operator-provisioned LightX2V/Wan2.2 or compliant WanGP runtime exists, execute at least two subject-bearing shots and bind exact reference bytes, generator source revision, model/checkpoint provenance when independently verifiable, generated bytes and continuity-evaluator evidence.
2. **Memento continuity benchmark:** only after exact code-license packaging is unambiguous and operator hardware feasibility is demonstrated. Compare the same Odyssey subject-bearing shot sequence against the existing LightX2V/Wan2.2 route using Hottop's continuity evaluator; keep it registry/radar-only until then.
3. **MiniMax H3 through LightX2V:** benchmark only after the operator supplies a reviewed local checkpoint/runtime and its model/output-rights are recorded. Do not infer readiness from upstream support requests.
4. **LTX-2 synchronized audio/video evaluation:** evaluate as a local operator backend only after the current license is accepted for the intended use; compare whether synchronized native audio materially beats Hottop's existing free local voice/music/SFX chain.
5. **FramePack isolation benchmark:** only if an operator GPU is available, compare identity drift, motion quality, latency and installation footprint against the existing Wan/LightX2V paths. Do not auto-download its models.
6. **Post-processing adapters:** RIFE/Real-ESRGAN enter only after a measurable failing quality case demonstrates value; do not add heavyweight dependencies speculatively.

## Rejection rules

Do not adopt a project merely because it has many stars, an impressive demo, or advertises “free.” Reject or defer when any of these are unresolved: unclear model/weights rights, mandatory paid API, hidden credit consumption, automatic model downloads outside operator control, insecure one-click installers, unbounded retries, opaque private interfaces, no deterministic test path, or no measurable improvement over existing Hottop routes.
