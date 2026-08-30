# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@eaffa96dcfcf8e0a5747bef309f9041400632eaf`**. PR #259 exact head `95fcb3222e26d501ead192662cc7f045e4dcc0b5` passed CI **#2237** and was squash-merged; post-merge push CI **#2238** passed on Python 3.11/3.12. The merged change is research-only and adds no executable provider, dependency, model download, GPU provisioning, credential or paid path.

No production workstream is currently known to be failing at this evidence point.

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

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor, LongCat-Video-Avatar, DiffSynth/MiniMax-H3 NF4 and other reviewed routes remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available; reviewed manual v0.7.0 runtime archives remain operator-provisioned only;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Shared evidence surface:

`hottop-models inspect-tts-benchmark --spec <benchmark.json>`

It inspects already-produced local WAVs only and never executes TTS, accesses the network, installs dependencies, downloads models, provisions GPU resources or calls a paid service. Latency must be finite and greater than zero. Separate benchmark rows cannot reuse the same resolved WAV path; identical bytes are still legal when independently produced as distinct artifact instances.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker and bounded generation settings while preserving exact runtime/model bytes, cold/warm timing, distinct WAV artifact instances, WAV/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed before execution; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **LightX2V/Wan2.2:** reviewed upstream remains `ModelTC/LightX2V@7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`; recent reviewed changes do not provide Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- **DiffSynth-Studio / MiniMax-H3 NF4:** framework `modelscope/DiffSynth-Studio@102fe9980b9375ecb6436d360297a00327472535` is Apache-2.0 and the NF4 route is an interesting lower-hardware H3 benchmark signal, but it remains research/operator-benchmark only. The official MiniMax-H3 Community License reviewed 2026-08-30 excludes the EU, UK, Republic of Korea and USA from its default Applicable Territory, requires separate prior written authorization for commercial products/services above USD 20M equivalent yearly revenue, carries distribution/NOTICE/UI-display/use restrictions, and prohibits using H3 Works or their outputs/results to improve another AI model outside the H3 derivative family. A derivative NF4 model-card `apache-2.0` field does not override the base-model license. Durable review: `docs/research/2026-08-30-diffsynth-minimax-h3-nf4-admission.md`.
- **MiniMax H3 Motion Lab:** `matlowai/ComfyUI-MAINodes@f4868b4a08e8a504ce86db54a17961d399ffa2bc` remains a GPL-3.0-or-later, operator-managed post-generation recovery experiment for bursty-motion smear; it is not a generator admission. Durable review: `docs/research/2026-08-30-minimax-h3-motion-lab-radar.md`.
- **LongCat-Video-Avatar 1.5:** benchmark-layer candidate only despite relevant audio-I2V/continuation/animal-domain capability; heavy local stack and explicit downloads keep it out of unattended production. Durable review: `docs/research/2026-08-30-longcat-video-avatar-15-admission.md`.
- **Step-Audio-EditX / Supertonic Mandarin:** remain research-only because main checkpoint/weights rights do not clear Hottop's commercial/operator admission gate. Durable reviews: `docs/research/2026-08-30-step-audio-editx-admission.md` and `docs/research/2026-08-30-mandarin-tts-license-radar.md`.
- **Qwen3-TTS / local 1.7B runtimes:** official source remains `QwenLM/Qwen3-TTS@022e286b98fbec7e1e916cb940cdf532cd9f488e`; retain operator-provisioned, benchmark-first evaluation. Do not infer quality from runtime support, throughput or a single successful WAV.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or the prepared 1.7B TTS benchmark candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. Treat DiffSynth/MiniMax-H3 NF4 only as an operator benchmark if exact base/derivative rights, operator geography/commercial context, local artifact bytes and offline runtime all clear first; do not call ModelScope/Hugging Face download paths from normal `video-run`.
4. If an operator-provisioned MiniMax-H3 clip fails requested-action motion specifically because of bursty-motion smear, benchmark the reviewed Motion Lab recovery path against exact baseline bytes; smoother output alone is not success.
5. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; after same-line local WAV generation, use `inspect-tts-benchmark` with one distinct resolved WAV artifact per trial and keep listening/speaker/onset evidence independent from speed.
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
