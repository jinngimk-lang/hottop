# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Latest production-code `main` at this snapshot: `ae62a5a6583956650fbf8454f9980590289c60a5` (`Prefer native eSpeak-NG in runtime fallback`, squash merge of PR #66).

Verified exact-head evidence:

- PR #62 closed the mixed CJK/Latin orphan-line defect; its production artifact was directly inspected and `用 InkClawAgent。` remained on one line in the lower safe area;
- later Production v0.2 work preserved the dialogue/BGM ducking, actual-voice-duration windows, clipping fail-close, mobile framing and subtitle contracts;
- PR #65 restored both cow and Odyssey provenance archives in production smoke after a workflow regression;
- PR #66 made normal runtime readiness/execution prefer native `espeak-ng` when available while retaining `espeak` compatibility as the guaranteed local fallback family;
- exact-head `ae62a5a6583956650fbf8454f9980590289c60a5`: CI **1605** passed and production-smoke **150** passed.

`docs/decisions/2026-08-26-mobile-subject-readability.md` records the durable portrait-readability rule, covering subject placement, readable subject scale, subtitle block occupancy and line-break quality.

## Guaranteed zero-cost software3d baseline

The checked-in software3d route has reproducible production evidence for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow output;
- mobile-first portrait placement, readable subject scale, bounded subtitle-block occupancy and non-orphaned short mixed-script captions;
- adaptive full-copy caption fitting with a readable font floor, CJK local-font fail-closed behavior and bottom safe-area anchoring;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- role-aware dialogue metadata (`speaker` + `delivery`) preserved into `hottop.video-plan.v1`;
- Mandarin dialogue using the guaranteed local eSpeak family, preferring native eSpeak-NG when installed;
- original synthetic music and procedural Foley/SFX;
- executed dialogue-aware BGM ducking, actual-voice-duration duck windows and fail-closed materially clipped dialogue;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- both cow and Odyssey provenance archives retained by production smoke;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic quality ceiling.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains integrated as an explicit non-default local route without replacing the guaranteed eSpeak-family fallback:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- native eSpeak-NG is preferred when present; legacy `espeak` remains compatible as the deterministic local fallback.

Capability boundary: current official 0.6B CustomVoice code discards `instruct`; the Production role-aware route therefore requires an instruct-capable checkpoint such as the current 1.7B path when delivery control is requested. Preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Mobile-first readability closure

Production evidence has closed four independent portrait-readability defects:

1. principal subjects were too low in frame;
2. key Odyssey characters remained too small after placement was corrected;
3. long Odyssey subtitles were technically inside the bottom safe area but occupied more than one fifth of the portrait canvas and competed with the subject;
4. the short mixed CJK/Latin cow caption `用 InkClawAgent。` passed safe-area/block-height gates but generic wrapping created a one-character first line.

MoviePy now preserves full semantic copy, resolves a real local CJK-capable font, fits long copy within the measured mobile height budget and prefers natural-width single-line layout for short mixed-script captions. If the single line is only slightly too wide, it shrinks within the existing readable font floor before wrapped-caption fallback.

Decision record: `docs/decisions/2026-08-26-mobile-subject-readability.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Fresh public checks on 2026-08-26 continue to show active upstream work around InfiniteTalk and MiniMax-H3-related requests/configuration, but no Hottop measurement justifies freshness-driven repinning of the tested Wan2.2 route.
- **MiniMax H3 via LightX2V** is visibly active upstream, but model/weights/output-rights, hardware, benchmark and local-provisioning gates remain uncleared. It stays an operator benchmark candidate, not an unattended default.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate. Real quality comparison still requires an operator-provisioned local 1.7B runtime; third-party runtimes do not supersede the reviewed official adapter without independent license/runtime/quality evidence.
- **CosyVoice3 / cosyvoice.cpp** remain comparison candidates; no same-dialogue benchmark currently supports replacing Qwen/eSpeak routing.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk and other candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code.
2. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak-NG/eSpeak vs Qwen benchmark using checked-in roles/deliveries; do not claim quality improvement before real audio evidence.
3. When a compliant operator-owned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V or WanGP reference-conditioned runtime + rights-safe assets exist, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
4. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
5. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
6. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
