# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified live-main evidence before this docs sync: **`main@3f7c8fc0e6b0120516c64614ee9f0c7bc388416d` → CI #2037 passed** on Python 3.11/3.12. PR #183 admitted WildActor as a gated identity-continuity research candidate and was squash-merged as `3f7c8fc0e6b0120516c64614ee9f0c7bc388416d`; the post-merge CI #2037 passed.

WildActor is relevant because it targets multi-reference identity preservation under changing viewpoint/composition/motion on a Wan2.2-5B-compatible path, but the reviewed release does **not** clear Hottop production admission. The exact source release does not expose a clear repository license at the reviewed revision, Actor-18M remains a construction pipeline/schema rather than a rights-cleared Hottop benchmark asset, and the public stack includes external model/download and optional hosted-API surfaces. Hottop therefore keeps it research-only: no copied code, no model/data download, no hosted Gemini use, no executable `video-run` route, no GPU provisioning and no runtime-ready claim. Future re-admission requires separately verified source/checkpoint/data/reference/output rights, operator-provisioned runtime, and same-sequence output-side identity + requested-action motion + geography + anti-copy + provenance/final-media evidence.

PR #179 previously closed the qwentts GGUF-structure preflight gap: RED exact head `07b16d5210ceeb11213e11305923b3398f3fd5d7` → CI #2027 passed Ruff and failed pytest because a `GGUF`-prefixed truncated file was still accepted; GREEN exact head `a8467f4e069f9e79954e9465fbb8d683346ed6ba` → CI #2030 passed on Python 3.11/3.12; PR #179 was squash-merged as `caeea70d39f7998f47825196d1b02fbedc888932`, and post-merge CI #2031 passed.

The qwentts preflight keeps bounded-memory exact hashing while retaining the first 24 bytes required for the fixed GGUF header surface. It rejects magic-only/truncated model bytes before any benchmark execution. The gate intentionally remains shallow and version-tolerant: it does not parse metadata, prove checkpoint identity, settle rights or claim Mandarin quality.

PR #177 previously closed a practical operator-artifact preflight memory gap. RED exact head `520999224f79aa137df2c6ac1a150f0c455d8d7d` → CI #2021 passed Ruff and failed pytest because the qwentts binder still used whole-file `Path.read_bytes()`. GREEN exact head `8a31e800b3207d4576b3eb98a887e97843621772` → CI #2023 passed on Python 3.11/3.12; the binder now computes exact SHA-256 with bounded 1 MiB streaming reads. Post-merge `main@7b4022ea…` → CI #2024 also passed. This prevents multi-GB operator-provisioned GGUF preflight from materializing an entire model in memory while preserving exact-byte provenance.

PR #174 corrected the durable interpretation of MLX-Audio issue #892 after inspecting merged upstream PR #895. The reported `Qwen3-TTS-12Hz-1.7B-Base-bf16 --voice Chelsie` path was not valid preset-speaker conditioning: Base checkpoints expose no preset-speaker table, MLX-Audio silently ignored the unsupported `--voice`, and synthesis proceeded unconditioned. Upstream fixed the runtime by rejecting unsupported voice conditioning on Base checkpoints and correcting examples to use real CustomVoice preset speakers.

Canonical doctrine therefore keeps **two independent TTS gates**:

1. capability binding before execution — requested preset speaker/voice/instruction/reference conditioning must be supported by the exact runtime/checkpoint; unsupported conditioning fails closed rather than silently degrading to unconditioned speech;
2. output evidence after execution — repeated trials still verify speaker consistency, onset stability, intelligibility, naturalness, PCM integrity/duration and exact WAV provenance.

This correction is runtime/checkpoint-specific evidence. It does **not** establish a defect in official Qwen CustomVoice, qwentts.cpp, Qwen3-TTS-ncnn or the Qwen model family.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest retained deterministic smoke evidence remains:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey delivery: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` derived from the exact ordered subject-bearing plan semantics; generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

`qwen3-tts-ncnn-0b6` and `qwen3-tts-qwentts-cpp-1b7` remain **benchmark candidates only** with `integration_ready=false / runtime_status=unprobed`.

The qwentts.cpp read-only input binder remains:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

It requires local non-empty files and executable binary permission, records resolved path + byte size + exact SHA-256 using bounded 1 MiB streaming reads, and requires a complete 24-byte fixed GGUF header surface on both model files rather than only the four-byte magic. It never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime status or claims Mandarin quality. `ready=true` means only that supplied benchmark inputs are shallowly GGUF-like and byte-bound; it does not prove exact checkpoint identity, licensing, runtime success or audio quality.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, exact model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V:** no Hottop-measured continuity, quality or runtime gain was found for the tested Wan2.2 I2V subset in this cycle. Keep the tested pin and **do not freshness-only repin**.
- **WildActor:** reviewed and merged as a **research-only** multi-reference identity candidate. Its Wan2.2-compatible mechanism is directly relevant, but unclear source licensing and separate model/data/reference/API/runtime rights block executable admission. Re-admission requires exact rights plus operator-provisioned runtime and complete output-side identity + requested-action motion evidence.
- **MiniMax-H3 community signal:** a public RTX 4090 multi-reference four-scene experiment reports four successful generations with reused environment/character references, but public media/evidence are insufficient to substitute for Hottop's own byte-bound continuity benchmark. Treat it as a radar signal only, not a production-quality claim or default-route change.
- **Qwen3-TTS 1.7B serving:** current public work continues to show that serving throughput/acceleration claims are runtime-specific and require fixed-protocol evidence; no new evidence removes Hottop's operator-local A/B gate. Existing onset-instability and missing-EOS/codec-repetition reports continue to justify repeated speaker/onset checks plus bounded generation and final PCM-duration validation.
- **Qwen3-TTS official / qwentts.cpp:** no reviewed upstream change in this cycle justifies changing current admission, adding a serving stack or downloading models automatically.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or the current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first; only after bounded-memory structural-header + exact-byte preflight passes may a separate explicit same-line Mandarin A/B execute.
4. For the qwentts.cpp CustomVoice A/B, use only checkpoint-supported preset speaker conditioning; do not use Base-only latent/reference registration on a CustomVoice checkpoint, and avoid registered names that could collide with built-in speakers.
5. Before any neural-TTS benchmark execution, fail closed if the requested speaker/voice/instruction/reference-conditioning mode is unsupported by the exact checkpoint/runtime. Never silently drop conditioning.
6. In real Qwen 1.7B A/B, preserve repeated speaker consistency, short-onset stability, intelligibility/naturalness, latency/RTF, PCM duration/integrity and exact runtime/model/output provenance as separate evidence dimensions.
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
