# Hottop Status

Last updated: 2026-09-01
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production-code point is **`d372c6709ab32dbcdd1fe25ab13025c540c1873c`** (`Fail closed on escaping LightX2V model symlinks`, PR #406), SHA-locked squash-merged from exact verified head `824a57122fe91f8898278f2f6bc6d5cef240dd06`.

Latest merged repository/evidence point is **`main@a15214f41d328631757eb4435db861a9242d65d5`** (`Record LightX2V model symlink boundary evidence`, PR #407). Its exact main push CI #2692 completed successfully. There are no open PRs at this recovery point.

Latest TDD/production evidence:

- RED `88615b4bd931cfce78a5e3c78da381c3c2deb0f9`: CI #2687 failed the new escaping-model-symlink regression because the old model provenance walker followed a symlink from inside the reviewed model root to bytes outside it. Python 3.12 was cancelled by fail-fast and is not relied upon as RED evidence.
- Intermediary `b853410c89233e2430b41a83f561e6fe160df702`: the implementation already failed closed, but CI #2688 exposed an over-specific diagnostic expectation; result was `1 failed, 657 passed`. The behavioral assertion was retained while coupling to the internal wrapper message was removed.
- GREEN exact head `824a57122fe91f8898278f2f6bc6d5cef240dd06`: model-tree symlinks must resolve strictly inside the reviewed model root before any GPU probe/inference. Internal links remain allowed. CI #2689 passed Ruff + full pytest on Python 3.11 and 3.12.
- production-smoke #335 passed the checked-in zero-cost software3d cow + Odyssey execution plus final-media/provenance verification; artifact `hottop-software3d-production-smoke` is **687,895 bytes**, digest `sha256:f5b4c912b86a9e07c886fbd8b5a454536ee4eb45c4e25d6d34158467e353fdf3`.
- cinematic-delivery-smoke #202 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification; artifact `hottop-cinematic-software3d-delivery` is **624,453 bytes**, digest `sha256:a6a8d9f495cd6ef2dcf3fc7acac067123285126d386acc6696131dda786d1b15`. Seam evidence: `intra_p95=0.934`, `max_delta=4.185`, `max_ratio=4.481`.

Latest durable production evidence record: `docs/research/2026-09-01-lightx2v-model-symlink-boundary.md`. Earlier 2026-09-01 records remain the detailed evidence history for strict JSON parsing, credential/runtime isolation, model/source/config/reference byte binding and generated-video media integrity.

`PROJECT.md` remains intentionally unchanged by #406/#407: bounding model symlinks to the reviewed local model root is a stricter implementation of existing ZERO_COST/local-preflight/fail-closed/provenance doctrine, not a new durable product direction.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Local preflight requires a reviewable checkout, recursively measured non-empty local model tree, strict-standard-JSON object config with no duplicate object names, an available local Python runtime and existing GPU/runtime requirements before inference.

The measured model byte boundary is now self-contained: symlinks found under `model_path` must resolve strictly inside the resolved reviewed model root. Escaping, broken or cyclic links fail closed before GPU probe/inference; internal links remain allowed. Generation is still bound to the resulting exact model-tree bytes, and model mutation during inference discards output.

The operator subprocess remains network-offline and least-authority: proxy settings, common secrets/credential handles and interpreter/loader injection controls are stripped; reviewed checkout `PYTHONPATH`, `PYTHONNOUSERSITE=1`, Hugging Face/Transformers/Datasets offline flags and telemetry-disable flags are forced. No install, download, hosted call, paid fallback or GPU provisioning occurs.

Generation remains bound to exact model bytes, generation request, source revision, config bytes, rights-safe reference bytes and generated-shot bytes. Source/model/config/reference mutations during generation fail closed and discard output. Input locks and byte stability are necessary provenance constraints, not output-quality proof.

Generated-video media gates continue to enforce ffprobe structure, finite duration/fps, positive dimensions, compositor floors, complete terminal raw frames, aligned motion samples and temporal coverage. **Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Runtime success, decodability, stable bytes or generic motion never prove subject identity, requested action or semantic correctness.

The next real quality gate remains generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated. Voice cloning/reference audio is rights-gated.

`mingshi2333/Qwen3-TTS-ncnn` remains a gated Apache-2.0 local-runtime candidate. It targets CPU/Vulkan Qwen3-TTS execution, but Hottop still lacks a rights-safe same-line Mandarin A/B with exact model/runtime provenance against the current 1.7B target. Its dependency/model acquisition paths must remain operator-provisioned; unattended Hottop must not fetch them.

## Fresh ecosystem radar — 2026-09-01

- **LightX2V** public `main` remains `26cfa87782e109ffdccb20d5f437561cefa9a530` (`fix: prevent first-step recompilation in MiniMax-H3 attention (#1469)`). This is MiniMax-H3 compile-performance maintenance, not same-case Wan2.2 I2V identity/requested-action evidence; there is **no freshness-only repin**.
- The upstream checkout currently declares three ROS/simulator submodules (`LIBERO`, `RoboTwin`, `RoboLab`). Existing Git clean-check behavior already detects initialized gitlink commit drift/dirty tracked state; these simulator submodules are not evidence of a Wan2.2 I2V production-quality gain, so Hottop does not add speculative submodule-specific inference machinery without a demonstrated gap.
- Open upstream reports still separate successful execution from useful output: #895 reports correct-length I2V output with static frames, #1170 reports meaningless color/light output, #603 reports materially worse content/motion than a comparable Diffusers path, and #1246 reports image-conditioning LoRA keys that fail to match during a Wan2.2 distilled merge path.
- Distilled/accelerated Wan2.2 I2V routes remain gated where exact code+weights+config provenance, image-conditioning correctness, license chain or Hottop same-case identity/requested-action quality is unproven.
- Qwen3-TTS alternate runtimes remain candidates, not unattended defaults, until exact code/weights/runtime/license review plus same-line Mandarin listening evidence demonstrates measurable value.
- No candidate currently clears admission strongly enough to replace the guaranteed software3d route or the reviewed LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, exact non-empty Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **media integrity/quality + identity + requested-action motion + exact model/request/source/config/reference/generated-byte provenance** across all subject-bearing shots before composition.
4. Extend local LightX2V validation only when a version-safe requirement is proven by RED→GREEN evidence; do not grow a guessed upstream field schema or speculative provenance checks disconnected from the actual inference path.
5. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
6. Continue targeted ecosystem radar around the measured gap; no freshness-only pins, large dependencies, hosted paid fallback or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
