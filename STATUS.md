# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production head before this documentation-only workstream: **`main@5dd36793a1f865ac020b44c8edbdbb4b16972ca2`**. It contains the merged audio.cpp Qwen3-TTS 1.7B CustomVoice read-only preflight/status closure. Exact-head CI **#2143** passed on Python 3.11/3.12. Live GitHub state must still be re-fetched on every recovery.

Audio.cpp admission/preflight evidence:

- Reviewed upstream remains `0xShug0/audio.cpp@a76ec04f620da829e4a53032247369083ba1ad45`, Apache-2.0 source. Qwen model/tokenizer/GGUF and output-publication rights remain separate operator gates.
- Existing model-hub entry remains `benchmark_candidate / integration_ready=false / runtime_status=unprobed / self_owned_compute`; no normal `video-run`, auto-build, model download/conversion, dependency fetch, container pull, GPU provisioning, credentials or paid call was added.
- Preflight RED `b862e4d50ce73d05737367d677dc1db1c034fee5` → CI #2133: Ruff passed; pytest failed on the intentionally missing `probe-audio-cpp` contract.
- GREEN implementation `b37cdc5433d974b44d82d94b3d6b619f1a874727` → CI #2137: Python 3.11/3.12 Ruff + full pytest passed.
- Final docs-synced exact head `be1df6451b4823b29b82eb32c36e967a0e2b54d9` → CI #2139 passed on Python 3.11/3.12 with no review threads.
- The ready-for-review connector hit the known GitHub GraphQL `fullDatabaseId` compatibility error. Draft #220 was closed and non-draft #221 recreated on the **same exact verified head**; no force/update-ref or history rewrite was used.
- PR #221 squash-merged as `03bcc2dfd0a449c47faea391d7f22b3281babb72`; post-merge CI #2141 passed on Python 3.11/3.12. Follow-up status sync reached `main@5dd36793a1f865ac020b44c8edbdbb4b16972ca2`, whose exact-head CI #2143 also passed.
- A fresh exact-source audit of audio.cpp `model_specs/qwen3_tts.json` plus `docs/models/qwen3.md` confirms the reviewed converted Qwen3-TTS layout: main `model.safetensors` and `speech_tokenizer/model.safetensors` are converted independently and placed as `model.gguf` beside each source. The package contract also supports recursively embedded sidecars, so there is no evidence for inventing a third mandatory preflight artifact.

`hottop-models probe-audio-cpp --executable <audiocpp_cli> --model-dir <Qwen3-TTS-12Hz-1.7B-CustomVoice>` binds an already provisioned operator input set without execution. The resolved model directory must contain `model.gguf` plus `speech_tokenizer/model.gguf`. The probe reuses Hottop's hardened local artifact boundary: concrete resolved targets, bounded-memory SHA-256, stable before/after filesystem snapshots, executable permission, complete GGUF v3 fixed headers, non-zero tensor counts and incompatible-role path/byte distinctness. `ready=true` is only benchmark-input readiness; it does not prove checkpoint identity, licensing, speaker capability, runtime success, Mandarin quality or publication rights.

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
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available; **no production runtime adapter admitted**;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

The qwentts/CrispASR/audio.cpp preflights bind operator-provided local artifacts only. They require resolved-target binding, bounded-memory SHA-256, stable before/after filesystem snapshots, executable permission, complete 24-byte GGUF fixed headers, reviewed GGUF version `3`, non-zero tensor counts and path/byte distinctness across incompatible runtime roles. The audio.cpp probe additionally locks one resolved model directory and the reviewed `model.gguf` + `speech_tokenizer/model.gguf` layout. None of these probes executes a runtime or proves checkpoint identity, licensing, conditioning capability or Mandarin quality.

Future 1.7B cross-runtime A/B must bind exact source/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, the **same Mandarin line**, the same checkpoint-supported preset speaker, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's SHA-256/size/duration/PCM integrity, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Unsupported speaker/voice/instruction/reference conditioning must fail closed before execution. Reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`. Latest reviewed changes are example-path cleanup plus H3/XPU-specific work and do not provide Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V route. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change justifies altering the 1.7B operator-local benchmark gate.
- **audio.cpp:** reviewed upstream remains `a76ec04f620da829e4a53032247369083ba1ad45`. A fresh exact-source audit confirms the current two-GGUF CustomVoice model-directory assumption against upstream conversion docs/package semantics; no extra mandatory local artifact was found. Upstream capability/performance evidence remains separate from Hottop Mandarin-quality evidence.
- **qwentts.cpp/CrispASR:** existing admissions remain unchanged. Auto-download/build paths stay forbidden in unattended Hottop execution.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route or current tested LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. If an operator provisions qwentts.cpp or CrispASR plus exact 1.7B CustomVoice GGUF assets locally, run the existing read-only preflight first; only after it passes may a separate explicit same-line Mandarin A/B execute.
4. If an operator provisions audio.cpp plus independently reviewed local Qwen3-TTS 1.7B CustomVoice assets, run `probe-audio-cpp` first. Only after it reports a stable byte-bound input set may a **separate explicit** same-line Mandarin A/B execute; do not promote the candidate directly into `video-run`.
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
