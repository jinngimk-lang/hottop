# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@7ea0c2a52d336e262e6df11165c3440789b8e244`** (`fix: require terminal frame proof in generated-video gate`, PR #367), SHA-locked squash-merged from exact verified head `6b587eb1f9f95b1125e9f249994fb52d19b857be`.

TDD/production evidence for the terminal-frame integrity workstream:

- RED `bac333db261312daca8decd568f17bf3327c0c43`: Python 3.11 CI reached the intended regression failure with Ruff green and `1 failed, 636 passed`; a zero-exit terminal probe with no decoded frame bytes was incorrectly accepted by the prior implementation;
- GREEN `6b587eb1f9f95b1125e9f249994fb52d19b857be`: exact-head CI #2577 passed Python 3.11 + 3.12 Ruff/full pytest;
- the same GREEN head passed production-smoke #288, including checked-in anti-polish cow + cinematic Odyssey execution and final-media/provenance verification; artifact `hottop-software3d-production-smoke` was 688,374 bytes with archive digest `sha256:06dd3368eb0ee8ef1f8b5b3bcae8a3eb0d409913be287b24240114e912f16b1f`;
- the same GREEN head passed cinematic-delivery-smoke #155, including actual 720p24 Odyssey delivery, runtime provenance and final media/provenance verification; artifact `hottop-cinematic-software3d-delivery` was 624,450 bytes with archive digest `sha256:4ca096d287d373598608bd2d71de693ab7b018f446bb6ba4a2dc60e4143dd7af`.

The shared generated-video `VideoQualityPolicy` continues to fail closed below conservative compositor-usability minima of **0.5 s duration, 256 px width, 256 px height and 8 fps**. In addition, terminal integrity now requires FFmpeg to both exit successfully **and emit an actual decoded terminal-frame payload**; a successful process with no decoded frame bytes fails closed. These are acceptance floors, not forced target delivery geometry.

Durable evidence records:

- `docs/research/2026-09-01-generated-media-output-floor.md`
- `docs/research/2026-09-01-terminal-frame-proof.md`

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; network-offline and runtime-bounded generation; exact request/source/config provenance; rights-safe I2V reference SHA-256 + bytes + rights binding; rejection of reference mutation; dirty/ambiguous source and escaping tracked-symlink rejection.

`PROJECT.md` is intentionally unchanged in this workstream because terminal-frame byte proof directly implements the existing generated-media/final-media integrity doctrine rather than changing durable project direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, actual source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity are separate dimensions.** Runtime success, request digests, decodability, generic motion or merely clearing the media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public tip remained `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`. Its newest material work repairs SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it does not provide Hottop-measured Wan2.2 I2V identity/requested-action benefit. Continue **no freshness-only repin**.
- A public LightX2V Wan2.2-TI2V-5B I2V failure report shows meaningless color/light-block output despite a runnable generation path. This reinforces, rather than changes, the current admission doctrine: runtime success, decodability and generic motion are not semantic/identity/requested-action proof.
- Specialized Wan2.2 acceleration forks remain gated where their effective route composes external model/LoRA/compiled assets without one fully reviewed code+weights+artifact provenance and license chain or Hottop same-case quality evidence.
- **Qwen3-TTS** lower-hardware community ports remain benchmark candidates. Any route that auto-downloads model-family weights conflicts with unattended no-auto-download unless the operator already provisioned and pinned those assets locally.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact request/source/config/reference provenance** across all subject-bearing shots before composition; terminal-frame proof and the shared media floor are necessary but not sufficient.
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
