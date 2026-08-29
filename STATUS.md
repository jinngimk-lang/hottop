# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest production-code merge in this workstream: **`main@719f5b35660a49baa4724b9ea6b741c1d4f1c273`**, from the qwentts.cpp distinct-model-role preflight closure. Exact GREEN PR head `3baeddfad9b4167f449e9ddc0bf0d291364d673e` passed CI #2060 on Python 3.11/3.12 before merge, and post-merge CI #2062 passed on Python 3.11/3.12.

The new closure fixes an input-set provenance defect in the read-only qwentts.cpp operator preflight. Upstream qwentts.cpp loads a talker GGUF (`--model`) and a separate shared tokenizer/codec GGUF (`--codec`). Hottop previously validated both inputs independently, so one valid GGUF—or identical bytes copied under two names—could incorrectly satisfy both roles.

TDD evidence:

- RED `3ff5c34a770aa48be0ebf6c94b042b7656afcde7` → CI #2059: Ruff passed; pytest failed on the new role-distinctness contract.
- GREEN `3baeddfad9b4167f449e9ddc0bf0d291364d673e` → CI #2060: Python 3.11/3.12 Ruff + full pytest passed.
- The ready-for-review GraphQL mutation again failed on the known `fullDatabaseId` compatibility error. Draft #195 was closed and non-draft #196 recreated on the **same exact GREEN head**, then squash-merged as `719f5b35660a49baa4724b9ea6b741c1d4f1c273` without force/update-ref bypass.
- Post-merge CI #2062 passed on Python 3.11/3.12.

The preflight now rejects talker/tokenizer pairs that resolve to the same concrete path **or** have identical exact SHA-256 bytes. Existing protections remain: symlinks are resolved before identity binding; bounded 1 MiB streaming SHA-256; complete 24-byte GGUF fixed-header surface; before/after device/inode/size/mtime_ns/ctime_ns/mode stability checks; executable checks; no execution/network/download/build/GPU provisioning/runtime-ready promotion.

`ready=true` therefore means only: operator-supplied local inputs were present, structurally GGUF-like where applicable, stable during preflight, exact-byte-bound to resolved targets, and distinct across the required talker/tokenizer roles. It does **not** prove semantic checkpoint identity, checkpoint/preset-speaker/output rights, qwentts runtime compatibility, synthesis success or Mandarin quality.

Durable record: `docs/research/2026-08-29-qwentts-distinct-role-artifacts.md`.

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

`qwen3-tts-ncnn-0b6` and `qwen3-tts-qwentts-cpp-1b7` remain **benchmark candidates only** with `integration_ready=false / runtime_status=unprobed`.

Read-only qwentts input preflight:

```text
hottop-models probe-qwentts-cpp \
  --executable /local/path/qwentts-cli \
  --talker-gguf /local/path/talker.gguf \
  --tokenizer-gguf /local/path/tokenizer.gguf
```

The talker and tokenizer/codec must be distinct artifacts; same resolved path or same exact SHA-256 fails closed. The preflight never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime state or claims audio quality.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Capability binding remains independent from output evidence: unsupported speaker/voice/instruction/reference conditioning must fail closed before execution; repeated trials still verify actual speaker consistency and output integrity afterward.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** last reviewed upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`; latest reviewed change only cleaned hard-coded Wan-Animate-2 example paths and provides no Hottop-measured continuity/quality/runtime gain. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** last reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change in this cycle justifies changing the 1.7B operator-local benchmark gate.
- **qwentts.cpp:** reviewed `master` remains `a8a7716b530e49fed537c57711247c12fbbb903c`. Its documented runtime topology confirms separate talker (`--model`) and tokenizer/codec (`--codec`) roles, which now informs the local preflight input-set gate. No reviewed upstream change justifies automatic serving/build integration.
- **WildActor:** remains a research-only multi-reference identity signal because reviewed source/checkpoint/data/reference/API/runtime rights are not all cleared.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first. Only after resolved-target + stable-snapshot + bounded-memory + fixed-header + exact-byte + distinct-role preflight passes may a separate explicit same-line Mandarin A/B execute.
4. For qwentts CustomVoice A/B, use only checkpoint-supported preset speaker conditioning. Do not silently drop unsupported conditioning or reuse Base-only reference/latent registration semantics on a CustomVoice checkpoint.
5. In real Qwen 1.7B A/B, preserve repeated speaker consistency, short-onset stability, intelligibility/naturalness, latency/RTF, PCM duration/integrity and exact runtime/model/output provenance as separate evidence dimensions.
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