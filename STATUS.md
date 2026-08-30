# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest fully verified `main` evidence point remains **`main@a7c295afd1c3fd481b051ee6fcc21fa54fe0c25e` / CI #2253**. PR #266 subsequently merged the already-GREEN runtime-revision status sync to `main@293289878291aa61ff2c6f14cc63e5710d7fdf92`; no separate post-merge run was visible when this workstream began.

Three TTS benchmark-integrity gaps are now closed on the active PR #267 branch:

- per-candidate cold/warm completeness: RED `CI #2241` → GREEN `CI #2243/#2244` → merged main/post-merge `CI #2246`;
- per-candidate runtime-revision consistency: RED `CI #2249` → GREEN `CI #2250/#2251` → merged main/post-merge `CI #2253`;
- per-candidate model/checkpoint-revision consistency: RED **`CI #2256`** → GREEN **`CI #2261`** on Python 3.11/3.12. The benchmark now persists `model_revision` per trial and rejects one candidate label spanning multiple model revisions.

The changes add no neural runtime execution, provider route, dependency, model download, GPU provisioning, credential or paid path.

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

**Benchmark completeness is fail-closed per candidate:** every represented runtime must have at least one `cold` and at least one `warm` trial before the evidence can be `ready=true`. Additional independent warm trials remain valid and are preferred for warmed-runtime variance and repeated speaker-consistency evidence.

**Benchmark implementation identity is fail-closed per candidate:** all cold/warm/repeated trials grouped under one candidate label must bind the same exact `runtime_revision` **and** the same exact `model_revision`. Comparing two binaries/builds or two model/checkpoint revisions requires distinct candidate identities instead of silently mixing evidence under one label.

Cold/warm coverage plus runtime/model-revision consistency are evidence-coherence gates; none replaces listening, onset, speaker, intelligibility or artifact-integrity gates.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker and bounded generation settings while preserving exact runtime/model bytes, one exact runtime revision and one exact model revision per candidate, cold/warm timing, distinct WAV artifact instances, WAV/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed before execution; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **Qwen3-TTS benchmark practice:** SGLang-Omni issue #1464 requires exact source revision, model revision, dataset, hardware, request count and concurrency for performance claims. Its Aug. 23 Qwen3-TTS tracker also records removal of Talker `torch.compile` after fixed-protocol tests failed to show reproducible end-to-end benefit. This directly supports Hottop's runtime+model coherence gate rather than a floating candidate label.
- **llama.cpp Qwen3-TTS:** issue #27937 opened 2026-08-29 reports that the default 32768 context can allocate roughly 3.5 GB of KV cache for Qwen3-TTS where a much smaller context may suffice. Treat this as a future operator-runtime performance signal only; it does not prove Mandarin quality or justify replacing the prepared qwentts.cpp/CrispASR/audio.cpp routes.
- **LightX2V/Wan2.2:** no fresh result in this cycle provides Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- **DiffSynth-Studio / MiniMax-H3 NF4:** remains research/operator-benchmark only under the previously recorded base-model license and geography/commercial gates.
- **MiniMax H3 Motion Lab / LongCat / Step-Audio-EditX / Supertonic:** existing research-only gates remain unchanged; no new evidence clears them for unattended production.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or the prepared 1.7B TTS benchmark candidates.

## Immediate next actions

1. Finish PR #267 only after its durable-record/status exact head is GREEN and the diff/review-thread check is clean; then squash-merge by exact SHA and verify live `main` evidence.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
4. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; after same-line local WAV generation, use `inspect-tts-benchmark` with at least one cold plus one warm trial **per candidate**, one exact runtime revision and one exact model revision per candidate, distinct resolved WAV artifacts per trial, and additional warm repeats where useful. Keep listening/speaker/onset evidence independent from speed.
5. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
6. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
