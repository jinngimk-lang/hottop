# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@831c41ebf601a7941dbcbfffed9cfc8d2e196a09` / CI #2391** on Python 3.11/3.12. The merge closes the Pure-C Qwen3-TTS 1.7B safetensors header-allocation bound described below. Every later recovery must still re-fetch live `main`, open PRs and exact-head CI before treating this historical evidence point as current.

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

Input locks are constraints, not output proof. Generated continuity evidence must cover **all subject-bearing shots** and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Reviewed alternatives remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates now include:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight;
- `qwen3-tts-pure-c-1b7` — read-only raw-safetensors model-tree preflight, registry-discoverable but `integration_ready=false` and `runtime_status=unprobed`;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

The Pure-C route is bound to exact source `gabriele-mastrapasqua/qwen3-tts@f1b6865713d12a2a2365282fc02e19a5a384a565`. Its manifest forbids normal `video-run`, auto-build and upstream `download_model.sh` / `download_voices.sh`; only operator-provisioned source/build plus independently bound official Qwen model bytes may enter the same-line Mandarin benchmark.

Pure-C preflight now closes three checkpoint-input/resource false-ready classes. First, SHA-bound `config.json` parsing requires `model_type=qwen3_tts`, `tts_model_type=custom_voice` and `tts_model_size=1b7`, so the shared upstream file layout cannot let Base, VoiceDesign or 0.6B trees masquerade as 1.7B CustomVoice. Second, RED CI #2378 proved that arbitrary non-empty bytes renamed to `.safetensors` could still pass the old generic file binder. GREEN CI #2380 and final exact-head CI #2382 added a shallow safetensors container gate in the same stable-filesystem/streaming-SHA pass: the 8-byte header length must fit the file, the JSON header must contain at least one structurally valid tensor descriptor, and declared data offsets must remain inside the actual bound data region. That fix merged as `44779086804ef9c734909447c8cc3bf01eb4f9d4`; post-merge CI #2384 is green. Third, RED CI #2387 proved that a declared safetensors JSON header still had no explicit allocation ceiling. GREEN exact-head CI #2389 added the upstream `100,000,000`-byte header limit, rejecting larger headers before allocating/reading them while continuing fixed-size streaming SHA-256 of the complete file. That resource-safety fix merged as `831c41ebf601a7941dbcbfffed9cfc8d2e196a09`; post-merge CI #2391 is green. These gates do not load tensors. `ready=true` still proves only local input structure/provenance, not checkpoint revision, rights, runtime success, speaker capability or Mandarin quality.

`hottop-models inspect-tts-benchmark --spec <benchmark.json>` treats latency/RTF as comparable evidence only when it binds:

1. exact text, language and checkpoint-supported preset speaker;
2. one concrete generation protocol with canonical SHA-256, integer seed, positive `max_new_tokens` and an explicit sampling control;
3. one concrete hardware profile with canonical SHA-256 plus coherent backend/device identity;
4. one recognized execution profile (`cli` or `server`) with positive concurrency and batch size; `server` additionally requires connection strategy;
5. at least one cold and one warm trial per candidate, while additional independent warm repeats remain first-class evidence for repeated-run speaker consistency and warmed-runtime variance;
6. one exact runtime revision and one exact model/checkpoint revision per candidate;
7. finite positive latency plus distinct resolved WAV artifact paths, byte identity and WAV/PCM integrity;
8. `listening_required=true`, keeping naturalness, speaker consistency, onset stability and intelligibility independent from speed/stream integrity.

Declared generation/hardware/execution profiles are measurement provenance, not proof that a runtime obeyed them. Operator execution records and actual invocation/config provenance remain separately required. Future 1.7B cross-runtime A/B must use the same Mandarin line, same supported preset speaker and semantically comparable generation controls, while retaining multiple warm repeats, short-onset checks, intelligibility/naturalness and publication-rights review.

Durable rationale: `docs/research/2026-08-30-tts-bench-method-admission.md`, `docs/research/2026-08-30-tts-execution-shape-evidence.md`, and `docs/research/2026-08-30-qwen3-tts-pure-c-admission.md`.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` remains **`7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`**. The current tip is still `Update scripts (#1452)` from 2026-08-28; the reviewed change only removes private hard-coded example paths and provides no Hottop-measured continuity/quality/runtime gain for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS** official `main` remains **`022e286b98fbec7e1e916cb940cdf532cd9f488e`**. No official change in this cycle removes the operator-local 1.7B benchmark gate.
- **Pure-C Qwen3-TTS** public `main` remains the reviewed **`f1b6865713d12a2a2365282fc02e19a5a384a565`**. Its local CPU/Metal/CUDA support and seeded generation remain implementation evidence only; Hottop has not reproduced Mandarin naturalness, onset stability, repeated speaker consistency, delivery control or latency.
- **qwentts.cpp** reviewed `master` remains **`a8a7716b530e49fed537c57711247c12fbbb903c`**. No new revision changes the current admission.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR, audio.cpp or the Pure-C runtime plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line local WAV generation and inspect it with the generation + hardware + recognized execution-shape coherence contracts above. Retain actual invocation/config separately because declared profiles are not execution proof.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
