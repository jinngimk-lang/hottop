# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production evidence point: **`main@6415dee873c063bd739e3216c2c81d28fe92111e`**. Post-merge CI **#2176** passed on Python 3.11/3.12.

This cycle added a provider-neutral, read-only local TTS A/B evidence surface without changing any production provider/runtime route:

- clean RED after test isolation: pytest failed because `hottop.tts_benchmark` did not exist;
- exact GREEN head `eda60c6a887a28f83f5a266c6b2280fbc8c37b6f` → PR CI **#2174**, Python 3.11/3.12 Ruff + full pytest green; Python 3.11 reported **563 passed**;
- the known ready-for-review connector `fullDatabaseId` GraphQL incompatibility was handled without force/update-ref: draft #232 was closed and non-draft #233 recreated on the **same verified exact head**;
- PR #233 squash-merged as `6415dee873c063bd739e3216c2c81d28fe92111e`; post-merge CI **#2176** passed.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest retained deterministic smoke evidence:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` derived from exact ordered subject-bearing plan semantics; generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

**Echo-Memory** remains a scene/revisit-memory benchmark signal only. Reviewed source `Echo-Team-Joy-Future-Academy-JD/Echo-Memory@194be716aedaa84d9bd377740d6e6d9c32a309cb` and public Echo checkpoints are CC BY 4.0; the current released backbone is Wan2.1 T2V 1.3B, while Wan2.2/5B/14B remain roadmap items. Revisit/scene memory cannot substitute for subject identity or requested-action evidence.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Current local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available; reviewed manual v0.7.0 runtime archives remain operator-provisioned only;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

New shared evidence surface:

`hottop-models inspect-tts-benchmark --spec <benchmark.json>`

It inspects **already-produced local WAVs only**. It never executes TTS, accesses the network, installs dependencies, downloads models, provisions GPU resources or calls a paid service. `hottop.tts-benchmark.v1` binds:

- exact benchmark text, language and preset speaker label;
- candidate/runtime revision and cold/warm trial identity;
- exact WAV resolved path, SHA-256 and size;
- sample rate, channels, sample width, frame count and duration;
- digital-silence rejection and positive measured latency;
- playback-duration / generation-latency factor;
- `listening_required=true`, so speed/PCM integrity cannot be mistaken for Mandarin naturalness, intelligibility, onset stability or speaker consistency.

The method was independently derived after reviewing `5uck1ess/tts-bench@020a69422c96224785a8dc4b95466676119a7dc2`. Its benchmark code is MIT, but its full installer surface reports roughly **39 GB** of per-model virtual environments plus roughly **125 GB** of model weights and can fetch/build model-specific dependencies. Hottop therefore admits only the measurement separation idea, not the installer/model stack. Durable review: `docs/research/2026-08-30-tts-bench-method-admission.md`.

Future 1.7B cross-runtime A/B must still use the **same Mandarin line**, same checkpoint-supported preset speaker and bounded generation settings, while separately preserving exact runtime/model bytes, cold/warm timing, every WAV's bytes/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported speaker/voice/instruction/reference conditioning must fail closed before execution. Reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **LightX2V/Wan2.2:** reviewed upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`. Latest reviewed changes do not provide Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V route. Keep the tested pin; no freshness-only repin.
- **WanGP/Wan2GP:** reviewed upstream `main` is `c3aa2915b039f898285d4a5de102d89eabf83237`; the reviewed PiD change is post-processing/upsampler maintenance, not improved Hottop reference-conditioned identity/requested-action motion. Durable review: `docs/research/2026-08-30-wangp-pid-radar.md`.
- **Echo-Memory:** reviewed exact source `194be716aedaa84d9bd377740d6e6d9c32a309cb`, CC BY 4.0; keep research/benchmark-only. Durable review: `docs/research/2026-08-30-echo-memory-admission.md`.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change justifies altering the 1.7B operator-local benchmark gate.
- **audio.cpp:** upstream maintenance after v0.7.0 does not justify freshness-only source repin; reviewed v0.7.0 Ubuntu CPU/Vulkan archives remain exact-digest manual operator options only, and Hottop must not invoke the bundled model manager.
- **tts-bench:** exact method review `020a69422c96224785a8dc4b95466676119a7dc2`, MIT benchmark code only. Its large automatic environment/model provisioning surface is rejected; Hottop integrates only a narrow local-WAV evidence contract.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route or current tested LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. If a measured future sequence specifically requires leave-and-return scene/viewpoint memory, benchmark Echo-Memory only after operator-provisioned exact source/base/checkpoint assets and rights-safe action/reference bytes are available.
4. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first. Hottop itself must not fetch/build those runtimes or models.
5. After an explicit operator-local runtime produces same-line WAV trials, write a benchmark spec and run `hottop-models inspect-tts-benchmark --spec <benchmark.json>` to bind WAV bytes/stream metadata and cold/warm speed evidence. Human/listening evidence, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication rights remain independent gates.
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
