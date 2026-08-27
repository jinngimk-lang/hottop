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
| `WeChatCV/Stand-In` | Lightweight Wan2.2 identity-control benchmark candidate for the current continuity gap | Exact source `e351224366be169076e94af1454115d91d458313` contains Apache-2.0 `LICENSE`; public Stand-In model card declares Apache-2.0 and includes Wan2.2 weights. Base Wan2.2 checkpoint rights/runtime remain separately bound. Official quickstart has automatic model downloads, which Hottop must never invoke unattended. | **Admitted registry-only operator benchmark; runtime unprobed, no default routing** |
| `rain152/IPVG` | Prompt-decomposition + HyperLoRA first-frame identity + Wan2.2 continuity mechanism | Exact source `cd70f169e9a86d47e7860392b8b80c8d59a6d75a` README claims MIT but root tree lacks the linked `LICENSE`; documented path also adds Qwen3-8B, HyperLoRA and Wan2.2 provisioning. | **Gated continuity benchmark candidate; no code ingestion** |
| `WildActor/WildActor` | Wan2.2-5B multi-reference full-body human identity candidate | Exact source `c858c2100ed14b32c36883e0570948f4c09e0d28` exposes Wan2.2 inference code but the inspected root tree has no license file. Human-only/data-pipeline scope also requires separate data/reference-rights review. | **Gated research candidate pending exact license/weights review** |
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

- `ernie-research/Memento@eafe8aa6811d7f27477801c23c54faa33fa4659c` is directly relevant: it extends Wan2.2-A14B with subject reconstruction plus local/global keyframe queries and is designed to preserve recurring subjects across shots/scenes. It remains gated because the exact GitHub tree lacks the README-linked root `LICENSE` file and official inference guidance recommends `8× A100 80GB`.
- `WeChatCV/Stand-In@e351224366be169076e94af1454115d91d458313` clears a narrower registry-level admission gate: the exact tree contains Apache-2.0 `LICENSE`, the public Stand-In model card declares Apache-2.0, Wan2.2-compatible identity weights are published, and the mechanism directly targets identity. Hottop therefore records it as `benchmark_candidate / integration_ready=false / runtime_status=unprobed`. Its upstream automatic download script is explicitly excluded; operator-provisioned local source/weights and output-side continuity evidence remain mandatory.
- `rain152/IPVG@cd70f169e9a86d47e7860392b8b80c8d59a6d75a` is mechanism-relevant and reports strong external challenge placement, but the exact root tree lacks the README-linked MIT `LICENSE`. Its Qwen3-8B + HyperLoRA + Wan2.2 provisioning also increases footprint. Keep it gated; borrow architecture only until exact-source licensing clears.
- `WildActor/WildActor@c858c2100ed14b32c36883e0570948f4c09e0d28` supplies Wan2.2-5B-compatible multi-reference human identity inference code, but the inspected root tree has no license file. It is human-specific and its data construction path introduces separate dataset/reference-rights questions, so it is research-only for now.
- LightX2V `main` advanced on 2026-08-27 to `680d9be199a69ebe4a02f86bdd653f23298ac02d`. The visible sequence after `b220e261…` is prompt-enhancer removal, path/config normalization, and retired-model-remnant cleanup; these are maintenance/cleanup changes rather than Hottop-measured continuity or runtime gains for the tested Wan2.2 I2V subset. Keep the tested pin; there is still **no freshness-only repin**.
- Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no upstream change removes the operator-local 1.7B A/B requirement.

No newly surfaced candidate is admitted for unattended execution, heavy provisioning or paid fallback.

## 2026-08-26 targeted freshness check

The measured generated-video gap remains real reference-conditioned multi-shot identity evidence, not lack of another provider abstraction.

- LightX2V's recent visible maintenance includes InfiniteTalk cancellation handling and new-model requests. None supplies Hottop evidence that a newer revision materially improves the already-tested Wan2.2 path, so the tested pin remains preferable to freshness-only churn.
- MiniMax H3 support/low-step requests remain interesting for operator benchmarking, but requests are not admission evidence. Model/checkpoint/output-rights, local hardware, exact revision, quality and provenance gates remain unresolved.
- Wan2.2 community inference work continues to expose expert/LoRA routing correctness hazards. This reinforces Hottop's rule that a nominally successful MP4 is not enough: exact runtime/model configuration plus generated-artifact provenance and quality evidence remain mandatory.

No candidate in this refresh clears the gate strongly enough to replace the guaranteed software3d baseline or the existing tested LightX2V/Wan2.2 operator route. The next useful execution event is therefore a **real operator-provisioned reference-conditioned benchmark**, not another speculative provider adapter.

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
2. **Stand-In/Wan2.2 identity benchmark:** after the exact local source and already-provisioned Stand-In/Wan2.2 A14B weights pass operator preflight, compare the same recurring Odyssey subject/shots against the existing LightX2V/Wan2.2 route. Promotion requires complete subject-bearing continuity evidence and measured gain; the upstream automatic downloader is never used by Hottop.
3. **Memento continuity benchmark:** only after exact code-license packaging is unambiguous and operator hardware feasibility is demonstrated. Compare the same Odyssey subject-bearing shot sequence against the existing LightX2V/Wan2.2 route using Hottop's continuity evaluator; keep it registry/radar-only until then.
4. **MiniMax H3 through LightX2V:** benchmark only after the operator supplies a reviewed local checkpoint/runtime and its model/output-rights are recorded. Do not infer readiness from upstream support requests.
5. **LTX-2 synchronized audio/video evaluation:** evaluate as a local operator backend only after the current license is accepted for the intended use; compare whether synchronized native audio materially beats Hottop's existing free local voice/music/SFX chain.
6. **FramePack isolation benchmark:** only if an operator GPU is available, compare identity drift, motion quality, latency and installation footprint against the existing Wan/LightX2V paths. Do not auto-download its models.
7. **Post-processing adapters:** RIFE/Real-ESRGAN enter only after a measurable failing quality case demonstrates value; do not add heavyweight dependencies speculatively.

## Rejection rules

Do not adopt a project merely because it has many stars, an impressive demo, or advertises “free.” Reject or defer when any of these are unresolved: unclear model/weights rights, mandatory paid API, hidden credit consumption, automatic model downloads outside operator control, insecure one-click installers, unbounded retries, opaque private interfaces, no deterministic test path, or no measurable improvement over existing Hottop routes.
