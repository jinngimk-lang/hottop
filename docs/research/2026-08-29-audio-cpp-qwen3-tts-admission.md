# audio.cpp Qwen3-TTS 1.7B admission — 2026-08-29

## Decision

Admit `0xShug0/audio.cpp` only as an **operator-provisioned cross-runtime benchmark candidate** for Qwen3-TTS 1.7B CustomVoice. Do not add it to normal `video-run`, do not auto-build it, and do not download or convert model assets automatically.

Reviewed source capability revision: `a76ec04f620da829e4a53032247369083ba1ad45`.

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

## Reviewed official prebuilt option

Upstream release `v0.7.0`, published 2026-08-27, is pinned separately from the source capability audit to commit `d2ff37009c69d464bcab6aa4a44a13746e84a914`. GitHub's release metadata provides exact SHA-256 digests for official runtime archives, including:

- `audio-v0.7.0-bin-ubuntu-x64-cpu.tar.gz` — `400774c3f92f3da4c5fedfa2e43d50482e951ec288eb39e66c10e63fb46de47d`, 39,878,502 bytes;
- `audio-v0.7.0-bin-ubuntu-x64-vulkan.tar.gz` — `e49676f1da28df0d2a6ca2073118964e91f3d14aa3c2ca3ad984e3d09b96932d`, 66,981,995 bytes.

The release workflow builds `audiocpp_cli`, `audiocpp_server` and `audiocpp_gguf` as deployment bundles and enables the native model manager. That reduces the operator's need to compile audio.cpp locally, but it creates an important boundary: **Hottop may record and verify a manually provisioned official prebuilt, but normal unattended Hottop must not download the archive or invoke the bundled model manager to fetch models.**

A release archive digest proves only the identity of the published runtime bundle. It does not prove that a locally extracted executable has the expected Qwen capability, that the operator supplied the correct CustomVoice model bytes, that the runtime executes successfully, or that Mandarin output quality is acceptable. The existing `probe-audio-cpp` remains the local byte-binding gate after extraction; actual Qwen capability and output quality remain execution/benchmark gates.

Upstream `main` has moved beyond the reviewed capability revision after v0.7.0, including release/documentation/runtime maintenance. Hottop does not freshness-only repin the source audit: future source revision changes require a concrete contract or benchmark reason.

## Exact upstream layout audit

The reviewed upstream model contract was re-checked against `model_specs/qwen3_tts.json` and `docs/models/qwen3.md` at the same exact source revision. This resolves an important preflight question without widening the gate:

- audio.cpp documents Qwen3 TTS conversion as converting the main `model.safetensors` and the separate `speech_tokenizer/model.safetensors` **independently**, placing each converted output beside its source as `model.gguf`;
- the package spec maps `model_weights` and `speech_tokenizer_weights` as distinct tensor roles and the native directory loader expects the corresponding model/speech-tokenizer resources;
- GGUF conversion can embed JSON/tokenizer/config sidecars recursively, so there is no reviewed evidence that Hottop should invent a third mandatory local artifact for this preflight;
- older tensor-only GGUFs may require sidecars, but the shallow Hottop probe intentionally does not claim runtime loadability or checkpoint identity. Those remain execution-time/operator-evidence gates.

Therefore the existing `model.gguf` + `speech_tokenizer/model.gguf` local layout is retained. The audit is evidence for the current probe shape, not a claim that any two GGUF-like files are a valid Qwen3 CustomVoice checkpoint.

## Benchmark gate

A future run must compare the same Mandarin line and a checkpoint-supported preset speaker against the existing qwentts.cpp/CrispASR and, where available, official Qwen adapter path. Bind exact source/build/backend or reviewed prebuilt digest, model/tokenizer bytes, speaker, instruction, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's SHA-256/size/duration/PCM integrity, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility and naturalness.

Runtime success, upstream speed claims or one acceptable WAV are not quality proof.

## Integration in this workstream

`integrations/audio-cpp-qwen3-tts-benchmark.yml` persists the narrow candidate contract without changing production routing. It remains intentionally `integration_ready=false / runtime_status=unprobed`, forbids normal `video-run`, auto-download and auto-build, records the same-line cross-runtime benchmark protocol, and now preserves the exact reviewed v0.7.0 Linux prebuilt provenance as a manual operator option.

The local preflight is a benchmark-input readiness tool only. It narrows the gap between discovery and a future explicit operator A/B while preserving the project's zero-cost/no-auto-provision boundary.