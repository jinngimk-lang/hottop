# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified live-main evidence in this snapshot: **`main@234ec262004182984440cc5d029bbb509216b7b9` → CI #2010 passed** on Python 3.11/3.12. That commit is the squash merge of PR #171 after the qwentts.cpp GGUF preflight integrity closure.

PR #170 first synchronized the previously verified main/radar evidence. Its exact head `84859b386fa7dbddf2bfe4591edfdc3ce9d9d753` passed **CI #2006**, squash-merged as `f81accac7cc4943d5d7427050df1ededb19a237e`, and the post-merge **CI #2007** passed.

PR #171 then closed a real artifact-integrity gap in the existing qwentts.cpp read-only preflight. TDD evidence:

- RED `85815342152cb4c2102a2acde8f346fe158825e7` → **CI #2008** passed Ruff and failed pytest because arbitrary non-empty bytes renamed `.gguf` were still accepted as `ready=true`;
- GREEN `728fdff3a2396d36d036c16fd2267192b439c6f4` → **CI #2009** passed Ruff + full pytest on Python 3.11/3.12, with no review threads;
- squash merge `234ec262004182984440cc5d029bbb509216b7b9` → post-merge **CI #2010** passed on Python 3.11/3.12.

The read-only benchmark-input binder remains:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

It requires local non-empty files, requires the executable bit on the binary, requires the official `GGUF` magic on both talker/tokenizer model files, and records resolved path + byte size + SHA-256. It never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime status, or claims Mandarin/audio quality. `ready=true` means only that the supplied local benchmark inputs are structurally GGUF-like and byte-bound; it does not prove correct model identity, rights, runtime success or production quality.

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

`qwen3-tts-qwentts-cpp-1b7` remains a separate **1.7B benchmark candidate only**. Reviewed source `ServeurpersoCom/qwentts.cpp@a8a7716b530e49fed537c57711247c12fbbb903c` is MIT and exposes Qwen3-TTS 1.7B CustomVoice through local GGUF on CPU/CUDA/Metal/Vulkan. The #168 preflight removed manual byte-binding ambiguity; #171 additionally rejects non-GGUF talker/tokenizer bytes before reporting artifact readiness. Neither change makes this route integration-ready or runtime-ready.

Future qwentts.cpp execution still requires operator-provisioned source/build plus exact local talker/tokenizer GGUF bytes. After the read-only preflight passes, a real benchmark must bind build/backend, GGUF bytes, exact Mandarin line, preset speaker, seed/sampling/generation ceiling, produced WAV bytes, serialized-PCM integrity/duration, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Voice cloning remains separately rights-gated.

Speech execution remains fail-closed across independent layers: semantic dialogue input validation, non-empty/finite/non-silent serialized PCM, Qwen duration-derived token ceiling, produced PCM slot-fit, and final media verification.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V:** observed upstream `main` has advanced to `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6` (2026-08-28, `Update scripts (#1452)`). The inspected change only replaces private hard-coded paths with `/path/to/...` examples in a Wan-Animate-2 distillation shell script. It provides no Hottop-measured continuity, quality or runtime benefit for the tested Wan2.2 I2V subset. Keep the tested Hottop pin; **no freshness-only repin**.
- **Qwen3-TTS:** no official upstream change observed in this cycle removes the operator-local 1.7B benchmark gate.
- **qwentts.cpp:** exact GitHub `master` remains `a8a7716b530e49fed537c57711247c12fbbb903c`; no GitHub release was published in this check. Its documented local surface includes seedable sampling, `max_new_tokens`, 1.7B CustomVoice GGUF, CPU/CUDA/Metal/Vulkan and streaming/C ABI support. Those features improve benchmark practicality but do not alter Hottop admission: local exact bytes and real same-line Mandarin output evidence are still required.
- **GGUF validation:** upstream GGUF specification confirms `GGUF` as the format magic. Hottop uses only this shallow structural check plus exact byte binding; it intentionally does not treat the magic header as proof of correct Qwen model identity or quality.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or the current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. For real multi-shot narratives, keep physical-state continuity, affective trajectory and cinematic relations distinct from identity/motion when story semantics require them.
4. If an operator provisions Qwen3-TTS-ncnn locally, benchmark its 0.6B CustomVoice route on the same Mandarin production lines as eSpeak with bound ncnn/model/runtime/output provenance; upstream token parity is implementation evidence, not audio-quality proof.
5. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, **run the read-only `hottop-models probe-qwentts-cpp` preflight first**. Only after executable + GGUF magic + exact byte binding pass may a separate explicit benchmark run the same Mandarin lines against eSpeak and the existing official Qwen adapter when available. Preserve exact build/backend/GGUF/WAV provenance, repeated speaker consistency, short-onset stability and latency/RTF.
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
