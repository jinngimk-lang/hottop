# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — inspect and improve real output quality; obtain generated identity evidence when operator runtime exists**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current verified runtime `main`: `5d903327cb87f757310ef53a4562a76aa0d35b3f` (`Keep MoviePy captions inside vertical safe area (#45)`).

Post-merge verification:

- main CI **1499** passed on Python 3.11 and 3.12;
- main production-smoke **81** passed both complete cow and Odyssey config → moving shots → Mandarin dialogue/music/SFX → MoviePy → FFmpeg → final media/provenance paths;
- PR #45 exact-head CI **1498** and production-smoke **80** were green before merge;
- production-smoke 80 artifact was downloaded and directly compared with smoke 78: Odyssey's long Mandarin caption that previously lost its lower lines is now fully visible, while short captions remain bottom anchored.

## Real artifact-level closures from this production cycle

### CJK/Mandarin subtitle readability and layout

Direct artifact inspection has now closed two separate subtitle defects that ordinary codec/media verification could not detect:

1. **Glyph coverage:** an earlier production-smoke artifact rendered Mandarin as tofu boxes. PR #37 made CJK caption-font resolution fail closed instead of silently using a non-CJK fallback. Normal `video-run` still does not auto-install fonts; CI explicitly provisions reviewed Noto CJK fonts.
2. **Vertical safe area:** production-smoke 78 rendered correct Chinese glyphs but MoviePy placed every caption at a fixed `0.78 * frame_height`; long multi-line Odyssey captions extended below the frame. PR #45 now bottom-anchors captions from the actual rendered `TextClip.h` using `max(24px, 6% frame height)` safe margin and clamps extremely tall captions to the top.

Evidence for the safe-area fix:

- CI **1496 RED** established the missing layout helper contract;
- CI **1497** exposed an incorrect new test assumption without weakening production code;
- exact-head CI **1498 GREEN** + production-smoke **80 GREEN**;
- direct old-vs-new artifact frame inspection confirmed the previously clipped three-line Odyssey caption is fully visible after the fix;
- post-merge main CI **1499 GREEN** + production-smoke **81 GREEN**.

### Deterministic software3d story identity

The same artifact-inspection loop previously found a more serious semantic defect: Odyssey subtitles/timing were correct, but the visual world was still the cow/workroom scene. That path is now fail closed:

- PR #39 fixed shot-mode story lookup to read the **output workspace** `hottop-video-plan.json`, not process cwd;
- smoke 66 artifact inspection confirmed cow and Odyssey now render materially distinct worlds;
- PR #40 made a missing workspace plan fail closed;
- PR #43 removed the final blank/unknown-topic-to-cow fallback.

The guaranteed deterministic baseline is now **story-explicit**: unsupported stories fail instead of silently reusing a historical template merely to emit a playable MP4.

## Guaranteed zero-cost baseline

The checked-in software3d baseline now has reproducible production proof for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- Mandarin dialogue + readable, safe-area-bounded CJK subtitles;
- original synthetic music + procedural Foley/SFX;
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

- **LightX2V** remains the primary Apache-2.0 operator inference framework. The tested Hottop integration pin remains `926299962ed32a142411e45468a289623432b4e4`. A freshness check in this cycle still observed upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018`; the newer change does not materially improve the tested Wan2.2 CLI path, so there is no evidence-backed reason to auto-repin.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- **Qwen3-TTS CustomVoice / CosyVoice** remain operator-owned Mandarin quality candidates. No current evidence justifies replacing the admission posture or auto-installing/downloading models.
- DINOv3, DreamSim and WanGP remain gated by their respective weights/license/runtime boundaries.

Durable rule: code license != model/weights/data license; popularity/freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and fix visible/story/audio failures before adding provider abstraction; workflow success alone is not sufficient quality evidence.
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
