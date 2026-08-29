# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production evidence point before this workstream: **`main@44f60bff11e1e05b733a3629fb6d8733053bd07a`**. Push CI **#2188** passed on Python 3.11/3.12. At recovery there were no open PRs.

Current active workstream: **LongCat-Video-Avatar 1.5 gated admission**. Durable review: `docs/research/2026-08-30-longcat-video-avatar-15-admission.md`. Exact PR/head/CI state must be re-fetched live before merge decisions.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover **all subject-bearing shots** and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor and other reviewed routes remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

### LongCat-Video-Avatar 1.5

Reviewed source: `meituan-longcat/LongCat-Video@6b3f4b8582a8bc3f20f795735f5383716c4ba794`.

- source repository license: MIT;
- official `meituan-longcat/LongCat-Video-Avatar-1.5` model-card license: MIT;
- relevant upstream capabilities: audio-image-to-video, audio-text-to-video, continuation, single/multi-audio, Whisper-Large-v3 conditioning, distilled 8-step inference, 480p/720p, stylized/animal domains and long-video stability;
- upstream setup requires Python/CUDA/PyTorch/FlashAttention plus explicit model downloads, and Avatar 1.5 examples use a two-process `torchrun` path;
- admission: **gated research/benchmark candidate only**. No executable Hottop route, no auto-install/download and no GPU provisioning.

Future benchmark requires operator-provisioned exact source/model bytes and the same rights-safe subject sequence as the primary route, with identity, requested-action motion, lip-sync/dialogue timing when relevant, continuation/geography stability, anti-copy, provenance and final-media evidence measured independently.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Current local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available; reviewed manual v0.7.0 runtime archives remain operator-provisioned only;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Shared evidence surface:

`hottop-models inspect-tts-benchmark --spec <benchmark.json>`

It inspects already-produced local WAVs only and never executes TTS, accesses the network, installs dependencies, downloads models, provisions GPU resources or calls a paid service. It binds exact text/language/speaker, runtime revision/trial identity, WAV bytes/stream metadata, non-silence, measured latency, standard realtime factor `latency / audio_duration`, explicit inverse speedup and `listening_required=true`.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker and bounded generation settings while preserving exact runtime/model bytes, cold/warm timing, WAV/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed before execution; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **LightX2V/Wan2.2:** keep the existing tested pin unless a newer revision produces Hottop-measured continuity/quality/runtime improvement; no freshness-only repin.
- **Stand-In:** reviewed V2 evidence remains announcement-only. Durable review: `docs/research/2026-08-30-stand-in-v2-radar.md`.
- **WanGP/Wan2GP:** reviewed PiD changes remain post-processing/upsampler maintenance, not improved Hottop identity/requested-action evidence. Durable review: `docs/research/2026-08-30-wangp-pid-radar.md`.
- **Echo-Memory:** scene/revisit-memory benchmark signal only; it cannot substitute for subject identity or requested-action motion proof. Durable review: `docs/research/2026-08-30-echo-memory-admission.md`.
- **LongCat-Video-Avatar 1.5:** MIT source + official weights and unusually relevant audio-I2V/continuation/animal-domain capability make it worth retaining as a gated benchmark candidate. The heavy local stack and explicit model-download path keep it out of unattended production. Durable review: `docs/research/2026-08-30-longcat-video-avatar-15-admission.md`.
- **Qwen3-TTS / local 1.7B runtimes:** retain the operator-provisioned, benchmark-first route. Do not infer quality from runtime support, speed claims or a single successful WAV.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route or current tested LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Finish the active LongCat admission PR only after exact-head CI/review evidence passes; then re-fetch `main` and post-merge CI and clear this workstream from `STATUS.md`.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
4. If LongCat-Video-Avatar 1.5 is ever locally provisioned, benchmark it against the same rights-safe sequence rather than adding an adapter from upstream claims alone.
5. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; after same-line local WAV generation, use `inspect-tts-benchmark` and keep listening/speaker/onset evidence independent from speed.
6. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
7. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
