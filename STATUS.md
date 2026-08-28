# Hottop Status

Last updated: 2026-08-28
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current verified repository truth

Live recovery on 2026-08-28 observed `main@451ab42817229a5d0dbde58e9daaeaaa8130b849`; CI **#1965** passed. PR #157 had already passed exact-head CI **#1964**, production-smoke **#202**, and 720p cinematic-delivery-smoke **#69** before squash merge. This head closes the code-contract gap between the existing identity-vs-motion doctrine and the provider-neutral continuity benchmark.

Treat recorded SHAs as verified historical evidence points only; future recovery must re-fetch live `main` and exact-head CI.

## Canonical Production v0.2 baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical for unattended work. This route requires no GPU/model, paid fallback, credentials or implicit multi-GB downloads. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest accepted cow/Odyssey deterministic evidence remains healthy. Do not retune deterministic visuals/audio without a measured regression.

## Creative hotspot / meme-native discovery boundary

Fresh creative work now explicitly separates two evidence layers when public evidence allows:

1. **source event** — what actually happened, when, and which claims are verified, alleged, satirical or fictional;
2. **active derivative meme** — what people are currently repeating, remixing, quoting, screenshotting or joking about.

The creative hook may come from the derivative meme while factual context remains bound to the source event. Social titles should use **meme-native hook compression** rather than newsroom summaries: prefer the shortest native phrase, number, action, reversal or concrete consequence that carries the current joke. Internal workflow labels such as `热点梗图` or `今日热搜 TOP1` stay out of audience-facing creative unless they are genuinely part of the joke.

The 2026-08-28 accepted lesson is the reusable compression pattern `short utterance + concrete consequence`, not the specific people, event, or layout from the historical example. If a source story is fictional/satirical or a circulating derivative claim is unverified, that boundary remains explicit even when the derivative meme is genuinely active.

## Dialogue / neural-TTS integrity boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; CosyVoice3 remains correctness-gated rather than default.

Input and output integrity remain separate fail-closed layers:

- every `AudioCue.text` is trimmed and must be nonblank;
- `kind=dialogue` must contain at least one Unicode letter or number;
- punctuation/symbol-only text may remain valid for SFX/Foley but cannot consume speech runtime as dialogue;
- neural model waveforms must be non-empty and finite;
- the exact int16 PCM destined for WAV must be non-silent before WAV/temp creation;
- bounded Qwen dialogue uses a planned-duration-derived `max_new_tokens` ceiling as resource protection;
- produced PCM duration remains the authoritative slot-fit gate;
- final audio/media verification remains authoritative for delivered artifacts.

Fresh upstream evidence adds one **benchmark-quality risk**, not a new production defect claim. `QwenLM/Qwen3-TTS` issue #343 reports a fine-tuned 1.7B Base voice whose short utterances / first roughly 1–2 seconds can show timbre or apparent gender instability while longer generations are stable. Because that report is a fine-tuned Base model, Hottop does not generalize it to preset CustomVoice. Instead, the future operator-local 1.7B Mandarin A/B must separately evaluate short-line onset stability as well as normal production-length dialogue. See `docs/research/2026-08-28-qwen3-tts-short-onset-benchmark.md`.

Fresh upstream issue #4576 remains a separate runtime example: very short Chinese inputs such as `1次`/`2次` can trigger runaway garbled output in a serving stack. Lexical input validation therefore does not replace token, produced-duration or PCM integrity gates.

**Operator benchmark rule:** future Qwen3-TTS 1.7B evidence binds model/checkpoint, runtime/patch/container identity, hardware, serving topology, execution/cache policy, traffic/concurrency shape, cold-first-use versus warmed repeated trials, seeds/repetitions where supported, throughput/TTFA/failures, Mandarin intelligibility, speaker consistency, delivery/naturalness, **short-onset stability**, and publication rights. Throughput gains never stand in for speech-quality gains.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download, serving-stack install or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot benchmark. Input locks are constraints, not proof; output-side continuity evidence must cover every subject-bearing shot and bind exact reference bytes, generated bytes, generator source/model provenance when independently verifiable and evaluator revision.

