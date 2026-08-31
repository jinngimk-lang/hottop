# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@b9a437e4ac4b588939cc0b76cb667b1d6a43c428`** (`fix: require complete terminal-frame payload`, PR #369), SHA-locked squash-merged from exact verified head `6caa9d75013fdbabff30a3d2fe7bc2aac15b656b`.

TDD/production evidence:

- RED `f449a2002e81f91b2869f706153d1116ffcaebc8`: CI #2581 reached pytest after successful install + Ruff and failed on the new one-byte terminal-frame regression, proving the prior non-empty-byte check was too weak;
- GREEN `6caa9d75013fdbabff30a3d2fe7bc2aac15b656b`: exact-head CI #2582 passed Python 3.11 + 3.12 Ruff/full pytest;
- production-smoke #290 passed checked-in anti-polish cow + cinematic Odyssey execution and final-media/provenance verification; artifact `hottop-software3d-production-smoke` was 687,895 bytes with archive digest `sha256:f7d352373c86448080960b0d1d3dc022f095c9e3023a5c71aff9d1855cb38328`;
- cinematic-delivery-smoke #157 passed actual 720p24 Odyssey delivery, runtime provenance, final-media/seam verification and evidence upload; artifact `hottop-cinematic-software3d-delivery` was 624,451 bytes with archive digest `sha256:261d9fc30ffd8ecb6ef3ee44afd8bcfa600e0060dcec85ab287e84fe5aa1f70c`.

The shared generated-video gate remains fail closed below conservative compositor-usability minima of **0.5 s duration, 256 px width, 256 px height and 8 fps**. Terminal integrity now additionally requires FFmpeg success plus exactly one complete raw `gray` terminal frame: **`width × height` bytes**. A zero-exit process with empty, partial or oversized terminal payload does not prove decodability.

Durable evidence records:

- `docs/research/2026-09-01-generated-media-output-floor.md`
- `docs/research/2026-09-01-terminal-frame-proof.md`
- `docs/research/2026-09-01-terminal-frame-byte-length-proof.md`

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; offline and runtime-bounded execution; exact request/source/config provenance; rights-safe I2V reference SHA-256 + byte-count + rights binding; rejection of reference mutation; dirty/ambiguous source and escaping tracked-symlink rejection.

`PROJECT.md` is intentionally unchanged because complete raw-frame proof is a stricter implementation of the existing generated-media/final-media integrity doctrine, not a new durable direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, independently verifiable source/config provenance, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, request digests, decodability, generic motion or merely clearing the media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public tip remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`. Its latest material work restores SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it does not provide Hottop-measured Wan2.2 I2V identity/requested-action benefit. Continue **no freshness-only repin**.
- Open LightX2V issue #603 reports lower Wan2.2 I2V resolution/content/realistic motion than the authors' Diffusers implementation under reportedly comparable parameters. Treat this as external warning evidence, not a benchmark; it reinforces the requirement for Hottop same-case semantic/identity/requested-action quality gates.
- Specialized acceleration/model forks remain gated where effective execution composes external weights/LoRAs/compiled assets without a fully reviewed code+weights+artifact provenance/license chain and Hottop same-case evidence.
- **Qwen3-TTS** lower-hardware community ports remain benchmark candidates. Any route that auto-downloads model-family weights conflicts with unattended no-auto-download unless those assets are operator-provisioned and pinned locally.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition; complete terminal-frame proof and the shared media floor are necessary but not sufficient.
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
