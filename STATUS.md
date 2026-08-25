# Hottop Status

Last updated: 2026-08-25
Active workstream: PR #13 `prod/qwen3-tts-customvoice`
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Foundation PR #1 and Production PR #12 are merged. Production v0.2 now has a **real, automatically reproducible zero-cost config-to-MP4 baseline** plus isolated optional free/operator-owned generative and audio routes.

Closed production evidence:

- `software3d` is integrated into normal `video-run` execution. It renders real 3D geometry/projection/animation, encodes per-shot MP4 through FFmpeg, and requires no Blender, GPU or model download.
- software3d shots emit `.artifact.json` sidecars with SHA-256 + byte size. `video-run` validates planned backend / artifact kind / backend / shot identity / output identity after generation, and MoviePy independently re-verifies exact bytes before composition.
- The checked-in cow/snake source + `anti-polish-software3d.yml` has executed end to end on a clean Ubuntu runner with role-aware eSpeak Mandarin dialogue, original synthetic music, procedural SFX/Foley, MoviePy and FFmpeg.
- The production smoke artifact contains final MP4, run-result, plan, ffprobe evidence and five provenance manifests. Verified final media: **10.008005 s**, **H.264 / yuv420p**, **AAC**, SHA-256 `bab46a50557ddb984d42abb1342d5e74e2f73cd9aa1db83fdfa2369b4a48674a`.
- PR #12 exact-head CI + production-smoke passed and the PR was squash-merged to `main` as `fde10b2b37536e66f29ff7af7a93966eb1c27fb6`; post-merge main CI run 1300 passed.
- ZeroGPU, WanGP and Comfy boundaries remain quality/provenance gated and fail closed; cross-shot identity locks and rights-safe references are checked before generation.
- eSpeak remains the guaranteed local TTS fallback. A rights-safe local CosyVoice3 adapter exists for reference-conditioned voice work.

## Mandarin dialogue quality workstream

Fresh official review on 2026-08-25 found that **Qwen3-TTS-12Hz-0.6B-CustomVoice** is a better normal-dialogue benchmark target than the previously tracked Base checkpoint:

- upstream code revision reviewed: `QwenLM/Qwen3-TTS@022e286b98fbec7e1e916cb940cdf532cd9f488e`;
- code license: Apache-2.0; official CustomVoice model card license: Apache-2.0;
- official checkpoint is roughly 2.5 GB and exposes nine preset timbres across ten languages, including Mandarin, plus natural-language style instructions;
- unlike Base voice cloning, the preset CustomVoice path does **not** require reference voice audio, so it avoids making voice-identity rights provenance a routine requirement;
- the official quickstart can resolve a remote model ID, so Hottop deliberately does the opposite in unattended safety policy: only an already provisioned **local model directory** is accepted; runtime sets Hugging Face/Transformers offline mode and local-only loading; no CI/model auto-download is allowed.

PR #13 adds a benchmark-ready isolated adapter in `src/hottop/audio_qwen3_tts.py`. It does **not** replace eSpeak or become a standard `video-run` backend yet. The first clean RED reached pytest on CI run 1303; implementation CI run 1305 passed Ruff + full pytest on Python 3.11 and 3.12. The candidate registry now marks CustomVoice as `benchmark_ready_operator_local` and demotes Base to a rights-gated voice-clone benchmark.

Promotion gate: wire Qwen3 CustomVoice into normal `VideoProductionConfig.audio.voice_backend` only after an operator-owned local model/GPU benchmark demonstrates materially better Mandarin intelligibility/prosody at acceptable runtime cost. No paid endpoint or hidden download may satisfy this gate.

## Autonomous governance / ecosystem radar

`PROJECT.md` remains canonical. Every active production cycle identifies the measured gap first and then performs targeted official/public upstream review. Candidates must pass code + weights/data license, cost, hardware, install/network security, measurable value and rollback gates before promotion. Useful capabilities enter through narrow adapters/config/tests/benchmarks rather than broad vendoring.

## Durable motion contract

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg → final media verification`

Default unattended target is zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never turn into paid credits or a hidden paid provider. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity remain hard gates.

## Current ecosystem priorities

1. **Mandarin dialogue quality:** benchmark local Qwen3 CustomVoice and CosyVoice3 against eSpeak when operator-provisioned runtimes are present. Voice cloning/reference audio remains rights-gated.
2. **Identity / reference-conditioned cinematic video:** benchmark only candidates whose exact code and weights terms permit intended use. WanGP is the practical operator route; SCAIL-2 and LongCat remain high-interest; H3 remains license-gated.
3. **Cinematic style proof:** produce a second complete reproducible lower-roughness Odyssey witch/pigs case so style routing is proven beyond Anti-Polish.
4. **Production evidence:** prefer actual config→moving shots→audio→composite→verified MP4 evidence over accumulating unbenchmarked abstractions.

## Immediate next actions

1. Close PR #13 after exact-head CI verifies the adapter/registry/status tree together; merge only as a benchmark-ready optional adapter, not a default voice backend.
2. If no local Qwen/CosyVoice model is operator-provisioned, do not download one automatically; continue the next unblocked Production v0.2 action instead.
3. Advance the lower-roughness Odyssey witch/pigs source toward a second reproducible full-pipeline case, reusing existing MoviePy/FFmpeg/audio/provenance gates rather than adding provider abstraction.
4. Continue targeted upstream scans against measured gaps and integrate only material improvements that clear the admission gate.
