# Hottop Status

Last updated: 2026-08-29
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified live-main evidence before this docs sync: **`main@69b3b0db2bb2f24f6387af323c8a06b159d9bdf1` → CI #2046 passed** on Python 3.11/3.12.

PR #188 closed a qwentts.cpp operator-preflight provenance gap. The previous binder could sample file size before hashing and then bind a digest after the local executable/GGUF had changed, creating a mixed artifact identity that described no single stable filesystem state.

TDD evidence:

- RED `53e4cb2e90a7b4029c1ab735003357f62792bf05` → CI #2042: Ruff passed; Python 3.11 pytest failed on mutation-during-preflight; Python 3.12 was cancelled by fail-fast.
- GREEN `6befa6cc43fa9a10dc110371a082df3d4adf2fb8` → CI #2043 passed on Python 3.11/3.12.
- Durable-record exact head `36a1e75c6987d2e3a95cc97f8cc1c6cc935cb9a1` → CI #2044 and replacement-PR CI #2045 passed.
- PR #188 was squash-merged as `69b3b0db2bb2f24f6387af323c8a06b159d9bdf1`; post-merge CI #2046 passed.

The read-only qwentts.cpp preflight now requires a stable local artifact snapshot across bounded-memory SHA-256 streaming. It compares device id, inode, size, nanosecond mtime, nanosecond ctime and file mode before/after hashing. Replacement, append, truncation, disappearance or permission/file-identity change fails closed with no stable `LocalArtifactIdentity` emitted for that input.

The existing structural gate remains: local files must be non-empty, the binary must be executable, and both model files must expose a complete 24-byte fixed GGUF header surface. The gate remains intentionally shallow and version-tolerant; it does not parse model metadata.

`ready=true` still means only: operator-supplied local inputs were present, shallowly GGUF-like where applicable, stable during preflight and exact-byte-bound. It does **not** prove checkpoint identity, checkpoint/preset-speaker/output rights, qwentts runtime compatibility, synthesis success or Mandarin quality.

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

The preflight performs bounded 1 MiB streaming hashes, shallow fixed-header GGUF checks and stable-snapshot comparison. It never executes qwentts.cpp, opens a network connection, downloads/builds anything, provisions hardware, changes model-hub runtime state or claims audio quality.

Future 1.7B A/B must bind exact runtime/build/backend, checkpoint capability mode, model/tokenizer/GGUF bytes, exact Mandarin line, valid preset speaker or separately rights-cleared reference conditioning, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's bytes/duration/PCM integrity, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Capability binding remains independent from output evidence: unsupported speaker/voice/instruction/reference conditioning must fail closed before execution; repeated trials still verify actual speaker consistency and output integrity afterward.

## Fresh ecosystem radar — 2026-08-29

- **LightX2V/Wan2.2:** no Hottop-measured continuity, quality or runtime gain was found for the tested I2V subset in this cycle. Keep the tested pin and **do not freshness-only repin**.
- **Qwen3-TTS / qwentts.cpp:** no reviewed upstream change in this cycle justifies changing current admission or adding an automatic serving stack. Preset-speaker/output-publication rights remain a separate gate from source/model license and must be resolved for the actual benchmark/output use.
- **WildActor:** remains a research-only multi-reference identity signal because reviewed source/checkpoint/data/reference/API/runtime rights are not all cleared. No copied code, model/data download, hosted API use or runtime-ready claim.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or current tested operator video route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. If an operator provisions qwentts.cpp plus exact 1.7B CustomVoice GGUF assets locally, run `hottop-models probe-qwentts-cpp` first. Only after stable-snapshot + bounded-memory + fixed-header + exact-byte preflight passes may a separate explicit same-line Mandarin A/B execute.
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
