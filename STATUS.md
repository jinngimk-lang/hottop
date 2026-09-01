# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@0415e0ff59042dc923c3f08c7e5a1a43da8d09c3`** (`Fail closed on LightX2V runtime injection environment`, PR #388), SHA-locked squash-merged from exact verified head `5b291939994b611dfd4083786fcf65e2c20652ae`.

Latest TDD/production evidence:

- RED exact head `653521087bb1f57f892539412037965b20ff854c`: CI #2634 reached clean Ruff and failed pytest on the new regression proving that `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP` and `PYTHONINSPECT` were still inherited by the LightX2V child process. Python 3.12 reached the failing pytest step and was cancelled by fail-fast after the failure was demonstrated.
- GREEN exact head `5b291939994b611dfd4083786fcf65e2c20652ae`: the LightX2V child environment now strips those interpreter/loader injection controls while preserving legitimate local CUDA library configuration such as `LD_LIBRARY_PATH`; CI #2635 passed Ruff + full pytest on Python 3.11 and 3.12.
- production-smoke #316 passed checked-in anti-polish cow + cinematic Odyssey execution, final-media/provenance verification and evidence upload; artifact `hottop-software3d-production-smoke` was 687,895 bytes with digest `sha256:7f3c4097e14bf192978c5f936853b818d430b4234fe05dca7a32998a80e5d17c`.
- cinematic-delivery-smoke #183 passed actual 720p24 Odyssey delivery, runtime provenance, final-media verification and evidence upload; artifact `hottop-cinematic-software3d-delivery` was 624,451 bytes with digest `sha256:e8e3822c6e9cb826d6dc58384632d22446d096c803be28f115bea717d0a4a034`.

PR #386 immediately before this change had already removed proxy settings and common secret-like `*_API_KEY`, `*_TOKEN`, `*_SECRET`, and `*_PASSWORD` variables from the operator inference child environment. Together, #386 and #388 prove a durable boundary: operator-owned local inference subprocess environments are minimized provenance/safety scopes, not blanket copies of the parent process. Offline/telemetry-disable flags remain forced and justified local runtime controls remain available.

Durable records for this boundary:

- `docs/research/2026-09-01-lightx2v-offline-environment-isolation.md`
- `docs/research/2026-09-01-lightx2v-runtime-injection-environment.md`
- `docs/superpowers/specs/2026-08-24-zero-cost-video-backend-design.md`

The LightX2V route also retains bounded local NVIDIA preflight; no auto-install/model download; recursively non-empty model-byte preflight; deterministic model/config/request/reference/generated-byte provenance; fresh-target invalidation; exact source identity; dirty/untracked-importable/escaping-symlink rejection; post-generation source/model/config/reference stability checks; generated-media integrity gates; and separate output-side identity/requested-action evidence.

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

- **LightX2V** public `main` advanced to `1d5eb0d6f1df8e7a78568361ed9cca9037ccda89` on 2026-09-01. The latest change updates MiniMax H3 DMD2 training configuration, not Hottop-measured Wan2.2 I2V identity/requested-action quality. Continue **no freshness-only repin**.
- Upstream LightX2V/Wan2.2 reports still show that successful execution can yield degraded/static/invalid semantic output, reinforcing separation of provenance/media integrity from identity/action/semantic quality.
- **Qwen3-TTS / SGLang-Omni** has current serving/quality optimization signals, including Mandarin CER improvements and H100 serving work, but remains operator-owned benchmark-only until exact runtime/model/license provenance and same-line Hottop Mandarin evidence win. No unattended dependency is admitted from freshness alone.
- Specialized acceleration/model forks remain gated where effective execution composes external weights/LoRAs/compiled assets without a fully reviewed code+weights+artifact provenance/license chain and Hottop same-case evidence.
- No candidate currently clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Persist the now-proven operator-inference environment-minimization rule in `PROJECT.md` and the zero-cost video design spec in the same workstream; treat it as superseding the weaker assumption that offline flags plus clean source identity alone fully scoped local execution.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. When a reviewed local LightX2V checkout, exact non-empty Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
4. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact model/request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition; valid metadata and stable bytes are necessary but not sufficient.
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
