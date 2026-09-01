# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@82e0c73abe78be1d75ac7689654ae58a3202aa51`** (`Bind LightX2V generation to exact local model bytes`, PR #381), SHA-locked squash-merged from exact verified head `106cda9f05433252938a9f17a0c861c93c2ae8e3`.

TDD/production evidence:

- RED `2d80289278b8ba73ef7203de517458a24f18f309`: CI #2611 reached Ruff successfully and Python 3.12 produced exactly `2 failed, 646 passed` on the new model-provenance regressions: the artifact manifest had no `generation_model_sha256`, and changing a local weight file during generation did not raise. Python 3.11 was cancelled by fail-fast and is not claimed as RED evidence.
- GREEN `106cda9f05433252938a9f17a0c861c93c2ae8e3`: exact-head CI #2613 passed Python 3.11 and 3.12.
- production-smoke #303 passed checked-in anti-polish cow + cinematic Odyssey execution, final-media/provenance verification and evidence upload; artifact `hottop-software3d-production-smoke` was 688,374 bytes with digest `sha256:53d0dca4aaf6a3c4b92cb5cf499ef2e816127eef846f8cdd94dd3267c77c5538`.
- cinematic-delivery-smoke #170 passed actual 720p24 Odyssey delivery, runtime provenance, final-media verification and evidence upload; artifact `hottop-cinematic-software3d-delivery` was 623,331 bytes with digest `sha256:8d99e56be002e4ebf6606195fd5db488c2ea495bc697fbad95f1f330ab9e5ec5`.

The LightX2V operator route now binds the complete configured local model tree by deterministic SHA-256 + total file bytes before generation, records `generation_model_sha256` / `generation_model_size_bytes` in the per-shot artifact manifest, and recomputes the tree after generation. A changed or unreadable model tree invalidates the shot and deletes the generated output before quality acceptance. This is local/read-only evidence: no model download, installation, GPU provisioning, hosted endpoint or paid fallback is introduced.

The generated-video media gate still validates ffprobe metadata shape, finite duration/fps, integer-convertible positive dimensions, conservative compositor-usability floors of **0.5 s duration, 256 px width, 256 px height and 8 fps**, exactly one complete raw terminal frame of **`width × height` bytes**, and aligned motion samples with sufficient temporal coverage. Those checks are necessary media integrity, not identity/action/semantic proof.

Durable evidence records now include:

- `docs/research/2026-09-01-generated-media-output-floor.md`
- `docs/research/2026-09-01-terminal-frame-proof.md`
- `docs/research/2026-09-01-terminal-frame-byte-length-proof.md`
- `docs/research/2026-09-01-motion-sample-payload-integrity.md`
- `docs/research/2026-09-01-motion-sample-coverage-proof.md`
- `docs/research/2026-09-01-nonfinite-video-metadata.md`
- `docs/research/2026-09-01-invalid-video-dimension-metadata.md`
- `docs/research/2026-09-01-ffprobe-metadata-shape-integrity.md`
- `docs/research/2026-09-01-lightx2v-model-byte-provenance.md`

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; offline and runtime-bounded execution; exact request/source/config provenance; rights-safe I2V reference SHA-256 + byte-count + rights binding; rejection of source/config/reference mutation; dirty/ambiguous source and escaping tracked-symlink rejection.

`PROJECT.md` remains intentionally unchanged: exact model-byte binding is a stricter implementation of the existing artifact/provenance and fail-closed operator-owned doctrine, not a new durable direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact local model bytes, reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, independently verifiable source/config provenance, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, correct duration/frame count, decodability, stable model bytes, generic motion or clearing the media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public tip remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; latest material work remains SeedVR distributed-operation focused and does not provide Hottop-measured Wan2.2 I2V identity/requested-action benefit. Continue **no freshness-only repin**.
- The official **Wan2.2-I2V-A14B** model repository continues to present an Apache-2.0 license. Hottop still treats exact local revision/bytes as separate run evidence rather than inferring provenance from a directory name.
- Upstream LightX2V warning reports continue to show that technically successful runs can produce degraded, static or meaningless content. Treat those reports as external warnings rather than Hottop benchmarks; keep media, semantic, identity and requested-action gates separate.
- Specialized acceleration/model forks remain gated where effective execution composes external weights/LoRAs/compiled assets without a fully reviewed code+weights+artifact provenance/license chain and Hottop same-case evidence.
- Recent **Qwen3-TTS** serving work reports measurable Mandarin CER improvements, but operator-owned local/offline serving stays benchmark-only until exact runtime/model/weight provenance is reviewed and same-line Hottop Mandarin evidence wins. SGLang-Omni remains a candidate serving route, not an unattended dependency.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact model/request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition; valid metadata and stable bytes are necessary but not sufficient.
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
