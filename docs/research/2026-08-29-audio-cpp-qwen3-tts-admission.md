# audio.cpp Qwen3-TTS 1.7B admission — 2026-08-29

## Decision

Admit `0xShug0/audio.cpp` only as an **operator-provisioned cross-runtime benchmark candidate** for Qwen3-TTS 1.7B CustomVoice. Do not add it to normal `video-run`, do not auto-build it, and do not download or convert model assets automatically.

Reviewed source: `a76ec04f620da829e4a53032247369083ba1ad45`.

## Why it is relevant

The current Production v0.2 audio gap is not another abstraction; it is real same-line Mandarin evidence from an operator-owned 1.7B runtime. audio.cpp is a native C++/ggml runtime with CPU, CUDA, HIP/ROCm, Vulkan and Metal backends. At the reviewed revision its Qwen3 documentation explicitly separates checkpoint capabilities:

- Base: reference-WAV voice cloning;
- VoiceDesign: instruction-conditioned voice design;
- CustomVoice: packaged speaker id via `--speaker`, with optional `--instruct` style control.

That capability split aligns with Hottop's fail-closed conditioning doctrine and gives a useful independent runtime for distinguishing model-level behavior from qwentts.cpp/CrispASR-specific behavior.

## Rights and cost boundary

- Source repository license: Apache-2.0 at the reviewed revision.
- Qwen model/tokenizer/checkpoint bytes remain independently reviewed operator inputs; source license does not authorize arbitrary weights or derived GGUF packages.
- Reference audio is outside the initial CustomVoice benchmark scope and remains rights-gated.
- Output-publication rights remain separately reviewed.
- No paid service is required by the candidate itself, but hardware/electricity are operator-owned costs.

## Runtime/download boundary

The reviewed project supports native model directories and audio.cpp-native GGUF conversion/loading. Hottop must not invoke model download, conversion, dependency fetch, build, container pull or hardware provisioning automatically.

The read-only command

`hottop-models probe-audio-cpp --executable <audiocpp_cli> --model-dir <Qwen3-TTS-12Hz-1.7B-CustomVoice>`

binds an **already provisioned** local benchmark input set without running audio.cpp. The model directory is resolved once and must contain the reviewed CustomVoice layout used by audio.cpp: `model.gguf` plus `speech_tokenizer/model.gguf`. The command reuses Hottop's hardened local artifact boundary: concrete resolved targets, bounded-memory SHA-256, stable before/after filesystem snapshots, executable permission, complete GGUF v3 fixed headers, non-zero tensor counts and incompatible-role path/byte distinctness.

The preflight never executes audio.cpp, accesses the network, invokes audio.cpp model-download/conversion helpers, builds dependencies, provisions accelerators or promotes the model-hub entry to runtime-ready. `ready=true` means only that the operator supplied a stable, byte-bound, structurally GGUF-like local input set. It does **not** prove checkpoint identity, licensing, speaker capability, runtime success, Mandarin quality or publication rights.

## Benchmark gate

A future run must compare the same Mandarin line and a checkpoint-supported preset speaker against the existing qwentts.cpp/CrispASR and, where available, official Qwen adapter path. Bind exact source/build/backend, model/tokenizer bytes, speaker, instruction, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's SHA-256/size/duration/PCM integrity, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility and naturalness.

Runtime success, upstream speed claims or one acceptable WAV are not quality proof.

## Integration in this workstream

`integrations/audio-cpp-qwen3-tts-benchmark.yml` persists the narrow candidate contract without changing production routing. It remains intentionally `integration_ready=false / runtime_status=unprobed`, forbids normal `video-run`, auto-download and auto-build, and records the same-line cross-runtime benchmark protocol.

The local preflight is a benchmark-input readiness tool only. It narrows the gap between discovery and a future explicit operator A/B while preserving the project's zero-cost/no-auto-provision boundary.