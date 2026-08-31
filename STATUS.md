# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@b7899e066ec743008d185ee532ef7dab32da7288`** (`fix: fail closed on malformed ffprobe metadata shapes`, PR #379), SHA-locked squash-merged from exact verified head `63c5b0a91efbb895535232f0f4d56e6acbb38cde`.

TDD/production evidence:

- RED `905fa77748f315c6de44936167d250741f48aba5`: CI #2606 reached Ruff successfully and Python 3.11 pytest failed on the new malformed-metadata-shape regression; Python 3.12 was cancelled after the branch advanced, so no stronger RED claim is recorded.
- GREEN `63c5b0a91efbb895535232f0f4d56e6acbb38cde`: exact-head CI #2607 passed.
- production-smoke #300 passed checked-in anti-polish cow + cinematic Odyssey execution and final-media/provenance verification; artifact `hottop-software3d-production-smoke` was 687,894 bytes with digest `sha256:363ed3091f79cdb2599a702df8faa3381fe7f3e706b32acab5858a969767614c`.
- cinematic-delivery-smoke #167 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification; artifact `hottop-cinematic-software3d-delivery` was 624,448 bytes with digest `sha256:95e5c9a29b91c9155688ff61906b32aacfbf110457abe96d49ceea19e5842b50`.

The generated-video gate now validates the ffprobe metadata container contract before consuming values: top-level metadata and `format` must be objects, `streams` must be a list, and every stream entry must be an object. Malformed shapes fail with `ffprobe metadata structure invalid` rather than raising or being reinterpreted. Existing fail-closed requirements remain: conservative compositor-usability floors of **0.5 s duration, 256 px width, 256 px height and 8 fps**; finite duration/fps; integer-convertible positive dimensions; exactly one complete raw terminal frame of **`width × height` bytes**; motion samples aligned to **`sample_width × sample_height`** and covering at least `max(2, int(duration * sample_fps) - 1)` complete samples.

Durable evidence records now include:

- `docs/research/2026-09-01-generated-media-output-floor.md`
- `docs/research/2026-09-01-terminal-frame-proof.md`
- `docs/research/2026-09-01-terminal-frame-byte-length-proof.md`
- `docs/research/2026-09-01-motion-sample-payload-integrity.md`
- `docs/research/2026-09-01-motion-sample-coverage-proof.md`
- `docs/research/2026-09-01-nonfinite-video-metadata.md`
- `docs/research/2026-09-01-invalid-video-dimension-metadata.md`
- `docs/research/2026-09-01-ffprobe-metadata-shape-integrity.md`

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; offline and runtime-bounded execution; exact request/source/config provenance; rights-safe I2V reference SHA-256 + byte-count + rights binding; rejection of reference mutation; dirty/ambiguous source and escaping tracked-symlink rejection.

`PROJECT.md` remains intentionally unchanged: metadata-shape validation is a stricter implementation of the existing generated-media/final-media integrity doctrine, not a new durable direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, independently verifiable source/config provenance, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, correct duration/frame count, decodability, generic motion or clearing the media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public tip remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; latest material work remains SeedVR distributed-operation focused and does not provide Hottop-measured Wan2.2 I2V identity/requested-action benefit. Continue **no freshness-only repin**.
- Upstream LightX2V warning reports still reinforce that successful execution, correct duration/frame count, or decodable MP4s can coexist with degraded, static, or meaningless content. Treat those reports as external warnings rather than Hottop benchmarks; keep semantic, identity, requested-action and media-integrity gates separate.
- Specialized acceleration/model forks remain gated where effective execution composes external weights/LoRAs/compiled assets without a fully reviewed code+weights+artifact provenance/license chain and Hottop same-case evidence.
- Official **Qwen3-TTS** code remains Apache-2.0, but model/weight licensing and exact revisions remain separate provenance dimensions. Operator-owned local/offline serving stays benchmark-only until the full asset chain is reviewed and same-line Mandarin evidence wins.
- **SGLang-Omni** is a fresher Apache-2.0 serving-code candidate with Qwen3-TTS/CosyVoice-family support, but its code license does not settle served-model weight licenses, hardware practicality or Hottop quality/latency. No auto-install/download or admission is justified without same-case evidence.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition; valid metadata structure, finite metadata, valid integer dimensions, complete terminal/sample-frame framing and temporal coverage are necessary but not sufficient.
4. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates; SGLang-Omni may be benchmarked only as a reviewed operator-owned serving route, never auto-provisioned.
5. Continue targeted ecosystem radar around measured gaps; do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
