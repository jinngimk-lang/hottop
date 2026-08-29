# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production head: **`main@8c7ba1d4c28e21b5c682abfedaabaf6a12913598`**. It exposes the already-reviewed audio.cpp Qwen3-TTS 1.7B candidate through the unified model-hub discovery layer without adding a runtime adapter or production route. Post-merge CI **#2128** passed on Python 3.11/3.12.

Audio.cpp admission/model-hub evidence:

- PR #216 exact head `c7a375a41fc53dee4edb87b6db8d5ce1faabff56` passed CI #2123, added only `docs/research/2026-08-29-audio-cpp-qwen3-tts-admission.md` plus the narrow operator benchmark manifest, then squash-merged as `7a10d487ad121cbb39da1afe1a394b46754e90c3`; post-merge CI #2124 passed on Python 3.11/3.12.
- Reviewed upstream is `0xShug0/audio.cpp@a76ec04f620da829e4a53032247369083ba1ad45`, Apache-2.0 source. Qwen model/tokenizer/GGUF and output-publication rights remain separate operator gates.
- The admission is benchmark-only: no normal `video-run`, no auto-build, no model download/conversion, no dependency fetch, no container pull, no GPU provisioning, no credentials and no paid call.
- Model-hub TDD RED `9fde4d80a88dc0ad03fc6197e56875568ce17b8e` → CI #2125: Ruff passed and pytest reported exactly **1 failed / 556 passed**, solely because `qwen3-tts-audio-cpp-1b7` was absent from the unified registry.
- GREEN exact head `8c4f6e3b88dd61219afb889a3bc2fd7f2cc8914b` added only the fail-closed registry entry + contract test → CI #2126 passed on Python 3.11/3.12.
- The ready-for-review connector hit the known GitHub GraphQL `fullDatabaseId` compatibility error. Draft #217 was closed and non-draft #218 recreated on the **same exact head**; no force/update-ref or history rewrite was used.
- PR #218 squash-merged as `8c7ba1d4c28e21b5c682abfedaabaf6a12913598`; post-merge CI #2128 passed on Python 3.11/3.12.

`qwen3-tts-audio-cpp-1b7` is now discoverable as `benchmark_candidate / integration_ready=false / runtime_status=unprobed / self_owned_compute` with CPU/CUDA/HIP/Vulkan/Metal capability metadata. It is excluded from integration-ready and runtime-ready selection. Upstream support is implementation evidence only, not Hottop Mandarin-quality evidence.

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

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Current local benchmark candidates include:

- `qwen3-tts-qwentts-cpp-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — unified discovery entry only; **no executable preflight/adapter admitted yet**;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

The qwentts/CrispASR preflights require resolved-target binding, bounded-memory SHA-256, stable before/after filesystem snapshots, executable permission, complete 24-byte GGUF fixed header, reviewed GGUF version `3`, non-zero tensor count and path/byte distinctness across incompatible runtime roles. They do not execute runtimes or prove checkpoint identity, licensing, speaker capability or Mandarin quality.

Future 1.7B cross-runtime A/B must bind exact source/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, the **same Mandarin line**, the same checkpoint-supported preset speaker, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's SHA-256/size/duration/PCM integrity, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Unsupported speaker/voice/instruction/reference conditioning must fail closed before execution. Reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`. Latest reviewed change cleans Wan-Animate-2 example paths and does not provide Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V route. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change justifies altering the 1.7B operator-local benchmark gate.
- **audio.cpp:** reviewed upstream remains `a76ec04f620da829e4a53032247369083ba1ad45` as of this cycle. It is active and supports several native backends, but upstream capability/performance evidence is not a Hottop Mandarin-quality result.
- **qwentts.cpp/CrispASR:** existing admissions remain unchanged. Auto-download/build paths stay forbidden in unattended Hottop execution.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route or current tested LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. If an operator provisions qwentts.cpp or CrispASR plus exact 1.7B CustomVoice GGUF assets locally, run the existing read-only preflight first; only after it passes may a separate explicit same-line Mandarin A/B execute.
4. If an operator provisions audio.cpp plus independently reviewed local Qwen3-TTS 1.7B CustomVoice assets, first add a narrow read-only artifact/runtime preflight or equivalent byte-bound benchmark harness. Do **not** promote the new discovery entry directly into `video-run`.
5. In every 1.7B cross-runtime A/B, use the same line, supported preset speaker and bounded generation settings, and preserve repeated speaker/onset/intelligibility/naturalness/RTF/PCM/provenance as separate evidence dimensions.
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
