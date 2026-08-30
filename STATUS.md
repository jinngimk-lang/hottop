# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@8f4c27ebf875eb41bbdb976777ed7b57dbaf799d` / CI #2407** on Python 3.11/3.12. This merge closes the TTS server worker/thread-topology evidence gap. Every later recovery must still re-fetch live `main`, open PRs and exact-head CI.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Reviewed alternatives remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight;
- `qwen3-tts-pure-c-1b7` — read-only raw-safetensors model-tree preflight, registry-discoverable but `integration_ready=false` and `runtime_status=unprobed`;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Pure-C remains bound to exact source `gabriele-mastrapasqua/qwen3-tts@f1b6865713d12a2a2365282fc02e19a5a384a565`. Its normal Hottop path forbids upstream model/voice downloads, auto-build and runtime execution. Its current preflight binds the intended 1.7B CustomVoice capability and performs bounded, metadata-only safetensors integrity/resource checks without loading tensors. `ready=true` still proves only local input structure/provenance, not checkpoint rights, runtime success, speaker capability or Mandarin quality.

`hottop-models inspect-tts-benchmark --spec <benchmark.json>` treats latency/RTF as comparable evidence only when it binds:

1. exact text, language and checkpoint-supported preset speaker;
2. one concrete generation protocol with canonical SHA-256, integer seed, positive `max_new_tokens` and explicit sampling control;
3. one concrete hardware profile with canonical SHA-256 plus coherent backend/device identity;
4. one recognized execution profile (`cli` or `server`) with positive concurrency and batch size;
5. for `server`, nonblank connection strategy plus positive `worker_count` and `threads_per_worker`;
6. cold/warm coverage, with additional independent warm repeats retained for warmed variance and repeated speaker-consistency evidence;
7. one exact runtime revision and one exact model/checkpoint revision per candidate;
8. finite positive latency plus distinct resolved WAV artifact paths, byte identity and WAV/PCM integrity;
9. `listening_required=true`, keeping naturalness, speaker consistency, onset stability and intelligibility independent from speed/stream integrity.

The server-topology closure was TDD-verified: RED `fa917df5e9e730994e2a01cee0717215ffea96de` passed Ruff and produced exactly **1 failed / 602 passed** because missing worker/thread topology still returned `ready=true`; GREEN `faf5141e1bc3197fdfcb675cbb83ad998a69e5af` passed CI #2404; final documented head `b041ba287f21f1607d2ae73f175d0bb3536e539c` passed CI #2405; the squash merge `8f4c27ebf875eb41bbdb976777ed7b57dbaf799d` passed post-merge CI #2407.

This gate is motivated by fresh 2026-08-29 Pure-C server evidence: process/prefork and per-worker thread shape can materially affect CPU utilization under concurrent requests. Declared worker topology is measurement provenance, **not proof the runtime honored it**; retain actual invocation/config evidence separately.

Durable rationale: `docs/research/2026-08-30-tts-bench-method-admission.md`, `docs/research/2026-08-30-tts-execution-shape-evidence.md`, and `docs/research/2026-08-30-qwen3-tts-pure-c-admission.md`.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` remains **`7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`**. The current reviewed tip is script/example maintenance and provides no Hottop-measured continuity/quality/runtime gain for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS** official `main` remains **`022e286b98fbec7e1e916cb940cdf532cd9f488e`**. No official change removes the operator-local 1.7B benchmark gate.
- **Pure-C Qwen3-TTS** public `main` remains reviewed **`f1b6865713d12a2a2365282fc02e19a5a384a565`**. Fresh issue #24 (2026-08-29) reinforces that server worker/process/thread topology belongs in performance provenance; it does not constitute a Hottop quality or speed result.
- **qwentts.cpp** reviewed `master` remains **`a8a7716b530e49fed537c57711247c12fbbb903c`**. No new revision changes current admission.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR, audio.cpp or Pure-C plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line Mandarin generation and inspect it with the generation + hardware + execution-shape coherence gates above. Preserve actual invocation/config separately from declared benchmark profiles.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
