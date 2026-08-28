# Qwen3-TTS-ncnn admission — 2026-08-28

## Why this matters

Production v0.2 keeps eSpeak-family Mandarin as the guaranteed zero-cost local fallback and Qwen3-TTS 1.7B CustomVoice as the higher-quality operator-owned benchmark target. The current physical gap is that the 1.7B route still needs a provisioned neural runtime/GPU before Hottop can run a real same-line A/B.

`mingshi2333/Qwen3-TTS-ncnn` provides a materially different operator path: a pure C++/ncnn port of **Qwen3-TTS 12 Hz 0.6B** with CPU and Vulkan execution. Upstream reports free-running greedy token parity against PyTorch, including the built-in CustomVoice path. This does not prove Hottop audio quality, but it lowers the hardware barrier enough to justify a benchmark-candidate registry entry.

## Reviewed provenance

- source repository: https://github.com/mingshi2333/Qwen3-TTS-ncnn
- exact source revision: `7c58a6756367e38abe19b0fc2639e56aa1e8bf74`
- source license: Apache-2.0, verified from the exact tree root `LICENSE`
- target official checkpoint family: `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`
- official model-card license observed on 2026-08-28: Apache-2.0
- official 0.6B CustomVoice model surface observed at roughly 2.5 GB total, including a 1.81 GB main safetensors file plus the speech-tokenizer assets

Code license, model/checkpoint license, preset-timbre/output-publication rights and any reference-audio rights remain separate gates.

## Runtime and network boundary

This candidate is **not integration-ready**.

The upstream README documents behavior incompatible with normal unattended Hottop execution unless explicitly disabled/replaced:

- CMake can fetch/build `ncnn` automatically when a local `ncnn_DIR` is not supplied;
- conversion instructions explicitly download the official Qwen checkpoint and clone Qwen modeling source;
- local converted model assets must exist before the C++ CLI can run.

Hottop therefore must never invoke the upstream automatic fetch/download/conversion path in normal `video-run` or CI. Re-admission requires an operator-provisioned local ncnn build plus locally converted/bound Qwen 0.6B assets with exact provenance.

## Upstream evidence vs Hottop evidence

Upstream reports:

- C++17 CPU/Vulkan execution;
- greedy CustomVoice token parity versus PyTorch within the matched numeric domain;
- CPU/Vulkan runtime improvements relative to its PyTorch fp32 CPU baseline.

These are upstream claims, not Hottop production evidence. Token parity does not establish Mandarin naturalness, speaker quality, onset stability, dialogue-slot fit or final mixed-video quality.

A future Hottop benchmark must bind:

1. exact Qwen3-TTS-ncnn source revision;
2. exact ncnn source/build identity;
3. exact converted 0.6B model/tokenizer bytes and official checkpoint source revision;
4. CPU/Vulkan hardware/runtime identity;
5. exact dialogue input and configured speaker/delivery intent;
6. output WAV bytes plus existing non-empty/finite/non-silent PCM and duration-slot gates;
7. same-line comparison against the guaranteed eSpeak fallback and, when available, the reviewed 1.7B Qwen route.

## Admission result

**Status: benchmark candidate only.**

The candidate is useful because it may provide a lower-hardware, zero-paid local neural-TTS benchmark path. It does **not** replace:

- eSpeak-family as the guaranteed no-model fallback;
- Qwen3-TTS 1.7B as the current quality-target benchmark;
- existing neural-TTS artifact integrity gates.

No upstream code is vendored, no model is downloaded, no build is started, and no runtime readiness is claimed by this admission.
