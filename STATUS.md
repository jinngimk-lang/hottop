# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; obtain generated identity evidence when operator runtime exists**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current runtime `main`: `d902c78433f329e41ebc8d79fe8b5f74d7c41c52` (`prod: improve Odyssey mobile subject scale`, squash merge of PR #53).

Verified pre-merge evidence for PR #53:

- RED CI **1539**: Ruff passed; pytest isolated the subject-scale contract at exactly **1 failed / 458 passed**, with Odyssey shot-4 hero measuring `0.128614250658297` of portrait frame height vs the `>=0.14` test contract;
- GREEN exact-head `ac2cc7ca56bab490833d08db1ab91f7895a4f535` CI **1540** passed on Python 3.11 and 3.12;
- production-smoke **106** passed the real cow + Odyssey config → moving shots → Mandarin dialogue/music/SFX → MoviePy → FFmpeg → final media/provenance path;
- direct inspection of the #106 Odyssey MP4 confirmed visibly larger key characters without subtitle clipping or broken scene geography.

Post-merge main CI **1541** and production-smoke **107** were running at the last fetch and must be re-fetched before claiming the merge commit green.

## Real artifact-level closures from this production cycle

### Perceptible deterministic motion

Direct artifact inspection showed that a playable MP4 can still read as nearly static. The guaranteed software3d baseline now has deterministic pixel-motion and camera-motion contracts. Cow uses deliberate Anti-Polish pan/dolly movement; Odyssey uses controlled cinematic pan/crane/dolly/zoom motion. The motion gate is style-routed and does not redefine random failure as roughness.

### Mobile-first vertical framing and subject readability

Production-smoke artifact inspection exposed two distinct 9:16 framing defects:

1. **Placement:** narrative subjects sat too low, leaving a persistent empty upper region. PR #52 moved the portrait projection principal point to 42% of frame height while preserving landscape projection and subtitle-safe lower space.
2. **Readable scale:** after placement passed, production-smoke #105 still showed the Odyssey key characters substantially smaller than the cow flagship. Cow read at roughly 21% of portrait frame height at midpoint; Odyssey key people were typically around 12–15%. PR #53 keeps landscape focal behavior unchanged and raises only Odyssey portrait focal scale from `0.98` to `1.10`. The backend-specific test requires the designated primary Odyssey character to occupy at least 14% of the 360×640 portrait frame at midpoint.

Durable rule: mobile-first framing must inspect both **where the subject sits** and **whether the principal subject is large enough to decode on a phone**. Numeric scale thresholds remain style/backend/story specific rather than universal.

Decision record: `docs/decisions/2026-08-26-mobile-subject-readability.md`.

### Final audio presence and duration

Final output verification rejects two false-positive classes that codec-only inspection could miss:

1. **Silent AAC:** final AAC must contain measurable audible signal.
2. **Truncated audio:** AAC must cover the full final video duration within a conservative **0.25 s** codec/container skew tolerance.

Production evidence confirmed both cow and Odyssey ten-second outputs carry roughly 10.008 s AAC and no long >=0.5 s silence interval at the checked threshold.

### Cinematic Odyssey visual separation

Direct artifact inspection found the lower-roughness Odyssey software3d baseline darker/flatter than the deliberate Anti-Polish cow scene. The Odyssey-only palette correction raised sampled mean grayscale luminance from roughly **29.5–32.4** to **45.9–48.3**, improving subject/environment separation without changing the cow baseline, provider routing or media contracts.

This is a deterministic style-routing baseline improvement, not a claim that software3d is the cinematic quality ceiling.

### CJK/Mandarin subtitle readability and layout

- **Glyph coverage:** CJK font resolution fails closed rather than silently rendering tofu boxes. Normal `video-run` does not auto-install fonts; CI explicitly provisions reviewed Noto CJK fonts.
- **Vertical safe area:** MoviePy bottom-anchors captions from actual rendered `TextClip.h`, with a safe lower margin and clamping for unusually tall captions.

### Deterministic software3d story identity

The deterministic baseline is story-explicit: cow and Odyssey route to distinct story worlds from the workspace plan, and missing/unknown topics fail closed instead of silently falling back to a historical template merely to emit a playable MP4.

## Guaranteed zero-cost baseline

The checked-in software3d route now has reproducible production proof for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow-like output;
- mobile-first portrait placement **and principal-subject readability**;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- Mandarin dialogue + readable, safe-area-bounded CJK subtitles;
- original synthetic music + procedural Foley/SFX;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic quality ceiling.

## Generated/reference-conditioned identity gap

The remaining identity gap still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

- **LightX2V** remains the primary Apache-2.0 operator inference framework. The tested Hottop integration pin remains `926299962ed32a142411e45468a289623432b4e4`. Fresh public activity remains concentrated around InfiniteTalk maintenance and requests for newer models such as MiniMax H3; no observed change materially improves Hottop's tested Wan2.2 local CLI contract enough to justify an unbenchmarked repin.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- **Qwen3-TTS CustomVoice / CosyVoice** remain operator-owned Mandarin quality candidates. No current evidence justifies changing the guaranteed eSpeak fallback or auto-provisioning models.
- DINOv3, DreamSim and WanGP remain gated by their respective weights/license/runtime boundaries.

Durable rule: code license != model/weights/data license; popularity/freshness alone is not admission evidence.

## Immediate next actions

1. Re-fetch post-merge `main` CI **1541** and production-smoke **107** for `d902c784…`; repair immediately if either fails.
2. Continue **direct artifact inspection** of the now motion-, placement-, and subject-scale-gated software3d outputs. Quantify the next visible deterministic gap before changing code.
3. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets exist, execute the real multi-shot identity benchmark before claiming identity preservation.
4. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
5. Continue Mandarin dialogue quality benchmarking through reviewed local Qwen3-TTS/CosyVoice routes when runtimes/models are supplied; eSpeak remains the guaranteed fallback.
6. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
7. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
