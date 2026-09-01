# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@0415e0ff59042dc923c3f08c7e5a1a43da8d09c3`** (`Fail closed on LightX2V runtime injection environment`, PR #388), SHA-locked squash-merged from exact verified head `5b291939994b611dfd4083786fcf65e2c20652ae`.

Latest TDD/production evidence:

- RED `653521087bb1f57f892539412037965b20ff854c`: CI #2634 reached clean Ruff and failed pytest on the new regression proving that the old LightX2V child environment still inherited interpreter/loader injection controls including `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP`, and `PYTHONINSPECT`.
- GREEN exact head `5b291939994b611dfd4083786fcf65e2c20652ae`: CI #2635 passed Ruff + full pytest on Python 3.11 and 3.12 after stripping those runtime-injection controls while preserving legitimate local runtime configuration such as `LD_LIBRARY_PATH`.
- production-smoke #316 passed checked-in anti-polish cow + cinematic Odyssey execution, final-media/provenance verification and evidence upload; artifact `hottop-software3d-production-smoke` was 687,895 bytes with digest `sha256:7f3c4097e14bf192978c5f936853b818d430b4234fe05dca7a32998a80e5d17c`.
- cinematic-delivery-smoke #183 passed actual 720p24 Odyssey delivery, runtime provenance, final-media verification and evidence upload; artifact `hottop-cinematic-software3d-delivery` was 624,451 bytes with digest `sha256:e8e3822c6e9cb826d6dc58384632d22446d096c803be28f115bea717d0a4a034`.

The LightX2V operator route now minimizes the environment inherited by its inference subprocess: unrelated proxy settings, common secret-like credential variables, and interpreter/loader injection controls are stripped; `PYTHONPATH` is pinned to the reviewed checkout; legitimate local runtime controls such as CUDA visibility and `LD_LIBRARY_PATH` remain available; and Hugging Face/Transformers/Datasets offline plus telemetry-disable flags are forced. This is defense-in-depth for the existing offline operator route; it does not install, download, provision, call hosted services or consume credits.

The route also requires the recursively measured configured local model tree to contain **non-zero local file bytes** before GPU probe or inference. It then binds that tree by deterministic SHA-256 + total bytes before generation, records `generation_model_sha256` / `generation_model_size_bytes`, and recomputes the tree after generation. Empty, changed or unreadable model trees fail closed; changed generation state deletes the produced shot before quality acceptance.

The generated-video media gate validates ffprobe metadata shape, finite duration/fps, integer-convertible positive dimensions, conservative compositor-usability floors of **0.5 s duration, 256 px width, 256 px height and 8 fps**, exactly one complete raw terminal frame of **`width × height` bytes**, and aligned motion samples with sufficient temporal coverage. Those checks are necessary media integrity, not identity/action/semantic proof.

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
- `docs/research/2026-09-01-lightx2v-nonempty-model-preflight.md`
- `docs/research/2026-09-01-lightx2v-offline-environment-isolation.md`
- `docs/research/2026-09-01-lightx2v-runtime-injection-environment.md`

The previous LightX2V protections remain in force: bounded local NVIDIA preflight; fresh target invalidation; offline and runtime-bounded execution; exact request/source/config provenance; rights-safe I2V reference SHA-256 + byte-count + rights binding; rejection of source/config/reference/model mutation; dirty/ambiguous source, untracked importable runtime files and escaping tracked-symlink rejection.

`PROJECT.md` remains intentionally unchanged: runtime-injection filtering is a stricter implementation of the existing zero-cost/offline/secret-safety, source-provenance and fail-closed operator-owned doctrine, not a new durable product direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact non-empty local model bytes, reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, independently verifiable source/config provenance, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, correct duration/frame count, decodability, non-empty/stable model bytes, generic motion or clearing the media floor never prove requested action, subject identity or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** remains the primary tested operator-owned framework candidate; do not repin for freshness alone. Admit a newer revision only when license/runtime review and Hottop same-case evidence show material value for Wan2.2 I2V identity/requested-action quality or a measured runtime gap.
- The official **Wan2.2-I2V-A14B** path remains model-byte-bound at runtime. Hottop does not infer provenance or quality from a model/directory name.
- Upstream warnings that successful generation can still be static, degraded or semantically meaningless remain relevant: provenance/media integrity and semantic/identity/requested-action gates stay separate.
- Specialized acceleration/model forks remain gated where effective execution composes external weights/LoRAs/compiled assets without a fully reviewed code+weights+artifact provenance/license chain and Hottop same-case evidence.
- **Qwen3-TTS** remains an operator-owned local benchmark candidate; serving/runtime freshness does not enter unattended production without exact model/runtime/license provenance and same-line Mandarin evidence.
- No candidate currently clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact non-empty Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact model/request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition; valid metadata and stable bytes are necessary but not sufficient.
4. Continue hardening only concrete operator-route gaps that can be proven with tests without pretending they substitute for real generated-media evidence.
5. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
6. Continue targeted ecosystem radar around measured gaps; do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
