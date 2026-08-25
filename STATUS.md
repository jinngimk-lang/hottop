# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — inspect and improve real output quality; obtain generated identity evidence when operator runtime exists**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current verified runtime `main`: `4602b70cf0fa76c3e1bb5011a0281bffd7adb68c` (`Improve cinematic Odyssey lighting (#49)`).

Post-merge verification:

- main CI **1510** passed on Python 3.11 and 3.12;
- main production-smoke **87** passed both complete cow and Odyssey config → moving shots → Mandarin dialogue/music/SFX → MoviePy → FFmpeg → final media/provenance paths;
- PR #49 exact-head CI **1509** and production-smoke **86** were green before merge;
- PR #48 exact-head CI **1506** and production-smoke **84** were green before merge; post-merge CI **1507** and production-smoke **85** also passed.

## Real artifact-level closures from this production cycle

### Final audio presence and duration

Final output verification now rejects two false-positive classes that codec-only inspection could miss:

1. **Silent AAC:** final AAC must contain measurable audible signal; an encoded silent track does not satisfy the audio contract.
2. **Truncated audio:** the AAC stream must cover the full final video duration within a conservative **0.25 s** codec/container skew tolerance. A short audible blip cannot make a ten-second video pass.

Direct production-smoke 84 inspection confirmed the normal baseline is not being rejected accidentally: both cow and Odyssey final videos are 10 s with ~10.008 s AAC streams, and a `-50 dB / 0.5 s` silence scan found no long silent interval.

### Cinematic Odyssey visual separation

Direct production-smoke 84 frame inspection found a style-routing defect that CI/media verification could not see: the lower-roughness Odyssey software3d baseline was darker/flatter than the deliberate Anti-Polish cow scene, weakening subject/environment separation.

PR #49 fixed only the Odyssey story palette. It did not change the cow baseline, provider routing, generation policy or media contracts.

Evidence:

- CI **1508 RED** established a deterministic style-routing contract: Odyssey background and hall-wall luminance must exceed the Anti-Polish cow scene by a measurable margin;
- exact-head CI **1509 GREEN** + production-smoke **86 GREEN**;
- direct smoke 86 artifact inspection at 1/3/5/7/9 s showed sampled Odyssey mean grayscale luminance rise from roughly **29.5–32.4** in smoke 84 to **45.9–48.3**, with visibly clearer subject/environment separation and captions still readable;
- post-merge main CI **1510 GREEN** + production-smoke **87 GREEN**.

This is a deterministic style-routing baseline improvement, not a claim that software3d is the cinematic quality ceiling.

### CJK/Mandarin subtitle readability and layout

Earlier artifact inspection closed two independent subtitle defects:

- **Glyph coverage:** CJK font resolution fails closed rather than silently rendering tofu boxes. Normal `video-run` does not auto-install fonts; CI explicitly provisions reviewed Noto CJK fonts.
- **Vertical safe area:** MoviePy bottom-anchors captions from actual rendered `TextClip.h`, with a safe lower margin and clamping for unusually tall captions, so long Mandarin subtitles remain fully visible.

### Deterministic software3d story identity

The deterministic baseline is story-explicit: cow and Odyssey route to distinct story worlds from the workspace plan, and missing/unknown topics fail closed instead of silently falling back to a historical cow template merely to emit a playable MP4.

## Guaranteed zero-cost baseline

The checked-in software3d route now has reproducible production proof for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- style-routed presentation: deliberate Anti-Polish cow vs brighter lower-roughness Odyssey baseline;
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

A production identity-preservation claim requires:

- at least two generated, byte-bound plan shots for the same rights-safe evaluated subject;
- exact planned local reference + stable `subject_id`;
- generated-video quality gates;
- generator candidate + actual local source revision bound to those bytes;
- independently verifiable model/checkpoint provenance when available;
- continuity evidence covering every subject-bearing plan shot for the evaluated subject;
- explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

- **LightX2V** remains the primary Apache-2.0 operator inference framework. The tested Hottop integration pin remains `926299962ed32a142411e45468a289623432b4e4`. A fresh check on 2026-08-25 observed upstream `main` still at `5dc5d6372654406761474719647763ac7b4bd018` (`fix(swiftvr): convert BF16 images before NumPy export (#1429)`); this does not materially improve Hottop's tested Wan2.2 CLI path, so there is no evidence-backed reason to repin.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- **Qwen3-TTS CustomVoice / CosyVoice** remain operator-owned Mandarin quality candidates. `cosyvoice.cpp` v0.1.1 is a lightweight runtime candidate but still requires matching GGML/ICU/runtime assets and has reported prebuilt CUDA noise caveats; there is no evidence-backed reason to replace the current admission posture or auto-install it.
- DINOv3, DreamSim and WanGP remain gated by their respective weights/license/runtime boundaries.

Durable rule: code license != model/weights/data license; popularity/freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs. Quantify the next visible deterministic gap before changing code; current Odyssey frames suggest composition/framing occupancy is a stronger candidate than further palette adjustment.
2. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets actually exist, execute the real multi-shot identity benchmark before claiming identity preservation.
3. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
4. Continue Mandarin dialogue quality benchmarking through reviewed local Qwen3-TTS/CosyVoice routes when runtimes/models are supplied; eSpeak remains the guaranteed fallback.
5. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
6. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
