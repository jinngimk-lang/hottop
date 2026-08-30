# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@6bbfe4a0f4734eeb3139aa1808277ea76b5607e4` / CI #2300** on Python 3.11/3.12.

The local Qwen3-TTS benchmark evidence surface now closes seven concrete coherence gaps:

- cold/warm completeness per candidate;
- one exact runtime revision per candidate;
- one exact model/checkpoint revision per candidate;
- one benchmark-wide finite generation protocol with canonical SHA-256;
- **concrete generation controls**: a ready generation protocol must contain an integer `seed`, positive integer `max_new_tokens` generation ceiling and at least one explicit sampling control (`temperature`, `top_p`, `top_k` or nonblank `sampling_mode`). Purely descriptive JSON such as `{ "note": "same settings" }` is not sufficient; `temperature=0` remains a valid explicit greedy protocol;
- one benchmark-wide finite hardware profile with canonical SHA-256;
- **concrete hardware identity**: a ready latency/RTF benchmark must name a nonblank execution `backend` plus at least one nonblank `cpu`, `gpu` or generic `accelerator` identity. A label such as `{ "note": "same machine" }` is no longer sufficient.

Latest TDD chain for the generation-control closure:

- RED exact head `4278fe3532e9578061579830ab08d3a7ad88160d`, CI **#2296**: Ruff passed; pytest failed on the new concrete-generation-control contract and the other matrix job was cancelled by fail-fast;
- GREEN implementation `52e93e2bcf57b573284878653a68c2be0d756209`, CI **#2297**: Python 3.11/3.12 Ruff + full pytest passed;
- durable-record head `7f5fee18f79a74c81a5a3e41b7d8755b0b4201fe`, CI **#2298**: both Python versions passed;
- the ready-for-review connector hit the known GitHub `fullDatabaseId` GraphQL compatibility error, so draft #278 was closed and non-draft #279 was recreated on the **same exact verified head**, with no history/code change;
- exact-head squash merge `6bbfe4a0f4734eeb3139aa1808277ea76b5607e4`, post-merge **CI #2300**: both Python versions passed.

The generation protocol remains **declared benchmark-control provenance, not proof that a runtime internally obeyed similarly named flags**. Operator execution records and actual CLI/config provenance remain separately required; incompatible control semantics across runtimes require separate protocol/candidate design rather than superficial key matching.

The hardware profile likewise remains **declared measurement provenance, not proof that the declared machine was actually used**. Runtime execution records and local environment provenance remain separately required. Different candidate hardware belongs in separate benchmark evidence sets instead of one directly comparable latency/RTF surface.

No neural runtime execution, provider route, dependency, model download, GPU provisioning, credential or paid path was added by this closure.

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

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor, LongCat-Video-Avatar, DiffSynth/MiniMax-H3 NF4 and other reviewed routes remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available; reviewed manual v0.7.0 runtime archives remain operator-provisioned only;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Shared evidence surface:

`hottop-models inspect-tts-benchmark --spec <benchmark.json>`

It inspects already-produced local WAVs only and never executes TTS, accesses the network, installs dependencies, downloads models, provisions GPU resources or calls a paid service.

A ready benchmark requires:

- exact text, language and checkpoint-supported preset speaker;
- one finite JSON generation protocol for the whole benchmark, canonical SHA-256, integer seed, positive `max_new_tokens` ceiling and at least one explicit validated sampling control; descriptive metadata without concrete controls fails closed;
- one non-empty finite JSON hardware profile for the whole benchmark, with canonical SHA-256, nonblank backend and concrete CPU/GPU/generic-accelerator identity;
- at least one `cold` and one `warm` trial for every candidate; additional independent warm repeats remain preferred;
- one exact `runtime_revision` and one exact `model_revision` per candidate;
- finite positive latency;
- a distinct resolved WAV path for every trial; identical bytes remain legal when independently produced as separate artifacts;
- WAV/PCM integrity and `listening_required=true` so speed/stream integrity cannot be mistaken for naturalness or speaker-quality proof.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker, one declared and semantically comparable generation protocol, and one actually comparable hardware evidence set while preserving runtime/model/config provenance, cold/warm timing, distinct WAV artifact instances, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed before execution; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **Qwen3-TTS runtime resource signal:** recent llama.cpp Qwen3-TTS discussion reports that a default 32768-token context can reserve roughly 3.5 GB of KV cache while a much smaller context may be sufficient for the tested workload. This is runtime-specific evidence, not a Hottop default recommendation; future operator A/B must bind the actual runtime/config/context rather than claiming performance from model support alone.
- **Qwen3-TTS benchmarking:** current public benchmark practice continues to bind concrete hardware, cold/warm protocol and runtime/model configuration. SGLang-Omni's fixed-protocol work remains a useful signal that acceleration claims must survive repeatable end-to-end measurement rather than being inferred from an optimization toggle.
- **Qwen3-TTS official source:** the latest reviewed official source remains gated behind operator-local 1.7B assets for Hottop quality claims; no fresh evidence in this cycle clears that gate.
- **LightX2V/Wan2.2:** no reviewed change in this cycle produced Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- Existing DiffSynth/MiniMax-H3, Motion Lab, LongCat, Step-Audio-EditX and other research gates remain unchanged; no candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line local WAV generation and inspect a benchmark with the concrete generation-control + hardware-identity contracts above. Keep listening/speaker/onset evidence independent from speed.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
5. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
