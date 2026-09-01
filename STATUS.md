# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production-code point is **`main@36274812206e0f4a25434bd6ba45154598298264`** (`Fail closed on duplicate LightX2V config keys`, PR #404), SHA-locked squash-merged from exact verified head `bfe02fbdb03211bac44c1aba8097d1faea20bd97`.

Current docs/evidence workstream: PR **#405** (`owner/record-lightx2v-duplicate-json-evidence`) records the #404 evidence and refreshes this snapshot. It contains no production-code or doctrine change and should merge only after exact-head CI passes.

Latest TDD/production evidence:

- RED `ba9a13a7d04c50525ef246eecc86d4d958989cfd`: CI #2681 completed setup/install/Ruff on Python 3.11, then full pytest failed the duplicate-config-key regression because the old JSON decoder accepted `{"guidance_scale": 3.0, "guidance_scale": 7.5}` and reached the injected GPU probe. Python 3.12 is not relied upon as RED evidence.
- GREEN exact head `bfe02fbdb03211bac44c1aba8097d1faea20bd97`: `json.loads` now rejects duplicate object names recursively via `object_pairs_hook`, while preserving strict-constant and top-level-object validation without guessing revision-specific LightX2V fields. CI #2682 passed Ruff + full pytest on Python 3.11 and 3.12.
- production-smoke #332 passed the checked-in zero-cost software3d cow + Odyssey execution plus final-media/provenance verification; artifact `hottop-software3d-production-smoke` is **688,373 bytes**, digest `sha256:b4cd4cc1619468c4c0b14c673139a74a50ba089e90d124dab0c0d1fb1e267452`.
- cinematic-delivery-smoke #199 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification; artifact `hottop-cinematic-software3d-delivery` is **624,450 bytes**, digest `sha256:65940330d3f9c71b90e757d79cd031a7e484760f915eac7d5d7b7a831991dff2`.

Latest durable production evidence record: `docs/research/2026-09-01-lightx2v-duplicate-json-keys.md`. Earlier 2026-09-01 records remain the detailed evidence history for strict JSON constants, config shape, credential/runtime isolation, model/source/config/reference byte binding and generated-video media integrity.

`PROJECT.md` remains intentionally unchanged by #404: duplicate-key rejection is a stricter implementation of existing ZERO_COST/local-preflight/fail-closed/provenance doctrine, not a new durable product direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Local preflight requires a reviewable checkout, recursively measured non-empty local model tree, strict-standard-JSON object config with no duplicate object names, an available local Python runtime and existing GPU/runtime requirements before inference.

The operator subprocess remains network-offline and least-authority: proxy settings, common secrets/credential handles and interpreter/loader injection controls are stripped; reviewed checkout `PYTHONPATH`, `PYTHONNOUSERSITE=1`, Hugging Face/Transformers/Datasets offline flags and telemetry-disable flags are forced. No install, download, hosted call, paid fallback or GPU provisioning occurs.

Generation remains bound to exact model bytes, generation request, source revision, config bytes, rights-safe reference bytes and generated-shot bytes. Source/model/config/reference mutations during generation fail closed and discard output. Input locks and byte stability are necessary provenance constraints, not output-quality proof.

Generated-video media gates continue to enforce ffprobe structure, finite duration/fps, positive dimensions, compositor floors, complete terminal raw frames, aligned motion samples and temporal coverage. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, decodability, stable bytes or generic motion never prove subject identity, requested action or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated. Voice cloning/reference audio is rights-gated.

`mingshi2333/Qwen3-TTS-ncnn` remains a gated local-runtime candidate. It targets CPU/Vulkan Qwen3-TTS execution, but Hottop still lacks a rights-safe same-line Mandarin A/B with exact model/runtime provenance and the current 1.7B target. Its dependency/model acquisition paths must remain operator-provisioned; unattended Hottop must not fetch them.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public `main` remains `d7e064c4ec8dfe6a545e139156498abb8c108a3e` (`fix(mlu): make Sage attention compile safe (#1435)`). This is runtime/compiler maintenance, not same-case Wan2.2 I2V identity/requested-action evidence; there is **no freshness-only repin**.
- Open upstream reports still separate successful execution from useful output: #895 reports correct-length I2V output with static frames, #1170 reports meaningless color blocks/light patterns, and #603 reports materially worse content/motion than a comparable Diffusers path.
- Distilled/accelerated Wan2.2 I2V routes remain gated where exact code+weights+config provenance, image-conditioning correctness, license chain or Hottop same-case identity/requested-action quality is unproven.
- Qwen3-TTS alternate runtimes remain candidates, not unattended defaults, until exact code/weights/runtime/license review plus same-line Mandarin listening evidence demonstrates measurable value.
- No candidate currently clears admission strongly enough to replace the guaranteed software3d route or the reviewed LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Finish PR #405 by exact-head CI, merge if green, then re-fetch live `main`/open PR state.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. When a reviewed local LightX2V checkout, exact non-empty Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, generate at least two subject-bearing rights-safe I2V shots.
4. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact model/request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition.
5. Extend local LightX2V config validation only when a version-safe requirement is proven by RED→GREEN evidence; do not grow a guessed upstream field schema.
6. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
7. Continue targeted ecosystem radar around the measured gap; no freshness-only pins, large dependencies, hosted paid fallback or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
