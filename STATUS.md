# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Live recovery at the start of this production cycle found `main@88cea030f2d3ea012f4e946c3a07a1b7ef29948f` with no open PR. The previous merged production point remains **`bbe129b695eb253c505790a1cef886be51e4ae6b`** (`fix: preserve explicit continuity benchmark scope`): its exact pre-merge head `6030060e1c395b670b94f223d756e24dc4c70c9e` passed CI #2511, production-smoke #253 and cinematic-delivery-smoke #120, and post-merge `main@bbe129b6…` passed CI #2513, production-smoke #255 and cinematic-delivery-smoke #122. The latter completed the real 720p24 Odyssey delivery, media runtime provenance capture, final media/provenance verification and evidence upload successfully.

Current active workstream is PR #350, `fix/lightx2v-tracked-symlink-provenance`, closing a clean-HEAD provenance escape in the LightX2V operator route. TDD RED is `ddedc38d136f48a863f35269c5ee4e57ee9d70ec`: CI #2518 passed Ruff and failed pytest on a tracked Python symlink resolving outside the checkout. Initial GREEN implementation is `27b7cd816ffe20455911c5dc6a0bbe3982c309d8`: CI #2519 succeeded on Python 3.11/3.12 before durable-memory synchronization. The final PR head must be checked live after this status synchronization; do not infer its CI/smoke result from the initial GREEN head.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence binds exact reference bytes, generated-shot bytes, plan semantics, generator/source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Benchmark scope is explicit.** Incidental or single-shot reference-bearing subjects do not automatically become continuity targets. For every subject that is explicitly evaluated, however, evidence must cover **all** byte-bound subject-bearing plan shots for that subject; partial/cherry-picked coverage fails closed.

Multi-subject integrity also remains fail closed:

- each evidence subject ID must be unique;
- distinct evaluated subjects require distinct reference artifact bytes;
- distinct subjects cannot reuse the same subject-bearing generated artifact bytes;
- evidence shot hashes must belong to the matching plan subject;
- candidate/source and generation-config provenance must match evaluated generated artifacts.

**Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Runtime success or generic motion never proves requested action or subject identity.

LightX2V source provenance remains fail closed across the generation window: inherited `PYTHONPATH` is isolated to the operator checkout root; dirty tracked code and untracked/ignored importable runtime code are rejected; **tracked symlinks resolving outside the checkout are rejected before generation** because their target bytes are not bound by Git HEAD; exact local source revision is captured before spawn and re-verified after generation; a post-generation provenance failure deletes the output instead of accepting a manifest. Internal tracked symlinks resolving inside the checkout remain admissible. Durable rationale: `docs/research/2026-08-31-lightx2v-source-provenance.md`.

Continuity benchmark rationale: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain qwentts.cpp, CrispASR, audio.cpp and Pure-C for 1.7B CustomVoice, plus the lower-hardware 0.6B ncnn benchmark candidate. All remain operator-provisioned and no-auto-download.

Comparable `inspect-tts-benchmark` latency/RTF evidence requires exact text/language/supported speaker, canonical generation protocol, recognized hardware backend with coherent CPU/device count, recognized `cli`/`server` execution shape, server worker/thread topology when applicable, cold/warm independent trials, one runtime revision + one model revision per candidate, finite positive latency, distinct resolved WAV trial paths, WAV/PCM integrity and `listening_required=true`. Hardware/execution profiles remain declared measurement provenance rather than proof of actual runtime utilization.

Durable method: `docs/research/2026-08-30-tts-bench-method-admission.md` plus the 2026-08-31 CPU/accelerator provenance records.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` is `d6cf4f13d152e636ae6daac604d46531077e8670` (2026-08-31 08:35 UTC). The tip removes the redundant ERNIE Image Turbo runner alias; same-day nearby changes affect Flux2/Hunyuan paths. The current recursive tree contains no tracked Git symlinks and the fresh changes do not change the tested Wan2.2 I2V route or provide Hottop-measured identity/motion/runtime gain. Keep the tested pin and continue **no freshness-only repin**.
- **Qwen3-TTS official** remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`. A fresh MLX-Audio report isolates progressive long-text pace acceleration to the Base ICL/reference-cloning path while CustomVoice preset speech stayed stable in that report. Treat it as runtime/path-specific evidence, not a defect claim against Hottop's CustomVoice route; the existing same-line A/B, speaker/onset, bounded-generation and final PCM gates remain appropriate.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Finish PR #350 only after exact final-head CI + production-smoke + cinematic-delivery-smoke are green; then SHA-lock squash merge and promptly remove stale open-workstream wording from this status snapshot.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. Continue LightX2V/reference-continuity review only around concrete, reproducible execution/provenance gaps; preserve explicit evaluated-subject benchmark scope.
4. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots for an evaluated subject and require complete byte-bound **identity + requested-action motion** evidence before composition.
5. When an operator provisions a local Qwen3-TTS 1.7B runtime/model, run the read-only artifact preflight first, then same-line Mandarin generation under existing generation/hardware/execution-shape coherence gates.
6. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
