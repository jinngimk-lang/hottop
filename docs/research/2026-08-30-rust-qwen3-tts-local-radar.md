# Rust Qwen3-TTS local runtime radar — 2026-08-30

## Why this matters

Production v0.2 still needs a real operator-owned Qwen3-TTS 1.7B Mandarin A/B. Hottop already has reviewed benchmark preparation for qwentts.cpp, CrispASR and audio.cpp, so a new local runtime should only be added when it materially lowers hardware/runtime friction **without weakening provenance, conditioning or no-auto-download guarantees**.

This pass reviewed two Rust implementations surfaced by the Qwen3-TTS ecosystem. Neither clears Hottop's admission gate today.

## Candidate A — `cgisky1980/Qwen3-TTS-Rust`

Reviewed source revision: `f86f59ed8b46ec0da4e77916f741d4589011be9e`.

Useful signals:

- Rust + llama.cpp/ONNX design;
- CPU/CUDA/Vulkan-oriented local execution claims;
- deterministic seed/sampling controls and generation-length control;
- public benchmark table reports roughly 0.55–0.64 RTF on RTX 2080 Ti for tested GGUF modes, with about 0.7–1.5 GB reported VRAM;
- supports speaker files, instructions and reference-audio voice creation.

Admission blockers:

1. the reviewed repository root does **not** contain a `LICENSE` file; `Cargo.toml` declares `MIT OR Apache-2.0`, but Hottop does not treat package metadata alone as equivalent to an auditable repository license grant;
2. upstream explicitly advertises automatic runtime management that downloads/configures llama.cpp and ONNX Runtime;
3. upstream documents a **silent speaker fallback**: when a requested speaker is missing, it falls back to `vivian` instead of failing closed. That conflicts directly with Hottop's canonical conditioning-integrity rule;
4. the normal first-run layout is designed to populate runtime/model assets automatically, which is incompatible with unattended `ZERO_COST_MODE=true` no-auto-download policy;
5. upstream runtime/performance claims are not Hottop Mandarin naturalness, onset or repeated-speaker evidence.

Decision: **research-only / not admitted to the model hub**. Revisit only if source licensing is made auditable and a manual/operator-provisioned mode can disable both network/runtime acquisition and silent speaker fallback.

## Candidate B — `second-state/qwen3_tts_rs`

Reviewed source revision: `efe3285ece133c452fe888d6eb52801761d0c501`.

Useful signals:

- Rust CLI/API implementation with libtorch and Apple-MLX backends;
- explicit 1.7B CustomVoice support including instruction conditioning;
- public Apple M4 measurements include Chinese 1.7B CustomVoice runs;
- CLI surface separates CustomVoice preset-speaker generation from Base/reference cloning.

Admission blockers:

1. the README license badge points to a root `LICENSE`, but that file is absent in the reviewed exact tree; `Cargo.toml` declares `Apache-2.0`, which is useful provenance but still leaves the repository-license surface incomplete;
2. the recommended quick installer explicitly installs binaries, models and reference audio automatically;
3. documented setup requires separate libtorch/PyTorch plus explicit Hugging Face model downloads and tokenizer generation;
4. published Apple M4 1.7B CustomVoice measurements are roughly 2.9–3.4 RTF, so this exact route does not presently demonstrate a clear runtime advantage over Hottop's already reviewed local candidates;
5. no Hottop same-line Mandarin artifact has been produced, and runtime claims do not prove speaker consistency, onset stability, intelligibility or naturalness.

Decision: **research-only / not admitted to the model hub**. Revisit only if the repository license surface is fixed and an operator-provisioned/manual-install path provides measurable value against qwentts.cpp, CrispASR or audio.cpp under the same Hottop benchmark protocol.

## Durable conclusion

Do not add a local TTS runtime merely because it is written in Rust, reports low latency, or supports Qwen3-TTS. Admission still requires:

- auditable source license plus separate model/tokenizer/reference/output rights;
- operator-provisioned local assets with no implicit model/runtime download;
- fail-closed conditioning (unsupported/missing speaker or reference must never silently degrade to another voice);
- exact source/build/model provenance;
- same-line Mandarin output evidence using Hottop's existing benchmark surface;
- repeated speaker consistency, short-onset stability, intelligibility/naturalness, PCM integrity, latency/RTF and output-byte binding.

The existing qwentts.cpp / CrispASR / audio.cpp preparation remains the stronger current path. No production route, dependency or pin changes are justified by this radar pass.