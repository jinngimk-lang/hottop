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

The reviewed upstream head still remains `a8a7716b530e49fed537c57711247c12fbbb903c` in this owner cycle. Its commit message reports end-to-end synthesis on a GTX 1070 Max-Q at roughly RTF 0.4 while validating CUDA 12.8/12.9 build compatibility. Treat that only as upstream runtime evidence for that exact setup, not as Hottop Mandarin naturalness, speaker-consistency or runtime-readiness evidence.

## Exact-pin runtime correctness risks — 2026-08-29

Open upstream issues on the exact reviewed revision add important benchmark constraints without changing admission status:

- **Issue #29 — checkpoint capability confusion / speaker shadowing.** The server correctly rejects WAV reference registration on CustomVoice because reference/cloning conditioning belongs to Base, but pre-encoded `.spk/.rvq` registration can incorrectly return success on CustomVoice. Synthesis then fails because the CustomVoice model still requires a preset speaker. If the registered latent uses the name of a built-in speaker, it can shadow/break that built-in speaker until the registration is deleted or the process restarts. Hottop must therefore treat reference/cloning registration as a separate Base-only, rights-gated capability and must never use it as a substitute for a CustomVoice preset speaker.
- **Issue #31 — CPU server connection/OpenMP sensitivity.** Buffered synthesis can accumulate OpenMP teams across HTTP connections and collapse effective parallelism in reported CPU server runs; lower `--max-batch` mitigated the measured case. Any future Hottop benchmark must bind topology, server/CLI mode, connection strategy and concurrency rather than treating a model/backend label as sufficient latency provenance.
- **Issue #32 — reference-extraction path sensitivity.** WAV voice registration can perform reference extraction on the HTTP thread and degrade later CPU synthesis in the reported server setup, while pre-encoded latent registration avoids that specific extraction cost. This is performance-path evidence only; it does not override the capability restriction above or authorize CustomVoice latent registration.

These are runtime-specific open issues, not model-family claims. They strengthen Hottop's existing rules: checkpoint/runtime capability validation before synthesis, exact execution-shape provenance, and output-side evidence after generation. They do **not** justify a qwentts.cpp execution adapter while the runtime remains `unprobed`.

Upstream issues:

- https://github.com/ServeurpersoCom/qwentts.cpp/issues/29
- https://github.com/ServeurpersoCom/qwentts.cpp/issues/31
- https://github.com/ServeurpersoCom/qwentts.cpp/issues/32

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

## Read-only local benchmark preflight

Hottop now exposes a **read-only artifact-binding preflight** for an already provisioned qwentts.cpp benchmark setup:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

The preflight:

- requires the executable, talker GGUF and tokenizer GGUF to exist as local files;
- requires the executable to be executable and all three files to be non-empty;
- records the resolved local path, byte size and SHA-256 for every supplied artifact;
- returns `ready=false` with explicit blockers when the local inputs are incomplete;
- **never executes qwentts.cpp**, opens a network connection, downloads a model, builds dependencies, changes model-hub runtime status or claims audio quality.

`ready=true` means only that the supplied local benchmark inputs are structurally present and byte-bound. It does **not** mean the runtime has successfully synthesized audio, that the GGUFs have correct publication rights, or that Mandarin quality has passed Hottop's benchmark gates.

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
6. exact checkpoint capability mode (`Base`, `CustomVoice`, `VoiceDesign`) and requested conditioning mode;
7. exact input text, language, valid preset speaker or separately rights-cleared Base reference conditioning, seed/sampling parameters and generation ceiling;
8. server/CLI mode, connection strategy, batch/concurrency/topology and cold/warm trial state;
9. produced WAV SHA-256, sample rate/channels, duration and serialized-PCM integrity;
10. latency and real-time factor;
11. repeated-run speaker consistency;
12. short-onset stability and whole-line intelligibility/naturalness;
13. output-publication rights posture.

Voice cloning remains separately rights-gated and is outside the initial benchmark. Start with preset CustomVoice only. Do not register Base-only voice references/latents on a CustomVoice checkpoint, and do not create registered speaker names that can collide with built-in preset speakers.

## Re-admission gate

Promote beyond `benchmark_candidate` only after all of the following are true:

- exact source/build and exact local GGUF bytes are operator-provisioned and reproducibly bound;
- checkpoint/model/tokenizer rights are explicitly reviewed;
- no hidden network/model-fetch behavior is required at runtime;
- same-line Mandarin A/B shows measurable quality or practicality value without weakening Hottop audio integrity gates;
- checkpoint/runtime capability validation rejects unsupported conditioning before synthesis;
- any executable adapter remains `shell=False` / argv-oriented and fail-closed;
- eSpeak remains the guaranteed local fallback.