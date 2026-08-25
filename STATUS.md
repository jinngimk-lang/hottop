# Hottop Status

Last updated: 2026-08-25
Active workstream: PR #12 `prod/software3d-config-runtime`
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Foundation PR #1 is merged. Production v0.2 is active. Hottop now has a **real, automatically reproducible zero-cost config-to-MP4 baseline** plus optional free/operator-owned generative routes.

Closed in the current production pass:

- `software3d` is integrated into normal `video-run` execution. It renders actual 3D geometry/projection/animation, encodes per-shot MP4 through FFmpeg, and does not require Blender, a GPU or model download.
- software3d shots emit `.artifact.json` sidecars with SHA-256 + byte size. `video-run` now discovers those sidecars, validates planned backend / artifact kind / backend / shot identity / output identity immediately after generation, and MoviePy independently re-verifies byte identity immediately before composition.
- The full software3d profile carries role-aware eSpeak Mandarin dialogue, original synthetic music and procedural SFX/Foley through MoviePy and FFmpeg.
- `production-smoke` run **32823329496** successfully executed the checked-in `examples/video/inkclaw-cow-snake.render.json` + `config/video/anti-polish-software3d.yml` with `hottop video-run --execute` on a clean Ubuntu runner using only free/open local dependencies.
- The smoke artifact contains final MP4, run-result, video plan, ffprobe evidence and five shot provenance manifests. Final media: **10.008005 s**, **H.264 / yuv420p**, **AAC**; final MP4 SHA-256 `bab46a50557ddb984d42abb1342d5e74e2f73cd9aa1db83fdfa2369b4a48674a`. `run-result` records `executed=true`, `ready=true`, five manifests and 12 executed stage commands.
- Ordinary PR CI at the production code head passed Ruff + full pytest on Python 3.11 and 3.12.
- ZeroGPU, WanGP and Comfy external boundaries remain quality/provenance gated and fail closed rather than silently using paid fallback.
- Cross-shot identity locks and rights-safe reference inputs are validated before generation.
- A local rights-safe CosyVoice3 adapter exists as a Mandarin/multilingual quality upgrade; model/runtime provisioning remains operator-owned and reference voice audio requires explicit rights provenance.
- Qwen3-TTS 0.6B Base is recorded as a high-priority Apache-2.0 local benchmark candidate; voice-clone capability remains rights-gated.
- The reviewed candidate registry tracks materially relevant zero-cost/operator candidates including SCAIL-2, LongCat-Video-Avatar, WanGP, MiniMax H3 and Qwen3-TTS with code-vs-weights license separation and runtime gates.

The software3d route is the guaranteed zero-cost real-motion baseline/fallback, **not** the cinematic quality ceiling. Reference-conditioned model backends must beat it on identity stability, motion, visual quality or production efficiency while preserving rights, cost and failure-safety gates.

## Autonomous governance / ecosystem radar

`PROJECT.md` is canonical. `docs/operations/autonomous-ecosystem-radar.md` and `docs/operations/ecosystem-radar-policy.md` record the operating mechanics:

- routine reversible research/design/code/tests/docs/CI/PR decisions proceed autonomously instead of waiting for repetitive approval;
- when the current run can safely continue, it continues through the next highest-value action rather than stopping at a loop/CI/sub-step boundary;
- durable better direction is written back into `PROJECT.md` and relevant skills/specs in the same workstream;
- every production cycle performs a targeted fresh upstream check against the active measured Hottop gap;
- candidates pass source, **code + weights/data license**, cost, hardware, security/install, measurable-value and rollback gates before integration;
- useful upstream capability is integrated through the narrowest safe adapter/config/test/benchmark rather than left as research notes;
- only destructive/irreversible, secret/credential, paid, legal or sensitive-publication boundaries stop for explicit operator action.

The hourly automation is synchronized to the same policy. Interactive work continues immediately between scheduled runs; the hourly task is persistence/recovery, not a reason to stop current work.

## Durable motion contract

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg → final media verification`

Default unattended target is zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never turn into paid credits or a hidden paid provider. `video-run` is dry-run by default and only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity are never optional.

## Current ecosystem priorities

1. **Identity / reference-conditioned cinematic video:** benchmark only candidates whose exact code and weights terms permit the intended use. WanGP's current reference/continuation route is the practical operator path; SCAIL-2 and LongCat remain high-interest benchmarks; H3 remains license-gated/operator-approved rather than an unattended default.
2. **Mandarin dialogue quality:** benchmark CosyVoice3/Qwen3-TTS or a materially stronger safe local runtime against eSpeak for intelligibility, prosody, runtime cost and integration complexity. Voice cloning/reference audio remains rights-gated.
3. **Cinematic style proof:** run the lower-roughness Odyssey witch/pigs source through a complete reproducible production path so style routing is proven beyond Anti-Polish.
4. **Production evidence:** prefer actual config→moving shots→audio→composite→verified MP4 evidence over accumulating unbenchmarked provider abstractions.

## Immediate next actions

1. Merge PR #12 after exact-head integration checks prove the latest `main` governance + production-smoke tree together.
2. Use the successful software3d full-pipeline run as the deterministic benchmark, not the visual target; add a rights-safe reference/last-frame continuity benchmark for WanGP/free GPU candidates.
3. Wire the best reviewed local TTS path into the standard audio backend only when it preserves explicit voice-rights and no-auto-download boundaries; benchmark it against eSpeak.
4. Produce a second full-pipeline cinematic-meme case from the original Odyssey witch/pigs source.
5. Continue targeted upstream scans while implementing and integrate only material improvements that clear the admission gate.
