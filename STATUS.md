# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified merge: **`main@49e8f64b8c56473c3c7260711d510f9b745f6d75`**, which added a read-only local artifact preflight for the already-admitted CrispASR Qwen3-TTS 1.7B benchmark candidate. Final merge-candidate head `5bbc05b2fab5e76c8a3a63c0210cac296a484711` passed CI #2118 on Python 3.11/3.12; squash merge via non-draft PR #214 produced `49e8f64b8c56473c3c7260711d510f9b745f6d75`, and post-merge CI #2120 also passed on Python 3.11/3.12.

CrispASR preflight TDD evidence:

- RED exact head `166f094a46c24acb8f37f0ca7d01685fb715afc3` → CI #2111: Ruff passed; pytest reported exactly `2 failed / 554 passed`, both because `probe-crispasr` did not exist.
- GREEN implementation `0dcd45627bfd88d68f2b688d5f3cf741271d36f2` added only the read-only artifact preflight + CLI surface → CI #2115 passed on Python 3.11/3.12.
- Final exact head `5bbc05b2fab5e76c8a3a63c0210cac296a484711` added the durable admission update → CI #2118 passed on Python 3.11/3.12.
- The ready-for-review GraphQL mutation hit the known connector `fullDatabaseId` compatibility error. Draft #213 was closed and non-draft #214 recreated on the **same exact head**; no force/update-ref or history rewrite was used.
- PR #214 squash-merged as `49e8f64b8c56473c3c7260711d510f9b745f6d75`; post-merge CI #2120 passed on Python 3.11/3.12.

No executable CrispASR synthesis adapter, model download, build/install path, GPU provisioning, credentials, paid call or production routing change was admitted. The new command only inspects operator-supplied local artifacts.

The prior qwentts.cpp preflight closure remains intact. Hottop requires model inputs to be non-empty, GGUF-magic-correct, at least 24 bytes, fixed-header version `3`, and to declare at least one tensor. Existing protections remain: symlinks resolve before identity binding; bounded 1 MiB streaming SHA-256; before/after device/inode/size/mtime_ns/ctime_ns/mode stability checks; executable permission checks; executable/talker/tokenizer path-or-byte role distinctness; no execution/network/download/build/GPU provisioning/runtime-ready promotion.

`ready=true` for either local GGUF preflight means only that operator-supplied local inputs were present, shallowly GGUF-structured for the currently reviewed version where applicable, stable during preflight, exact-byte-bound to resolved targets, non-zero-tensor for model roles, and distinct across incompatible runtime roles. It does **not** prove semantic checkpoint identity, model/tokenizer/checkpoint rights, runtime compatibility, checkpoint speaker capability, synthesis success or Mandarin quality.

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

`qwen3-tts-ncnn-0b6`, `qwen3-tts-qwentts-cpp-1b7` and `qwen3-tts-crispasr-1b7` are **benchmark candidates only** with `integration_ready=false / runtime_status=unprobed`.

Read-only qwentts input preflight:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

Read-only CrispASR input preflight:

```text
hottop-models probe-crispasr \
  --executable /local/path/crispasr \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

Both preflights reuse the same hardened local artifact identity boundary: resolved symlink targets, bounded-memory streaming SHA-256, before/after filesystem snapshot stability, executable permission checks, complete 24-byte GGUF fixed header, reviewed GGUF version `3`, non-zero tensor count, and path/byte distinctness across incompatible runtime roles. They never execute the runtime, open network connections, invoke auto-download paths, build dependencies, provision hardware, change model-hub runtime state or claim audio quality.

CrispASR remains a second **operator-provisioned cross-runtime benchmark candidate** at exact reviewed source `bb77301c4dbde1fca217e1a19584b1ae0167ee03`. Source is MIT; reviewed `cstr` 1.7B CustomVoice GGUF and tokenizer/codec model cards declare Apache-2.0 conversions of official Qwen Apache-2.0 assets. Its `-m auto` downloader remains forbidden in Hottop unattended execution. Preset CustomVoice is the initial benchmark scope and reference-audio cloning remains separately rights-gated.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Capability binding remains independent from output evidence: unsupported speaker/voice/instruction/reference conditioning must fail closed before execution; repeated trials still verify actual speaker consistency and output integrity afterward.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** reviewed upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`; latest reviewed change only cleaned hard-coded Wan-Animate-2 example paths and provides no Hottop-measured continuity/quality/runtime gain. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change in this cycle justifies changing the 1.7B operator-local benchmark gate.
- **qwentts.cpp:** reviewed `master` remains `a8a7716b530e49fed537c57711247c12fbbb903c`. No reviewed upstream change in this cycle justifies automatic serving/build integration.
- **CrispASR:** reviewed source remains `bb77301c4dbde1fca217e1a19584b1ae0167ee03` on 2026-08-29. The latest reviewed change adds configurable padding silence for a VLC/C2PA playback issue and does not change this admission. `-m auto` remains excluded; public issue #183 remains runtime-specific performance evidence, not Mandarin-quality proof.
- **llama.cpp `llama-tts`:** remains research-only for this measured gap. Prior Qwen3-TTS Base/Vulkan repetition/EOS and Vulkan assertion failures reinforce bounded-generation and final PCM-duration/integrity gates, but do not justify a new unattended runtime.
- **WildActor:** remains a research-only multi-reference identity signal because reviewed source/checkpoint/data/reference/API/runtime rights are not all cleared.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or current tested operator video route. CrispASR preflight only improves the future **cross-runtime TTS benchmark readiness surface**.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first. Only after its artifact checks pass may a separate explicit same-line Mandarin A/B execute.
4. If an operator provisions CrispASR plus exact 1.7B CustomVoice talker/tokenizer GGUF assets locally, run `hottop-models probe-crispasr` first and **do not use `-m auto`**. Only after the same artifact checks pass may a separate explicit same-line Mandarin A/B execute.
5. For all CustomVoice A/B, use only checkpoint-supported preset speaker conditioning. Do not silently drop unsupported conditioning or reuse Base-only reference/latent registration semantics on a CustomVoice checkpoint.
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
