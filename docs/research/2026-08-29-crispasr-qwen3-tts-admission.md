# CrispASR Qwen3-TTS 1.7B admission — 2026-08-29

## Decision

Admit `CrispStrobe/CrispASR` only as an **operator-provisioned benchmark candidate** for Qwen3-TTS 1.7B CustomVoice. Do not add an executable production route yet.

This candidate is useful because it provides a second local C++/ggml runtime for the same 1.7B CustomVoice target already tracked through qwentts.cpp, including CPU and Vulkan execution. A same-line Mandarin A/B across two independent runtimes can help distinguish model-quality limitations from runtime-specific correctness or performance defects.

## Exact reviewed source and licenses

- Source: `CrispStrobe/CrispASR@bb77301c4dbde1fca217e1a19584b1ae0167ee03`.
- Source license: MIT.
- Reviewed converted talker: `cstr/qwen3-tts-1.7b-customvoice-GGUF`; model card declares Apache-2.0 and states it is a format conversion/quantisation of `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`.
- Reviewed codec/tokenizer: `cstr/qwen3-tts-tokenizer-12hz-GGUF`; model card declares Apache-2.0 and states it is a conversion of `Qwen/Qwen3-TTS-Tokenizer-12Hz`.
- Output/publication rights remain an operator review gate; repository/model-card license metadata does not replace that review.

The source head was rechecked on 2026-08-29 and remained `bb77301c4dbde1fca217e1a19584b1ae0167ee03`. The latest reviewed change adds a padding-silence option for a VLC/C2PA playback issue and does not change this admission.

## Why it is materially relevant

CrispASR exposes `qwen3-tts-1.7b-customvoice` with preset speakers and a separately supplied tokenizer/codec GGUF. Its current documentation lists a Q8_0 1.7B talker around 2.04 GB plus a tokenizer/codec GGUF, and keeps the codec at F16 as the higher-fidelity pairing.

A public upstream performance report (`CrispStrobe/CrispASR#183`) measured the 1.7B CustomVoice Q8_0 path on an AMD Radeon R9700 / Vulkan runtime. The report recorded roughly 0.72 RTF before a native-GQA change and roughly 0.5–0.76 RTF after it over 100–600 words, while explicitly limiting the quality claim to a listening check on that runtime. Hottop treats this as **runtime-specific benchmark evidence**, not as a general quality claim.

## Admission boundaries

Normal Hottop execution MUST NOT use CrispASR auto-provisioning:

- `-m auto` downloads model files on first use and is forbidden in unattended Hottop paths;
- Hottop must not clone/build CrispASR, pull releases/containers, download GGUF assets, or provision GPU drivers automatically;
- runtime/model/tokenizer artifacts must be operator-provisioned locally and byte-bound before any benchmark;
- preset CustomVoice is the initial benchmark scope; arbitrary voice cloning/reference audio remains separately rights-gated;
- `benchmark_candidate` does not mean `integration_ready` or `runtime_ready`.

## Read-only local artifact preflight

Hottop now exposes a non-executing local input check for an operator-provisioned CrispASR benchmark:

```text
hottop-models probe-crispasr \
  --executable /local/path/crispasr \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

The preflight deliberately reuses Hottop's already-hardened local artifact identity checks rather than introducing a weaker CrispASR-specific parser. It therefore preserves the current resolved-target, bounded-memory streaming SHA-256, before/after filesystem snapshot, executable-permission, complete 24-byte GGUF fixed-header, reviewed GGUF version `3`, and non-zero-tensor gates. Talker and tokenizer/codec must be distinct by both resolved path and exact bytes; the executable must also remain distinct from model artifacts.

`ready=true` means only that the operator supplied a stable, shallowly GGUF-structured, exact-byte-bound and role-distinct local benchmark input set. It does **not** prove semantic checkpoint identity, license/publication rights, supported speaker capability, CrispASR runtime compatibility, synthesis success, latency, speaker consistency, or Mandarin quality.

The command never executes CrispASR, opens a network connection, invokes `-m auto`, downloads/builds anything, provisions hardware, or promotes model-hub runtime state.

TDD evidence for this surface:

- RED exact head `166f094a46c24acb8f37f0ca7d01685fb715afc3` → CI #2111: Ruff passed and pytest reported exactly `2 failed / 554 passed`; both failures were the missing `probe-crispasr` command.
- GREEN implementation head `0dcd45627bfd88d68f2b688d5f3cf741271d36f2` → CI #2115: Python 3.11/3.12 both passed Ruff and full pytest.

## Future same-line benchmark gate

Only after an operator provides a reviewed local build and exact 1.7B talker + tokenizer GGUF should Hottop run a benchmark. Bind at minimum:

1. CrispASR exact source/build identity and backend (CPU/Vulkan/CUDA if applicable);
2. talker and tokenizer resolved paths, SHA-256 and byte sizes;
3. exact Mandarin line, preset speaker, seed/sampling/generation ceiling and cold/warm trial shape;
4. WAV bytes, sample rate, duration, serialized-PCM finite/non-silent integrity and planned-slot duration gate;
5. latency/RTF, repeated speaker consistency, short-onset stability, intelligibility and naturalness;
6. the same line/protocol through qwentts.cpp and, when provisioned, the reviewed official Qwen adapter.

A faster RTF does not prove better Mandarin quality. A successful process exit does not prove speaker conditioning, valid audio, or production readiness.
