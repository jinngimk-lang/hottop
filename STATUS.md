# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — improve real output quality before stronger generated routes**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Recovered `main` before the active PR: `f393b76032fb5f666375e1cd488adca7c00f9073` (`Fix CJK caption font routing (#37)`).

PR #37 is merged and fully post-merge verified:

- implementation CI **1467** GREEN on Python 3.11/3.12;
- production-smoke **60** GREEN and downloaded artifact manually verified CJK glyphs;
- final PR exact-head CI **1469** + production-smoke **62** GREEN;
- post-merge main CI **1470** + production-smoke **63** GREEN.

Mandarin/CJK captions now fail closed when no real local CJK-capable font is available; normal `video-run` does not auto-install fonts.

## Software3d story-routing closure

Artifact-level inspection of production-smoke 60 found a second real defect: Odyssey carried Odyssey captions/timing but rendered the cow/workroom software3d world. Root cause was shot mode resolving `cwd/hottop-video-plan.json`; `video-run` launches software3d from project root, so the workspace plan was absent and the old resolver silently fell back to cow.

Active PR **#38 — Fail closed on software3d story routing** fixes that production bug without GPU/model/network dependencies:

- CI **1471** RED: no public fail-closed `story_profile_for_topic` contract;
- supported topic/profile mapping is explicit for the checked-in cow and Odyssey stories;
- unknown/blank software3d topics now fail instead of silently becoming cow;
- shot mode resolves story identity from the output workspace's `hottop-video-plan.json`, independent of current working directory;
- direct library fixtures may explicitly pass a supported `story_profile`;
- CI **1475** exposed one legacy provenance fixture that had omitted all story semantics; it was corrected to explicitly declare cow rather than weakening the production boundary;
- exact-head CI **1477** GREEN on Python 3.11/3.12;
- production-smoke **66** GREEN for both full cow and Odyssey pipelines;
- downloaded smoke-66 artifact was manually inspected: cow remains the cow/workroom world, while Odyssey now renders a materially distinct banquet-hall ensemble/witch/transformation world with no `young-cow-body` visual reuse.

This upgrades software3d from “two caption variants over one visual template” to two honest deterministic visual production proofs.

## Guaranteed zero-cost baseline

The software3d baseline now demonstrates, with real uploaded artifacts:

- story-specific moving 3D geometry for cow and Odyssey;
- Mandarin dialogue + readable CJK subtitles;
- original synthetic music + procedural Foley/SFX;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- byte-bound per-shot provenance and pre-composition re-verification;
- final media verification;
- no GPU, model download, credentials or paid service.

Deterministic fallback remains a guaranteed capability, not the cinematic quality ceiling.

## Completed continuity/provenance integrity

Production v0.2 reference-continuity evidence fails closed on:

1. exact planned reference bytes;
2. shot bytes bound to plan shots carrying the same `reference.subject_id`;
3. complete coverage of every subject-bearing plan shot for each evaluated subject;
4. generated-artifact candidate/source provenance for LightX2V continuity evidence;
5. explicit evaluator identity/revision and thresholds.

For LightX2V, `candidate_revision` means **actual local generator source revision**: git HEAD for a real checkout, otherwise `source-sha256:<sha256(lightx2v/infer.py)>` for packaged/non-git local code. A reviewed registry pin is not substituted for code actually executed.

**Generator source revision, model/checkpoint revision, evaluator revision and artifact bytes are separate provenance dimensions.** Hottop does not infer model/weights revision from framework source revision; model provenance is bound only when independently verifiable local model metadata exists.

Benchmark scope remains explicit: incidental/single-shot subjects are not automatically forced into cross-shot evaluation merely because they carry `subject_id`.

## Current generated-output identity gap

The remaining reference-identity gap still requires **real generated-output evidence** from an operator-owned reference-conditioned route.

This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires:

- at least two generated, byte-bound plan shots for the same rights-safe evaluated subject;
- exact planned local reference + stable `subject_id`;
- quality-gated generated artifacts;
- generator candidate + actual source revision bound to those bytes;
- independently verifiable model/checkpoint provenance when available;
- continuity evidence covering every subject-bearing plan shot for the evaluated subject;
- explicit evaluator identity/revision and fail-closed thresholds.

Until that runtime exists, structural benchmark work must not be mistaken for real visual-continuity evidence.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current posture:

- **LightX2V** remains the primary Apache-2.0 operator inference framework. Hottop's tested integration pin remains `926299962ed32a142411e45468a289623432b4e4`; a 2026-08-25 freshness check observed upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018`, but the SwiftVR-specific fix does not justify an automatic re-pin of the tested Wan2.2 route.
- **SigLIP 2 Base 256** remains the preferred first operator-local evaluator experiment; explicit local path only, with no implicit model download.
- **SigLIP v1 Base 256** is a lower-footprint Apache-2.0 control/fallback candidate, not preferred unless benchmark separation proves sufficient.
- **DINOv3** remains operator-owned/local-only because code + released weights use the custom DINOv3 License and pretrained access requires upstream acceptance.
- **DreamSim** remains gated because MIT code does not establish the downloaded weights/backbone rights/runtime boundary.
- **WanGP** remains operator-owned under community-license restrictions; do not vendor or auto-provision it.

Durable rule remains: **code license != model/weights/data license**. Popularity/freshness alone is not an admission reason.

## Immediate next actions

1. Finish PR #38 exact-head doctrine/status CI, merge only with the already-green CI 1477 + production-smoke 66 evidence, then verify post-merge main CI/smoke.
2. Continue output-quality inspection of the guaranteed baseline rather than trusting workflow success alone; prioritize visible/story/audio defects over additional provider abstraction.
3. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets are actually present, execute the real multi-shot identity benchmark before making an identity-preservation claim.
4. Prefer SigLIP 2 Base 256 for the first model-based evaluator experiment only after explicit local weights are supplied; pin exact revision/hash, use no implicit download, and require same-subject vs identity-drift control separation.
5. Continue Mandarin dialogue quality benchmarking through reviewed operator-owned local Qwen3-TTS/CosyVoice routes when local runtimes/models are supplied; eSpeak remains the guaranteed fallback.
6. Continue targeted ecosystem scans against measured gaps and integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform the targeted ecosystem scan relevant to the measured gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
