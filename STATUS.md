# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified live-main evidence in this snapshot: **`main@6c881f2969d64ae0c7b26f45fc6a75046d86249b` → CI #2014 passed** on Python 3.11/3.12. That commit is the squash merge of PR #173 after exact-head CI #2013 passed.

PR #173 persisted a fresh third-party Qwen3-TTS runtime repeatability report. Follow-up inspection of merged MLX-Audio PR #895 clarified the root cause: the reported `Qwen3-TTS-12Hz-1.7B-Base-bf16 --voice Chelsie` path was not valid preset-speaker conditioning. Base checkpoints expose no preset-speaker table; MLX-Audio silently ignored the unsupported `--voice` and generated unconditioned speech. Upstream fixed this by rejecting unsupported voices on Base checkpoints and correcting examples to use real CustomVoice preset speakers.

Current doctrine therefore keeps **two independent TTS gates**:

1. capability binding before execution — requested preset speaker/voice/instruction/reference conditioning must be supported by the exact runtime/checkpoint; unsupported conditioning fails closed rather than silently degrading to unconditioned speech;
2. output evidence after execution — repeated trials still verify speaker consistency, onset stability, intelligibility, naturalness, PCM integrity/duration and exact WAV provenance.

This correction is runtime/checkpoint-specific evidence. It does **not** establish a defect in official Qwen CustomVoice, qwentts.cpp, Qwen3-TTS-ncnn or the Qwen model family.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest retained deterministic smoke evidence remains:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey delivery: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` derived from the exact ordered subject-bearing plan semantics; generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

`qwen3-tts-ncnn-0b6` and `qwen3-tts-qwentts-cpp-1b7` remain **benchmark candidates only** with `integration_ready=false / runtime_status=unprobed`.

The qwentts.cpp read-only input binder remains:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

It requires local non-empty files, executable binary permission, official `GGUF` magic on both model files, and records resolved path + byte size + SHA-256. It never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime status or claims Mandarin quality. `ready=true` means only that supplied benchmark inputs are structurally GGUF-like and byte-bound.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, exact model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V:** upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6` (2026-08-28, `Update scripts (#1452)`). The change only replaces private hard-coded paths with `/path/to/...` examples in a Wan-Animate-2 distillation script. No Hottop-measured continuity, quality or runtime gain for the tested Wan2.2 I2V subset; keep the tested pin and **do not freshness-only repin**.
- **Qwen3-TTS official:** upstream `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no official change removes the operator-local 1.7B benchmark gate.
- **qwentts.cpp:** upstream `master` remains `a8a7716b530e49fed537c57711247c12fbbb903c`; no newer commit was observed. Existing seedable sampling, `max_new_tokens`, 1.7B CustomVoice GGUF and CPU/CUDA/Metal/Vulkan support improve benchmark practicality but do not alter Hottop admission.
- **MLX-Audio #892/#895:** the reported repeated-voice issue was caused by an unsupported Base-model preset speaker being silently ignored. Upstream now rejects this invalid conditioning. Hottop retains repeated speaker consistency as a post-generation quality gate while adding fail-closed capability binding before synthesis.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or the current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first; only after byte/structure preflight passes may a separate explicit same-line Mandarin A/B execute.
4. Before any neural-TTS benchmark execution, fail closed if the requested speaker/voice/instruction/reference-conditioning mode is unsupported by the exact checkpoint/runtime. Never silently drop conditioning.
5. In real Qwen 1.7B A/B, preserve repeated speaker consistency, short-onset stability, intelligibility/naturalness, latency/RTF, PCM duration/integrity and exact runtime/model/output provenance as separate evidence dimensions.
6. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
7. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
