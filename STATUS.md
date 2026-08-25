# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — obtain real reference-conditioned continuity evidence**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current `main`: `e1f9e5cd67aae42b44d60cb073f17df0e39af81f` (`Bind continuity benchmarks to generator provenance (#33)`).

Post-merge verification is complete:

- main CI run **1456** passed;
- main production-smoke run **58** passed;
- production-smoke again executed both checked-in cow and Odyssey software3d stories through config → real moving shots → Mandarin dialogue/music/SFX → MoviePy → FFmpeg → final media/provenance verification and uploaded reproducible evidence.

The guaranteed zero-cost software3d production baseline remains healthy without GPU/model download/credits.

## Completed continuity/provenance integrity

Production v0.2 reference-continuity evidence now fails closed on:

1. exact planned reference bytes;
2. shot bytes bound to plan shots carrying the same `reference.subject_id`;
3. complete coverage of every subject-bearing plan shot for each evaluated subject;
4. generated-artifact candidate/source provenance for LightX2V continuity evidence;
5. explicit evaluator identity/revision and thresholds.

PR #33 added the generator-attribution layer after two TDD cycles:

- CI **1448** RED: byte-valid LightX2V artifacts could be relabelled as another candidate revision;
- CI **1450** found a legacy JSON compatibility regression from optional `null` fields; absent provenance fields now remain omitted;
- CI **1451** GREEN: benchmark↔artifact candidate/revision binding;
- CI **1452** RED: real LightX2V artifact writer lacked candidate/source provenance;
- CI **1453** GREEN: LightX2V writer records actual local source revision;
- final PR exact-head CI **1455** + production-smoke **57** passed before merge;
- post-merge main CI **1456** + production-smoke **58** passed.

For LightX2V, `candidate_revision` means **actual local generator source revision**: git HEAD for a real checkout, otherwise `source-sha256:<sha256(lightx2v/infer.py)>` for packaged/non-git local code. A reviewed registry pin is not substituted for the code actually executed.

**Generator source revision, model/checkpoint revision, evaluator revision and artifact bytes are separate provenance dimensions.** Hottop does not infer model/weights revision from framework source revision; model provenance is bound only when independently verifiable local model metadata exists.

Benchmark scope remains explicit: incidental/single-shot subjects are not automatically forced into cross-shot evaluation merely because they carry `subject_id`.

## Current measured gap

The remaining identity gap is now genuinely **real generated-output evidence** from an operator-owned reference-conditioned route.

This execution environment still does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

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

- **LightX2V** remains the primary Apache-2.0 operator inference framework. Hottop's tested integration pin remains `926299962ed32a142411e45468a289623432b4e4`; a 2026-08-25 freshness check observed upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018`, but the newer SwiftVR-specific fix does not justify an automatic re-pin of the tested Wan2.2 route.
- **SigLIP 2 Base 256** remains the preferred first operator-local evaluator experiment; explicit local path only, with no implicit model download.
- **SigLIP v1 Base 256** is a lower-footprint Apache-2.0 control/fallback candidate, not preferred unless benchmark separation proves sufficient.
- **DINOv3** remains operator-owned/local-only because code + released weights use the custom DINOv3 License and pretrained access requires upstream acceptance.
- **DreamSim** remains gated because MIT code does not establish the downloaded weights/backbone rights/runtime boundary.
- **WanGP** remains operator-owned under community-license restrictions; do not vendor or auto-provision it.

Durable rule remains: **code license != model/weights/data license**. Popularity/freshness alone is not an admission reason.

## Immediate next actions

1. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets are actually present, execute the real multi-shot identity benchmark before making an identity-preservation claim.
2. Prefer SigLIP 2 Base 256 for the first model-based evaluator experiment only after explicit local weights are supplied; pin exact revision/hash, use no implicit download, and require same-subject vs identity-drift control separation.
3. Record model/checkpoint provenance independently from generator source revision when the operator can prove it locally; do not invent a weights pin from framework metadata.
4. Continue guaranteed software3d cow/Odyssey production proof and fresh-hotspot/product-mechanism production independently of optional GPU availability.
5. Continue Mandarin dialogue quality benchmarking through reviewed operator-owned local Qwen3-TTS/CosyVoice routes when local runtimes/models are supplied; eSpeak remains the guaranteed fallback.
6. Continue targeted ecosystem scans against the measured gap and integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform the targeted ecosystem scan relevant to the measured gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