**Identity fidelity and motion fidelity are separate evidence dimensions.** A recognizable subject with wrong/frozen/degenerate motion is not successful subject-and-motion continuity; strong motion does not prove subject identity.

PR #157 now enforces that doctrine in `hottop.reference-continuity-benchmark.v1`. Generic frame/pixel motion remains a media-quality check, not requested-action proof. When a route explicitly claims combined identity + motion success, `ReferenceContinuityPolicy(require_motion_fidelity=True)` requires evaluator-supplied `motion_fidelity` and `reference_pose_diversity` for each evaluated subject and fails closed if either is missing or below policy threshold. Historical identity-only evidence remains backward-compatible. See `docs/research/2026-08-28-motion-fidelity-anti-copy-evidence.md`.

Primary tested/operator route remains **LightX2V/Wan2.2**. Gated continuity and motion-control candidates remain research/benchmark-only unless their exact source/checkpoint rights and operator runtime pass admission. Do not fabricate DGX/GPU readiness; driver/CUDA/PyTorch/model/reference state must be probed on actual operator machines before any generated-quality claim.

UnityVideo remains registered as `benchmark_candidate / integration_ready=false / runtime_status=unprobed / self_owned_compute`, not as an executable backend. Reviewed source `JIA-Lab-research/UnityVideo@e79e9b6bd1c498dd919dceb4cdea47e20417bf70` is MIT; the published `KlingTeam/UnityVideo` model card reports Apache-2.0 for the roughly 10 GB inference checkpoint while Wan2.2 base/reference/output rights remain separate. Its upstream CLI auto-downloads UnityVideo + Wan2.2 assets on first use, and the released checkpoint was evaluated only at 256×256 / 33 frames, so normal `video-run` must never invoke it without explicit local provisioning and same-sequence operator evidence. See `docs/research/2026-08-28-unityvideo-admission.md`.

Wan-Animate-2 is now also present in `integrations/model-hub.yml` only as `benchmark_candidate / integration_ready=false / runtime_status=unprobed / self_owned_compute`. Exact reviewed source `Wan-Video/Wan-Animate-2@3ad2fef7d61d6200c9c653e0fe47be7616b323f3` has Apache-2.0 source code, but checkpoint, reference-image, driving-performance and output rights remain separately bound. Upstream documents 720p around an 8×A800 setup and 480p on 2×A800 and provides checkpoint download helpers; Hottop must never invoke those download paths unattended. There is no executable Hottop adapter. Any future operator benchmark must independently prove identity fidelity and motion/performance fidelity on rights-safe bytes. See `docs/research/2026-08-28-wan-animate-2-admission.md`.

Wan3.0 is the current Alibaba Cloud flagship and is relevant to the same continuity gap because its official hosted route supports multi-modal reference-based video and up to 30-second generation. It is **not** a ZERO_COST or operator-local Hottop route: official Model Studio access requires an API key and metered billing, while `AlibabaCloud-Official/Wan3.0@4ff8ec7c43049d975f724feab26bdcbafb16d888` contains documentation plus Apache-2.0 repository licensing but no local inference code or downloadable model/checkpoint assets. Repository license therefore does not establish model-weight rights. See `docs/research/2026-08-28-wan3-zero-cost-admission.md`.

## Fresh ecosystem radar — 2026-08-28

Targeted checks remain gap-driven rather than popularity-driven.

