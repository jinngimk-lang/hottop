# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@2fc00a88ce1ff63ccf07c15de77daf97d7b30238` / CI #2277** on Python 3.11/3.12.

Four TTS benchmark evidence-coherence gaps are now closed:

- per-candidate cold/warm completeness: RED `CI #2241` → GREEN `CI #2243/#2244` → merged/post-merge `CI #2246`;
- per-candidate runtime-revision consistency: RED `CI #2249` → GREEN `CI #2250/#2251` → merged/post-merge `CI #2253`;
- per-candidate model/checkpoint-revision consistency: RED `CI #2256` → GREEN `CI #2261/#2264` → merged/post-merge `CI #2266`;
- benchmark generation-protocol binding: RED **`CI #2269`** → GREEN `CI #2274/#2275` → merged main/post-merge **`CI #2277`**. A ready benchmark now requires one non-empty finite JSON `generation_protocol` for the whole comparison and preserves its canonical sorted-key JSON SHA-256 in `hottop.tts-benchmark.v1`.

The generation protocol is declared benchmark-control evidence, not proof a runtime obeyed a similarly named flag. Actual runtime CLI/config provenance remains separately required.

These changes add no neural runtime execution, provider route, dependency, model download, GPU provisioning, credential or paid path. No open PR is expected from this completed workstream.

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

It inspects already-produced local WAVs only and never executes TTS, accesses the network, installs dependencies, downloads models, provisions GPU resources or calls a paid service.

A ready benchmark now requires all of the following:

- exact text, language and checkpoint-supported preset speaker;
- one non-empty finite JSON **generation protocol** for the whole benchmark, covering the seed/sampling/generation-ceiling semantics used to make candidate runs comparable; the evidence preserves both the protocol and its canonical SHA-256;
- at least one `cold` and one `warm` trial for every candidate; additional independent warm repeats remain valid and preferred;
- one exact `runtime_revision` and one exact `model_revision` per candidate;
- finite positive latency;
- a distinct resolved WAV path for every trial; identical bytes remain legal when independently produced as separate artifacts;
- WAV/PCM integrity and `listening_required=true` so speed/stream integrity cannot be mistaken for naturalness or speaker-quality proof.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker and one declared generation protocol while preserving actual runtime/model/config provenance, cold/warm timing, distinct WAV artifact instances, WAV/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed before execution; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **Qwen3-TTS official source:** live `QwenLM/Qwen3-TTS@022e286b98fbec7e1e916cb940cdf532cd9f488e`; no official change in this cycle clears the 1.7B operator-local benchmark gate.
- **Generation controls matter:** current Qwen3-TTS-compatible runtimes expose seed/sampling controls and `max_new_tokens`; public Qwen3-TTS serving evidence includes rare missing-EOS/repetition runs that continue until the generation ceiling. This supports binding generation protocol identity rather than comparing WAVs produced under unspecified settings.
- **LightX2V/Wan2.2:** live upstream remains `ModelTC/LightX2V@7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`; the reviewed Aug. 28 change is example-script path cleanup, not a Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- Existing DiffSynth/MiniMax-H3, Motion Lab, LongCat, Step-Audio-EditX and other research gates remain unchanged; no reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or the prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; after same-line local WAV generation, use `inspect-tts-benchmark` with one declared generation protocol, at least one cold plus one warm trial per candidate, one exact runtime revision and one exact model revision per candidate, and distinct resolved WAV artifacts per trial. Keep listening/speaker/onset evidence independent from speed.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
5. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
