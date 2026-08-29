# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest live-main evidence point before the current CrispASR admission workstream: **`main@f81346871437c59000acc0aa469ddb93d51d5470`**, with CI #2092 passed on Python 3.11/3.12 and no open PR at recovery.

The current workstream adds a second independent local C++/GGUF runtime candidate for the unresolved Qwen3-TTS 1.7B Mandarin benchmark without changing the guaranteed production route. TDD evidence:

- RED `ebc892f62be62ff44a7724e8c99ea520baa30b4c` → CI #2094: Ruff passed; pytest failed because `qwen3-tts-crispasr-1b7` did not yet exist in the model hub.
- GREEN implementation `52bbd47de55c1ef80665d7dbc968d95201617913` added only the benchmark-only model-hub entry, focused selection contract and durable admission record → CI #2096 passed on Python 3.11/3.12.
- PR #210 remains benchmark/admission scope only. No executable adapter, model download, build/install path, GPU provisioning, credentials, paid call or production routing change is part of this workstream.

The prior qwentts.cpp preflight closure remains intact. Hottop requires model inputs to be non-empty, GGUF-magic-correct, at least 24 bytes, fixed-header version `3`, and to declare at least one tensor. Existing protections remain: symlinks resolve before identity binding; bounded 1 MiB streaming SHA-256; before/after device/inode/size/mtime_ns/ctime_ns/mode stability checks; executable permission checks; executable/talker/tokenizer path-or-byte role distinctness; no execution/network/download/build/GPU provisioning/runtime-ready promotion.

`ready=true` for qwentts therefore means only: operator-supplied local inputs were present, shallowly GGUF-structured for the currently reviewed version where applicable, stable during preflight, exact-byte-bound to resolved targets, non-zero-tensor for model roles, and distinct across required executable/talker/tokenizer roles. It does **not** prove semantic checkpoint identity, model/tokenizer/checkpoint rights, qwentts runtime compatibility, checkpoint speaker capability, synthesis success or Mandarin quality.

Durable qwentts records include:

- `docs/research/2026-08-29-qwentts-distinct-role-artifacts.md`;
- `docs/research/2026-08-29-qwentts-executable-role-distinctness.md`;
- `docs/research/2026-08-29-qwentts-gguf-tensor-count.md`;
- `docs/research/2026-08-29-qwentts-gguf-version.md`.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest retained deterministic smoke evidence:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` derived from exact ordered subject-bearing plan semantics; generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

`qwen3-tts-ncnn-0b6`, `qwen3-tts-qwentts-cpp-1b7` and `qwen3-tts-crispasr-1b7` are **benchmark candidates only** with `integration_ready=false / runtime_status=unprobed`.

Read-only qwentts input preflight:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

The executable, talker and tokenizer/codec must be three distinct artifacts; same resolved path or same exact SHA-256 across incompatible roles fails closed. Model GGUF inputs must have a complete fixed header, use reviewed GGUF version `3`, and declare at least one tensor. The preflight never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime state or claims audio quality.

CrispASR is admitted only as a second **operator-provisioned cross-runtime benchmark candidate** at exact reviewed source `bb77301c4dbde1fca217e1a19584b1ae0167ee03`. Source is MIT; reviewed `cstr` 1.7B CustomVoice GGUF and tokenizer/codec model cards declare Apache-2.0 conversions of the official Qwen Apache-2.0 assets. CrispASR supports `-m auto`, which downloads models on first use; Hottop must never invoke that path. There is no executable CrispASR adapter yet. Preset CustomVoice is the initial benchmark scope and reference-audio cloning remains separately rights-gated.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Capability binding remains independent from output evidence: unsupported speaker/voice/instruction/reference conditioning must fail closed before execution; repeated trials still verify actual speaker consistency and output integrity afterward.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** reviewed upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`; latest reviewed change only cleaned hard-coded Wan-Animate-2 example paths and provides no Hottop-measured continuity/quality/runtime gain. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change in this cycle justifies changing the 1.7B operator-local benchmark gate.
- **qwentts.cpp:** reviewed `master` remains `a8a7716b530e49fed537c57711247c12fbbb903c`. No reviewed upstream change in this cycle justifies automatic serving/build integration. Existing server/performance reports remain inputs to future benchmark topology rather than reasons to widen the unattended route.
- **CrispASR:** exact reviewed source `bb77301c4dbde1fca217e1a19584b1ae0167ee03` is MIT and includes a local Qwen3-TTS 1.7B CustomVoice GGUF path on CPU/CUDA/Metal/Vulkan. Its documented `-m auto` path downloads assets and is excluded from Hottop unattended execution. Public issue #183 reports roughly `0.5–0.76` RTF after a native-GQA fix for a 1.7B CustomVoice Q8_0 path on AMD RDNA4/Vulkan; Hottop records this only as runtime-specific benchmark evidence, not Mandarin-quality proof. The reviewed `cstr` 1.7B CustomVoice GGUF and tokenizer cards both declare Apache-2.0 and direct provenance to the official Qwen assets.
- **llama.cpp `llama-tts`:** remains research-only for this measured gap. A 2026-08-07 Qwen3-TTS 1.7B Base/Vulkan report reproduced phrase repetition and missed codec EOS before being fixed; a 2026-08-10 Vulkan GET_ROWS assertion report remains open. These runtime-specific failures reinforce Hottop's bounded-generation and final PCM-duration/integrity gates, but do not justify replacing the reviewed qwentts.cpp CustomVoice benchmark route or adding a new unattended runtime.
- **WildActor:** remains a research-only multi-reference identity signal because reviewed source/checkpoint/data/reference/API/runtime rights are not all cleared.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or current tested operator video route. CrispASR only improves the future **cross-runtime TTS benchmark surface**.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first. Only after resolved-target + stable-snapshot + bounded-memory + complete-fixed-header + reviewed-GGUF-version-3 + non-zero-tensor + exact-byte + three-role-distinct preflight passes may a separate explicit same-line Mandarin A/B execute.
4. If an operator instead provisions CrispASR plus exact 1.7B CustomVoice talker/tokenizer GGUF assets locally, **do not use `-m auto`**. Bind exact source/build/backend and model bytes first, then run the same Mandarin line/preset-speaker protocol so qwentts/CrispASR differences can be attributed to runtime rather than prompt drift.
5. For all CustomVoice A/B, use only checkpoint-supported preset speaker conditioning. Do not silently drop unsupported conditioning or reuse Base-only reference/latent registration semantics on a CustomVoice checkpoint.
6. In real Qwen 1.7B A/B, preserve repeated speaker consistency, short-onset stability, intelligibility/naturalness, latency/RTF, PCM duration/integrity and exact runtime/model/output provenance as separate evidence dimensions.
7. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
8. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
