# Hottop Status

Last updated: 2026-08-25
Active branch: `prod/autonomous-radar-governance`
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Foundation PR #1 is merged. Production v0.2 is active and the repository now has a real zero-cost deterministic motion baseline plus optional free/operator-owned generative routes.

Closed in the current production pass:

- `software3d` is integrated into normal `video-run` execution. It renders actual 3D geometry/projection/animation, encodes per-shot MP4 through FFmpeg, and does not require Blender, a GPU or a model download.
- Software3d shots emit convention-bound `.artifact.json` sidecars with SHA-256 + byte size; MoviePy verifies byte identity before composition.
- A full software3d profile carries role-aware dialogue, original synthetic music and procedural SFX/Foley through the standard audio/composition/finalization path.
- ZeroGPU, WanGP and Comfy external boundaries remain quality/provenance gated and fail closed rather than silently using paid fallback.
- Cross-shot identity locks and rights-safe reference inputs are validated before generation.
- A local rights-safe CosyVoice3 adapter exists as a Mandarin/multilingual quality upgrade; model/runtime provisioning remains operator-owned and reference voice audio requires explicit rights provenance.
- Qwen3-TTS 0.6B Base is recorded as a high-priority Apache-2.0 local benchmark candidate; voice-clone capability remains rights-gated.
- The reviewed candidate registry now tracks materially relevant zero-cost/operator candidates including SCAIL-2, LongCat-Video-Avatar, WanGP, MiniMax H3 and Qwen3-TTS with code-vs-weights license separation and runtime gates.

## Current governance change

Branch `prod/autonomous-radar-governance` updates `PROJECT.md` so repository truth matches the operating mandate:

- routine reversible research/design/code/tests/docs/CI/PR decisions proceed autonomously rather than waiting for repetitive approval;
- durable direction changes are written back into `PROJECT.md` and relevant skills/specs in the same workstream;
- every production cycle performs a targeted ecosystem freshness check for current Hottop gaps;
- candidates that pass source, code+weights license, cost, hardware, security, measured-value and rollback gates are integrated through a small adapter/config/test/benchmark instead of being left as research notes;
- only destructive/irreversible, secret/credential, paid, legal or sensitive-publication boundaries stop for explicit operator action;
- `PROJECT.md` now correctly records Production v0.2 as the current milestone rather than the completed Foundation milestone.

The hourly automation has been synchronized to the same Production + Ecosystem Radar policy. Interactive work continues immediately between scheduled runs; the hourly task is persistence/recovery, not a reason to stop current work.

## Durable motion contract

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg → final media verification`

Default unattended target is zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never turn into paid credits or a hidden paid provider. `video-run` is dry-run by default and only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity are never optional.

## Current ecosystem priorities

1. **Identity / reference-conditioned cinematic video:** benchmark only candidates whose code and weights terms permit the intended use. SCAIL-2 and LongCat remain high-interest; H3 remains license-gated/operator-approved rather than an unattended default.
2. **Low-cost local execution:** continue using WanGP as operator interop rather than vendoring it; track upstream capability changes without binding Hottop core schema to a model release.
3. **Mandarin dialogue quality:** benchmark CosyVoice3/Qwen3-TTS or a materially stronger safe local runtime against eSpeak for intelligibility, prosody, runtime cost and integration complexity.
4. **Production evidence:** prefer actual config→moving shots→audio→composite→verified MP4 evidence over accumulating additional unbenchmarked provider abstractions.

## Immediate next actions

1. Verify the autonomy/radar branch on exact-head CI, open a focused PR, and merge when green/no review blocker.
2. Continue Production v0.2 immediately after merge: run/strengthen the full software3d config→MP4 baseline and archive reproducible final-media/provenance evidence.
3. Wire the best reviewed local TTS path into the standard video audio backend only when it preserves explicit voice-rights and no-auto-download boundaries; benchmark it against the current fallback.
4. Continue targeted upstream scans while implementing; integrate only material improvements that clear the admission gate.
