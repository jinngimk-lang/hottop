# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — real output quality + reference-conditioned evidence**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current recovered main

Current base before active PR #41: `27db1a009a5e1d0813bbfcb7bc3a22b6d3df03a5` (`Fix software3d story routing in production workspace (#39)`).

Recent merged runtime evidence:

- PR #37 CJK subtitle fix: post-merge main CI **1470** + production-smoke **63** GREEN; downloaded prior smoke artifacts were visually inspected and Mandarin subtitles render as real glyphs instead of tofu.
- PR #39 workspace story routing: exact-head CI **1478** + production-smoke **67** GREEN; it fixed the observed runtime bug where software3d shot mode looked in process cwd rather than the output workspace for `hottop-video-plan.json`.
- Independent smoke **66** artifact from the stricter parallel line was downloaded and visually inspected: cow remains the cow/workroom world, while Odyssey renders a materially distinct banquet-hall / witch / pig-transformation world. The two checked-in examples are no longer caption-only variants of one visual template.

## Active PR #41 — remove residual implicit-cow fallbacks

PR #39 fixed normal workspace routing, but two permissive branches remained on main: a missing workspace plan returned cow, and an unknown topic returned cow. A future unsupported deterministic story could therefore still produce a technically valid but semantically false cow MP4.

PR #41 (`Reject unsupported software3d story fallbacks`) makes that boundary fail closed:

- CI **1482 RED**: strict public story resolver absent;
- implementation introduces explicit known topic mapping and rejects blank/unknown topics;
- missing workspace plan now fails instead of defaulting cow;
- legacy unit fixtures were updated to provide explicit cow workspace semantics rather than weakening production behavior;
- the old test that required `unknown → cow` was replaced with a fail-closed contract;
- exact code-head CI **1489** GREEN on Python 3.11 and 3.12;
- code-head production-smoke **75** GREEN for both full cow and Odyssey pipelines;
- no GPU, model, network, credential or paid dependency was added.

`PROJECT.md` now records the durable rule: deterministic fallback is story-explicit. Missing/unknown/unsupported stories must fail rather than silently reuse a historical template simply to emit a playable MP4.

## Guaranteed zero-cost baseline

The software3d baseline now has reproducible proof for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- Mandarin dialogue + readable CJK subtitles;
- original synthetic music + procedural Foley/SFX;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback and evidence baseline, not the cinematic quality ceiling.

## Generated/reference-conditioned identity gap

The remaining identity gap requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment still does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

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

- **LightX2V** remains the primary Apache-2.0 operator inference framework. Tested Hottop pin remains `926299962ed32a142411e45468a289623432b4e4`; a fresh 2026-08-25 check still found no upstream change that justifies automatically replacing the tested Wan2.2 pin for the current gap.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights/revision are supplied; no implicit download.
- **Qwen3-TTS CustomVoice / CosyVoice** remain operator-owned Mandarin quality candidates. Fresh checks found CosyVoice demo availability issues but no evidence that changes Hottop's existing admission posture or justifies auto-install/model download.
- DINOv3/DreamSim/WanGP remain gated by their respective weights/license/runtime boundaries.

Durable rule: code license != model/weights/data license; popularity/freshness alone is not admission evidence.

## Immediate next actions

1. Merge PR #41 only after final docs exact-head CI remains green; post-merge verify main CI + production-smoke.
2. Continue direct output inspection of the guaranteed software3d artifacts and fix visible/story/audio failures before adding provider abstractions.
3. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets actually exist, execute the real multi-shot identity benchmark before claiming identity preservation.
4. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
5. Continue Mandarin dialogue quality benchmarking through reviewed local Qwen3-TTS/CosyVoice routes when runtimes/models are supplied; eSpeak remains guaranteed fallback.
6. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
