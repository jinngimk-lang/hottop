# CosyVoice3 runtime correctness radar — 2026-08-27

## Why this matters

Hottop keeps CosyVoice3 as an operator-owned local Mandarin TTS benchmark candidate, not as the guaranteed fallback. The current production baseline remains the eSpeak family, while Qwen3-TTS 1.7B CustomVoice remains the admitted delivery-controlled neural benchmark candidate.

This note records fresh correctness evidence that narrows the safe CosyVoice3 admission surface. It does **not** enable a new runtime, download weights, add a dependency, or change normal `video-run` routing.

## Source identity

- Repository: `QwenAudio/CosyVoice`
- Code license reported by GitHub: Apache-2.0
- Exact inspected `main`: `074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc`
- Repository push date for that head: 2026-05-25
- Review date: 2026-08-27

Code license is not a substitute for model/checkpoint/data/reference-audio rights. Any future Hottop benchmark must bind the exact local checkpoint/model revision separately and keep voice cloning/reference audio rights-gated.

## Fresh correctness findings

### 1. TensorRT + FP16 can produce non-finite audio

Upstream issue `QwenAudio/CosyVoice#1930`, opened 2026-08-08, reports a controlled reproduction on the official `Fun-CosyVoice3-0.5B-2512` checkpoint where `load_trt=True` plus `fp16=True` produced non-finite/NaN audio in **64/64** generations on an NVIDIA L40S. The same report states FP32 TensorRT and eager controls passed on the same corpus and inputs.

The thread contains conflicting community claims about whether a particular TensorRT package pin resolves the issue. Hottop has not independently reproduced either claim. Therefore no such pin is treated as a verified fix.

**Admission consequence:** Hottop must not admit CosyVoice3 TensorRT FP16 as a production/default route from documentation or popularity alone. A future operator-local runtime must fail closed on non-finite output and require same-runtime benchmark evidence before promotion.

### 2. Streaming serving has a device-mismatch correctness failure

`vllm-project/vllm-omni#6455`, opened 2026-08-21, reports CosyVoice3 streaming TTS failing at runtime because STFT input/window tensors land on different devices. The reproduction uses a local vLLM-Omni server and a normal streaming TTS request.

This is a serving-path correctness issue rather than a model-quality comparison. It means a future Hottop CosyVoice3 streaming route cannot infer readiness merely because the model loads or the server starts.

**Admission consequence:** streaming must remain benchmark-gated and fail closed until the exact serving stack, device placement, generated waveform and complete Hottop dialogue/media path are verified together.

## Hottop closure in this cycle

The freshness review exposed a concrete bug in Hottop's existing local CosyVoice3 adapter. `_write_pcm16_wav()` previously bounded samples with Python `min/max`; for `NaN`, that expression resolves to `1.0`, silently converting a non-finite sample into full-scale positive PCM instead of rejecting the corrupt waveform.

This cycle therefore does two narrow things:

- registers `cosyvoice3-0b5-2512` in `integrations/model-hub.yml` only as `benchmark_candidate / integration_ready=false / runtime_status=unprobed`, with the TensorRT-FP16, streaming and finite-waveform gates encoded in the runtime boundary;
- hardens the existing local adapter so any non-finite sample raises `CosyVoice3Error` **before** an output WAV is created.

This is safety hardening, not provider promotion. It adds no CosyVoice dependency, runtime auto-install, checkpoint download, GPU provisioning or default route.

## Hottop policy

CosyVoice3 remains a **benchmark candidate**, not a guaranteed or unattended default.

Any future CosyVoice3 operator-local route must satisfy all of the following before promotion:

1. exact local source/runtime identity is recorded;
2. exact model/checkpoint provenance is independently verifiable;
3. no automatic multi-GB download occurs in normal Hottop execution;
4. output waveform is checked for finite samples before acceptance;
5. output is decodable, non-empty and has plausible duration;
6. the selected serving mode is tested end-to-end on the actual operator hardware;
7. TensorRT FP16 is disabled or independently demonstrated correct on the exact runtime before it can be admitted;
8. streaming is disabled or independently demonstrated correct on the exact runtime before it can be admitted;
9. role/delivery semantics survive render → plan → execution rather than becoming archival-only metadata;
10. same-line Mandarin A/B evidence demonstrates measurable value over the guaranteed fallback without weakening rights, provenance, media or cost gates.

Until those conditions are met, CosyVoice3 must not replace the eSpeak-family guaranteed fallback or the current Qwen3-TTS 1.7B delivery-controlled benchmark priority.

## Decision

A narrow safety integration is justified; a runtime promotion is not. Hottop now records the candidate and rejects non-finite samples, while keeping the actual CosyVoice3 runtime outside unattended/default production until operator-local benchmark evidence clears the remaining gates.

This follows the durable project rule: **benchmark evidence beats optimization flags, popularity and nominal server readiness**.
