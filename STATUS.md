# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — bind real reference-conditioned continuity evidence to generator provenance**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Recovery baseline `main`: `94e3e1d206c0372aeb3affb0213da62750fc3f76` (`Sync Production v0.2 continuity status (#32)`). Main CI run **1447** passed.

The guaranteed zero-cost production baseline remains healthy: checked-in cow and Odyssey software3d stories execute through real config → moving shots → Mandarin audio/music/SFX → MoviePy → FFmpeg → final media/provenance verification in production-smoke, without GPU/model download/credits.

Deployed reference-continuity verification already fails closed on:

1. exact planned reference bytes;
2. shot bytes bound to plan shots carrying the same `reference.subject_id`;
3. complete coverage of every subject-bearing plan shot for each evaluated subject.

Benchmark scope remains explicit; incidental or single-shot subjects are not forced into cross-shot evaluation merely because they carry a `subject_id`.

## Active candidate-provenance closure

Draft PR #33, **Bind continuity benchmarks to generator provenance**, closes the remaining attribution hole between generated artifacts and the benchmark's self-reported candidate/revision.

TDD evidence on the branch:

- CI run **1448**: RED. Ruff passed; pytest failed on the new contract proving byte-valid LightX2V artifacts could otherwise be relabelled as a different candidate revision.
- CI run **1450**: implementation found a backward-compatibility regression because optional provenance fields serialized as `null` into legacy deterministic artifact JSON. The JSON shape was preserved by omitting absent candidate fields.
- CI run **1451**: GREEN on Python 3.11 and 3.12 for benchmark↔artifact candidate/revision binding.
- CI run **1452**: RED. Ruff passed; pytest failed because the real LightX2V artifact writer did not yet emit candidate/source provenance.
- CI run **1453**: GREEN on Python 3.11 and 3.12 after LightX2V artifacts began recording `candidate_id` plus the actual local generator source revision.
- CI run **1454**: exact-head documentation-inclusive CI passed. Final production-smoke for the exact head must remain green before merge.

For LightX2V, `candidate_revision` now means **actual local generator source revision**, not a reviewed registry pin and not model weights revision. A git checkout records its actual HEAD; a packaged/non-git checkout records `source-sha256:<sha256(lightx2v/infer.py)>`. This prevents source-version relabelling without fabricating provenance.

Model/checkpoint provenance remains independent. Hottop must not infer weights revision from framework source revision; bind it only when an operator runtime exposes verifiable local model metadata.

## Current measured gap

After candidate/source provenance is merged, the remaining identity gap is **real generated-output evidence** from an operator-owned reference-conditioned route, plus independently verifiable model/checkpoint provenance where available.

This environment still does not contain an operator-provided LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended operation must not auto-download multi-GB models, provision a GPU, consume credits or weaken that boundary. The guaranteed software3d baseline remains fully usable and continuously smoke-tested.

A production identity claim requires:

- at least two generated, byte-bound plan shots for the same rights-safe evaluated subject;
- the exact planned local reference and stable `subject_id`;
- quality-gated shot artifacts and byte provenance;
- generator candidate + actual source revision bound to the evaluated artifacts;
- model/checkpoint provenance recorded separately when locally verifiable;
- continuity evidence covering every subject-bearing plan shot for that evaluated subject;
- explicit evaluator identity/revision and fail-closed thresholds.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current posture:

- **LightX2V** remains the primary Apache-2.0 operator inference framework. Hottop's tested integration pin remains `926299962ed32a142411e45468a289623432b4e4`; a 2026-08-25 freshness check observed upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018`, but the newer SwiftVR-specific fix does not justify an automatic re-pin of the tested Wan2.2 route.
- **SigLIP 2 Base 256** remains the preferred first operator-local evaluator experiment: official Apache-2.0 model-card posture and materially smaller than SO400M, but explicit local-path-only because standard loading can download implicitly.
- **SigLIP v1 Base 256** is a still-smaller Apache-2.0 control/fallback candidate for evaluator experiments, not a preferred evaluator unless benchmark separation proves sufficient.
- **DINOv3** remains operator-owned/local-only because code + released weights use the custom DINOv3 License and pretrained access requires upstream acceptance.
- **DreamSim** remains gated because MIT code does not establish the rights/runtime boundary for downloaded pretrained weights/backbones.
- **WanGP** remains operator-owned under its current community-license restrictions; do not vendor or auto-provision it.

Durable rule: **generator code revision, model/weights revision, evaluator revision and artifact bytes are separate provenance dimensions**. Code license also remains distinct from model/weights/data license.

## Immediate next actions

1. Finish PR #33 only after exact-head CI + production-smoke are green; merge with expected-head protection, then verify post-merge `main`.
2. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime and rights-safe assets are actually present, execute the real multi-shot identity benchmark before making an identity-preservation claim.
3. Prefer the reviewed SigLIP 2 Base 256 local-path route for the first model-based evaluator experiment only after explicit local weights are supplied; pin exact revision/hash, perform no implicit download, and require same-subject vs identity-drift control separation before admission.
4. Continue the guaranteed software3d cow/Odyssey production proof and fresh-hotspot + product-mechanism production independently of optional GPU availability.
5. Continue Mandarin dialogue quality benchmarking through reviewed operator-owned local Qwen3-TTS/CosyVoice routes when their local runtimes/models are supplied; eSpeak remains the guaranteed fallback.
6. Continue targeted upstream scans against measured gaps; integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform the targeted ecosystem scan relevant to the measured gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
