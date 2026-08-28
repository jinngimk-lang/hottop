# Hottop Status

Last updated: 2026-08-28
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production merge in this snapshot: **PR #168 `prod: add qwentts.cpp benchmark input preflight`**, squash-merged as `9bac5ea9c32e4a70ec2229b39e87d6454fbdab78`.

TDD evidence for #168:

- initial test head `bd2c8c94…` was blocked by Ruff and was **not** accepted as behavioral RED;
- isolated RED `29a7f0206b11fdbbf63f1a21ca0b350f7530cfea` → **CI #1998** passed Ruff and failed pytest because the qwentts.cpp preflight module/CLI did not exist;
- GREEN implementation `d8ab9ef8d102907dac27845abc724e15650ae239` → **CI #2000** passed Ruff + full pytest on Python 3.11/3.12;
- full-lint verification `991ebffcfa214009c65d8769af45db4d7ec5f5da` → **CI #2001** passed Ruff + full pytest on Python 3.11/3.12;
- final documented exact head `759ed5e13c4eaaa6accde1e031edceb4d8dd25d1` → **CI #2002** passed Ruff + full pytest on Python 3.11/3.12, with no review threads;
- post-merge `main@9bac5ea9c32e4a70ec2229b39e87d6454fbdab78` → **CI #2003** passed on Python 3.11/3.12.

The new command is a read-only benchmark-input binder:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

It requires local non-empty files, requires the executable bit on the binary, and records resolved path + byte size + SHA-256. It never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime status, or claims Mandarin/audio quality. `ready=true` means only that the supplied local benchmark inputs are structurally present and byte-bound.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest independently retained deterministic smoke evidence remains:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey delivery: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** When motion or anti-copy evidence is claimed, `hottop.reference-continuity-benchmark.v1` requires `motion_spec_sha256`, derived from the exact ordered subject-bearing plan fields (`scene`, `intent`, `continuity_instruction`, `generation_prompt`, `negative_prompt`). Generic motion cannot be reused as proof for different requested action semantics.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

`qwen3-tts-ncnn-0b6` remains a **benchmark candidate only**. It targets the 0.6B CustomVoice line through CPU/Vulkan and can lower hardware cost, but Hottop has not reproduced Mandarin naturalness or production quality. Normal Hottop must not invoke its automatic ncnn/model provisioning paths.

`qwen3-tts-qwentts-cpp-1b7` remains a separate **1.7B benchmark candidate only**. Reviewed source `ServeurpersoCom/qwentts.cpp@a8a7716b530e49fed537c57711247c12fbbb903c` is MIT and exposes Qwen3-TTS 1.7B CustomVoice through local GGUF on CPU/CUDA/Metal/Vulkan. The new #168 preflight removes manual artifact-binding ambiguity but does **not** make this route integration-ready or runtime-ready.

Future qwentts.cpp execution still requires operator-provisioned source/build plus exact local talker/tokenizer GGUF bytes. After the read-only preflight passes, a real benchmark must bind build/backend, GGUF bytes, exact Mandarin line, preset speaker, seed/sampling/generation ceiling, produced WAV bytes, serialized-PCM integrity/duration, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Voice cloning remains separately rights-gated.

Speech execution remains fail-closed across independent layers: semantic dialogue input validation, non-empty/finite/non-silent serialized PCM, Qwen duration-derived token ceiling, produced PCM slot-fit, and final media verification.

## Fresh ecosystem radar — 2026-08-28

- **LightX2V:** current observed upstream work still does not provide Hottop-measured benefit for the tested Wan2.2 I2V subset. Keep the tested Hottop pin; no freshness-only repin.
- **Qwen3-TTS:** no official upstream change observed in this cycle removes the operator-local 1.7B benchmark gate.
- **qwentts.cpp:** reviewed source remains `a8a7716b530e49fed537c57711247c12fbbb903c`. Upstream reports real end-to-end synthesis on a GTX 1070 Max-Q at roughly RTF 0.4 for its tested setup; treat that only as upstream runtime evidence, not Hottop runtime readiness or Mandarin-quality proof.
- **Qwen3-TTS serving:** recent H100/H200 work continues to reinforce benchmark-first admission; optimization toggles without repeatable end-to-end gain are not integration evidence.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or the current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. For real multi-shot narratives, keep physical-state continuity, affective trajectory and cinematic relations distinct from identity/motion when story semantics require them.
4. If an operator provisions Qwen3-TTS-ncnn locally, benchmark its 0.6B CustomVoice route on the same Mandarin production lines as eSpeak with bound ncnn/model/runtime/output provenance; upstream token parity is implementation evidence, not audio-quality proof.
5. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, **run the read-only `hottop-models probe-qwentts-cpp` preflight first**. Only after local bytes are bound may a separate explicit benchmark run the same Mandarin lines against eSpeak and the existing official Qwen adapter when available. Preserve exact build/backend/GGUF/WAV provenance, repeated speaker consistency, short-onset stability and latency/RTF.
6. When operator-local official Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback with bound runtime/hardware provenance and repeated cold/warm trials.
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