- **MuSS:** reviewed `zhang-haojie/MuSS@19f5808a776e9b12fcf5e5efa0cacc2f5e4886d8` separates subject consistency, action strength and Anti-Copy-Paste Variance (`ACP-Var`), where `ACP-Var` explicitly penalizes rigid reference-pose copying. Its public repository intentionally omits the benchmark implementation and says code/dataset licensing is still being finalized. Hottop therefore imports no MuSS code/data and does not claim MuSS-calibrated thresholds; only the independently useful identity-vs-action-vs-anti-copy acceptance pattern informed the provider-neutral contract.
- **Wan3.0:** Alibaba Cloud Model Studio documents `wan3.0-video` as the current all-in-one reference-based model with text/image/video/audio/file inputs, native audio and up to 30-second output. The official route requires an API key and is priced per generated second; the reviewed public GitHub repository does not publish local inference code or weights. It therefore remains outside unattended `ZERO_COST_MODE=true` and outside operator-local admission. No paid API fallback was added.
- **Wan-Animate-2:** admitted into the discovery registry only after RED→GREEN model-hub tests. Its reference-image + driving-video shape is directly relevant to identity + motion evidence, but it remains non-executable until local operator provisioning, checkpoint-rights review and output-side benchmark evidence exist. Diffusers support remains upstream work rather than a reason to change Hottop routing.
- **UnityVideo:** reviewed source `e79e9b6bd1c498dd919dceb4cdea47e20417bf70` provides depth, DensePose, RAFT optical-flow, segmentation and skeleton conditioning on Wan2.2-TI2V-5B. It remains relevant to Hottop's independently measured **motion fidelity** dimension, but it is not identity proof and is not admitted for unattended execution.
- **LightX2V/Wan2.2:** LightX2V `main` remains `680d9be199a69ebe4a02f86bdd653f23298ac02d`; the visible latest change is retired-model cleanup rather than a Hottop-measured continuity/runtime improvement. Keep the tested pin; there is still no freshness-only repin.
- **Qwen3-TTS:** official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`. Existing H100/H200 reproduction evidence still supports benchmark-first admission rather than acceleration-toggle-driven routing.
- **Qwen-Audio-3.0-TTS:** Alibaba Cloud's hosted route remains metered/API-key dependent and therefore outside unattended ZERO_COST admission until a reviewed operator-local open route exists.
- **MV-S2V and other continuity candidates:** impressive demos remain gated when source/checkpoint license, multi-GPU runtime or operator assets are unresolved. Popularity alone is not evidence.

No newly reviewed candidate clears the admission gate strongly enough to replace the guaranteed software3d baseline or current tested operator routes.

## Immediate next actions

1. Keep `PROJECT.md`, hotspot/meme skill, creative-memory skill and future creative archives aligned on **source-event + derivative-meme discovery** and **meme-native hook compression**; fresh current evidence remains authoritative.
2. Continue inspecting fresh real cow/Odyssey production evidence and modify deterministic visuals/audio only for a **measured** defect.
3. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
4. For any route claiming both identity and motion, persist **identity fidelity, requested-action/performance fidelity and reference-pose diversity/anti-copy evidence separately**; generic pixel motion cannot stand in for requested-action fidelity, and no dimension may stand in for another.
5. If Wan-Animate-2 is locally provisioned by the operator, benchmark its reference-image + driving-performance route on the same rights-safe subject sequence used by the existing continuity evaluator. Promote nothing unless identity and motion/performance both measurably pass without weakening geography, provenance, cost or final-media gates.
6. If UnityVideo is locally provisioned by the operator, benchmark one or more explicit depth/flow/pose conditions against the same rights-safe subject-bearing sequence used by the existing Wan2.2/LightX2V route. Promote nothing unless motion/action adherence measurably improves without weakening identity, geography, provenance or final-media gates.
7. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run a same-line Mandarin A/B against the guaranteed fallback. Include both short production-like utterances with separate first-1–2-second onset review and normal production-length lines; label cold-first-use separately, use repeated warmed trials, and promote only on measured intelligibility/speaker consistency/delivery/naturalness plus publication-rights evidence.
8. Re-evaluate gated continuity candidates only when exact source/checkpoint rights are compatible and the required operator runtime/assets are already provisioned; benchmark Hottop's own rights-safe sequence rather than copied benchmark media. Hosted Wan3.0 remains excluded until a separately reviewed zero-paid local route with auditable code/model rights exists.
9. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
10. For fresh creative output, perform live/supplied **source-event + derivative-meme** analysis first; consult creative memory only after current context is resolved, compress social hooks into the smallest meme-native high-information wording, and archive real feedback/performance lessons when evidence exists.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including `creative-reference-memory` when prior Hottop cases can help.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh source-event + derivative-meme/mechanism analysis for new creative generation.
8. creative-memory retrieval when useful, after current context is resolved.
9. continue the highest-value safe action autonomously.