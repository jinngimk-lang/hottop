# Qwen3-TTS Pure C admission — 2026-08-30

## Decision

Admit `gabriele-mastrapasqua/qwen3-tts` as an **operator-provisioned local benchmark candidate**, not as a production runtime and not as an unattended download/build path.

Reviewed source: `f1b6865713d12a2a2365282fc02e19a5a384a565`.

## Why it matters

The project is a pure C inference engine for Qwen3-TTS and explicitly supports both 0.6B and 1.7B models, including `Qwen3-TTS-12Hz-1.7B-CustomVoice`, Chinese, preset speakers, reproducible seeds, sampling controls, `--max-tokens` and `--max-duration`. It reads raw safetensors with memory mapping instead of requiring a Python/PyTorch runtime or a GGUF conversion step. That makes it a materially different local-runtime benchmark candidate for Hottop's 1.7B Mandarin gap.

Upstream performance claims are hardware/runtime-specific and are **not** Hottop Mandarin quality evidence. Upstream samples in the reviewed README are mostly 0.6B and do not replace Hottop's same-line Mandarin benchmark.

## Rights and supply-chain boundary

- root source license: **MIT**;
- model family: official Qwen3-TTS assets; exact model/checkpoint rights must be re-bound when an operator provisions local bytes;
- vendored/third-party components keep their own notices/licenses and must be reviewed with the actual build used;
- voice cloning/reference audio remains separately rights-gated and is not required for this CustomVoice benchmark.

A permissive runtime license does not by itself grant rights to every model, voice asset, reference recording or generated output.

## Download/build behavior

The reviewed repository ships `download_model.sh`, which explicitly fetches Qwen model files from Hugging Face, including the 1.7B CustomVoice model. It also documents `download_voices.sh` for optional voice assets. Normal Hottop execution must **never** invoke these helpers or silently build/provision the runtime.

Admission is therefore fail-closed:

1. operator manually provisions the exact source/build and model directory;
2. Hottop records actual runtime source/build identity and model/checkpoint bytes/revision;
3. no model download, build dependency fetch, GPU provisioning, hosted API or paid fallback occurs from normal `video-run`;
4. execution is allowed only as an explicit operator benchmark after local preflight exists or equivalent evidence is supplied.

## Benchmark protocol

Compare this runtime with qwentts.cpp, CrispASR and audio.cpp using the **same-line Mandarin** text, the same checkpoint-supported preset speaker and semantically comparable controls. Bind:

- exact runtime revision/build;
- exact model/checkpoint revision and local artifact bytes;
- hardware/backend and execution shape;
- seed, sampling controls and generation ceiling;
- cold/warm latency and RTF;
- distinct WAV artifact bytes and PCM integrity;
- repeated speaker consistency;
- short-onset stability;
- Mandarin intelligibility and naturalness;
- publication/output-rights posture.

**Runtime support is not Mandarin quality proof.** A successful build or generated WAV cannot replace output-side listening and artifact evidence.

## Re-admission trigger

Promote beyond `benchmark_candidate` only after an operator-provisioned exact runtime/model passes the same Hottop benchmark method as the existing 1.7B local candidates and shows a measurable quality, reliability or resource advantage with a clear rollback path.
