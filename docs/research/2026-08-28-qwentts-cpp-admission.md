# qwentts.cpp 1.7B CustomVoice admission — 2026-08-28

## Decision

Admit `ServeurpersoCom/qwentts.cpp` only as an **operator-provisioned benchmark candidate** for Qwen3-TTS 1.7B CustomVoice. It is not an unattended Hottop backend, not an integration-ready route, and not evidence that neural TTS quality has improved.

The candidate is unusually relevant because it exposes Qwen3-TTS 1.7B through a local C++/GGML runtime with CPU, CUDA, Metal and Vulkan backends. That directly reduces the serving-stack barrier around Hottop's unresolved 1.7B Mandarin same-line A/B target. The admission remains benchmark-only until Hottop reproduces quality and artifact-integrity evidence on an operator-provisioned runtime.

## Exact reviewed upstream

- Repository: `https://github.com/ServeurpersoCom/qwentts.cpp`
- Reviewed source revision: `a8a7716b530e49fed537c57711247c12fbbb903c`
- Source license at reviewed revision: MIT
- Upstream capabilities observed at the reviewed revision:
  - Qwen3-TTS 0.6B and 1.7B
  - 1.7B CustomVoice, Base and VoiceDesign surfaces
  - preset speakers including `vivian` and `dylan`
  - CPU, CUDA, Metal and Vulkan execution backends
  - Q8_0 / Q4_K_M GGUF quantization paths
  - local CLI/server and a C ABI
  - 24 kHz mono WAV output

Source-code permission does not automatically settle model, tokenizer, converted-GGUF or output-publication rights. Upstream Qwen model/tokenizer assets are described as Apache-2.0, but exact GGUF checkpoint identity and rights must still be bound at benchmark time.

## Zero-cost and provisioning boundary

`qwentts.cpp` is compatible with **self-owned compute**, not with Hottop's unattended auto-provisioning path.

Normal Hottop execution must not:

- invoke upstream `checkpoints.sh` or any Hugging Face/model download helper;
- auto-download pre-converted GGUFs;
- auto-build or auto-fetch dependencies;
- pull Docker images on behalf of `video-run`;
- provision CPU/GPU/Vulkan resources;
- obtain credentials or enable paid inference.

An operator may separately provision an exact reviewed source checkout, build/runtime and local GGUF assets. Only then may Hottop benchmark the candidate.

## Why this is not a production route yet

The public implementation materially lowers the runtime barrier, but Hottop has not reproduced:

- Mandarin naturalness versus the guaranteed eSpeak-family fallback;
- 1.7B preset-speaker consistency across repeated identical lines;
- short-line onset stability in the first 1–2 seconds;
- instruction/delivery controllability comparable with the existing official Qwen adapter;
- duration compliance under codec repetition / missing-EOS failure modes;
- finite, non-silent serialized PCM across the actual local backend;
- runtime latency/RTF on the operator's real CPU/CUDA/Vulkan hardware.

Recent Qwen3-TTS ecosystem failures reinforce this caution: codec repetition and missing-EOS have appeared in third-party runtimes, so a successfully returned waveform is not enough. Existing Hottop semantic-input, token-ceiling, PCM finite/non-silent and final-duration gates remain mandatory for any future adapter.

## Future benchmark protocol

When the operator has provisioned local assets, compare the **same Mandarin production lines** across eSpeak-family, the existing official Qwen adapter when its 1.7B checkpoint is available, and qwentts.cpp.

Bind at minimum:

1. qwentts.cpp source revision;
2. compiler/build flags and backend (`cpu`, `cuda`, `metal` or `vulkan`);
3. GGML/GGUF runtime/library identity;
4. talker GGUF path, SHA-256 and byte size;
5. tokenizer/codec GGUF path, SHA-256 and byte size;
6. exact input text, language, preset speaker, seed/sampling parameters and generation ceiling;
7. produced WAV SHA-256, sample rate/channels, duration and serialized-PCM integrity;
8. latency and real-time factor;
9. repeated-run speaker consistency;
10. short-onset stability and whole-line intelligibility/naturalness;
11. output-publication rights posture.

Voice cloning remains separately rights-gated and is outside the initial benchmark. Start with preset CustomVoice only.

## Re-admission gate

Promote beyond `benchmark_candidate` only after all of the following are true:

- exact source/build and exact local GGUF bytes are operator-provisioned and reproducibly bound;
- checkpoint/model/tokenizer rights are explicitly reviewed;
- no hidden network/model-fetch behavior is required at runtime;
- same-line Mandarin A/B shows measurable quality or practicality value without weakening Hottop audio integrity gates;
- any executable adapter remains `shell=False` / argv-oriented and fail-closed;
- eSpeak remains the guaranteed local fallback.
