# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@3a9e8e1d1103229564b4b7f049c775396a356788`** (`video: reject unusable generated media geometry`, PR #365), SHA-locked squash-merged from exact verified head `13a900a5a6027f7f36abf2db782ee8a6cd5e511a`.

TDD/production evidence for the generated-media output-floor workstream:

- RED `d99f4fdf6da56db9e6a1c823f5dbdeff8aa6c60e`: CI #2571 reached pytest failure on Python 3.11 and 3.12 while install/Ruff were green, proving the prior shared gate could accept an implausibly tiny/short/low-FPS moving clip;
- GREEN `13a900a5a6027f7f36abf2db782ee8a6cd5e511a`: exact-head CI #2572 passed Python 3.11 + 3.12 Ruff/full pytest;
- the same GREEN head passed production-smoke #286, including both checked-in anti-polish cow and cinematic Odyssey execution plus final-media/provenance verification; artifact `hottop-software3d-production-smoke` was 687,894 bytes with archive digest `sha256:758597fb2597e70b1d3446255a197b50e63c0fcda438b3b9f920d445af3dc9b9`;
- the same GREEN head passed cinematic-delivery-smoke #153, including actual 720×1280/24 fps Odyssey delivery, runtime provenance, final-media/provenance and seam-quality verification; artifact `hottop-cinematic-software3d-delivery` was 624,450 bytes with archive digest `sha256:f548b98770b9090dbdc5d7408d424e90448521a8857a6c5a8b2e7582ebdcd7b2`.

The shared generated-video `VideoQualityPolicy` now fails closed below conservative compositor-usability minima of **0.5 s duration, 256 px width, 256 px height, and 8 fps**. These are minimum acceptance floors, not forced target delivery geometry; higher-quality profiles and later MoviePy/FFmpeg scaling remain style/config routed.

Durable evidence record: `docs/research/2026-09-01-generated-media-output-floor.md`.

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; network-offline and runtime-bounded generation; exact request/source/config provenance; rights-safe I2V reference SHA-256 + bytes + rights binding; rejection of reference mutation; dirty/ambiguous source and escaping tracked-symlink rejection.

`PROJECT.md` is intentionally unchanged in this workstream because the new media floor directly implements the existing generated-media quality/integrity doctrine rather than changing durable project direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, actual source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity are separate dimensions.** Runtime success, request digests, generic motion, or merely clearing the new media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate is generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public tip remained `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` in this cycle. Its newest material work repairs SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it does not provide Hottop-measured Wan2.2 I2V identity/requested-action benefit. Continue **no freshness-only repin**.
- A specialized Wan2.2 acceleration fork surfaced with aggressive quantization/4-step claims, but its effective route composes multiple external model/LoRA/compiled assets. Exact code/weights/artifact licensing and provenance have not been admitted as one Hottop-compatible zero-cost runtime, and no same-case Hottop quality win is proven. Radar-only: no vendoring, auto-install or model download.
- **Qwen3-TTS** lower-hardware community ports remain benchmark candidates. Any route that auto-downloads model-family weights conflicts with unattended no-auto-download unless the operator has already provisioned and pinned those assets locally.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route, or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media quality + identity + requested-action motion + exact request/source/config/reference provenance** across all subject-bearing shots before composition; the shared media floor is necessary but not sufficient.
4. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
5. Continue targeted ecosystem radar around measured gaps; do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
