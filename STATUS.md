# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — require complete continuity coverage for evaluated subjects**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current deployed `main`: `eac3beed84f9a9481c3ee9b7e9716803ef9bcdc9` (`Production v0.2: bind continuity evidence to subject shots (#30)`).

Post-merge evidence for #30 is complete:

- main CI run **1437** passed;
- automatically triggered main-push production-smoke run **43** passed;
- the production smoke preserved the #29 evidence-lifecycle guarantee by rerunning the real checked-in software3d production proof after the continuity verifier reached `main`.

The deployed continuity verifier now binds each evaluated subject to the planned reference path and to exact byte-bound artifacts from `VideoShot.reference.subject_id`, so another subject's valid manifest hashes cannot be reassigned as evidence.

Recent deployed milestones:

- PR #23 — fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #28 — output-side identity evidence and exact-byte continuity binding, merged as `3fd869a93b8fc651cc3f2e624767c13498076de7`.
- PR #29 — post-merge `main` production evidence, merged as `fb3c8dea92591f8872cd5fc89197a2b8fd914cd3`.
- PR #30 — subject→planned-reference→subject-shot continuity binding, merged as `eac3beed84f9a9481c3ee9b7e9716803ef9bcdc9`.

## Active workstream — PR #31

Draft PR #31, **Production v0.2: require complete continuity shot coverage**, closes a cherry-picking gap left after #30.

After #30, a subject could no longer claim another subject's shot bytes, but it could still report only a subset of its own valid subject-bearing shots. A three-shot route could therefore score only its two best-looking shots and omit the identity-drift failure.

TDD / implementation evidence:

- RED head `1db89ed69744d7f1cd727d359393376e219bc008`: CI run **1438** reached pytest with Ruff green and failed on the new three-shot counterexample.
- GREEN implementation `55614a0542850cd95883e7530b324e9bfc87abc6`: an evaluated subject's evidence hashes must now equal the full set of byte-bound artifacts for all plan shots carrying that `subject_id`; foreign hashes and omitted subject shots both fail closed.
- exact-head CI run **1439** passed.
- a broader idea to force every plan subject into the benchmark was explicitly rejected: single-shot/background subjects may be outside cross-shot evaluation scope. Completeness is enforced **within each evaluated subject**, not by expanding benchmark scope implicitly.
- current exact-head production-smoke should be re-fetched before merge; do not rely on the stale run number in this snapshot.

This remains provider-neutral and introduces no model, evaluator dependency, GPU requirement, network call or paid service.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current measured gap remains **real generated-output identity on operator-owned reference-conditioned runs**, not another provider abstraction.

Current evaluator admission posture:

- **SigLIP 2 Base 256** remains the preferred first operator-local evaluator experiment: Apache-2.0 model-card posture, roughly 1.54 GB repository / 1.5 GB main safetensors, but local-path-only because standard loading can download implicitly.
- **SigLIP 2 SO400M** remains a higher-capacity multi-GB fallback candidate, not the first experiment.
- **DINOv3** remains operator-owned/local-only because code + released weights use the custom DINOv3 License and pretrained access requires upstream acceptance.
- **DreamSim** remains gated because MIT code does not establish the rights/runtime boundary for the downloaded pretrained weights/backbones.
- **LightX2V** remains the primary Apache-2.0 operator inference framework; exact model/weights terms remain separate.
- **WanGP** remains operator-owned under its current community-license restrictions; fresh upstream releases continue to improve H3/LTX continuity/quality, but that does not change Hottop's license/runtime boundary or justify vendoring/auto-provisioning.

Durable rule remains: **code license != model/weights/data license**, and permissive code/model terms do not justify hidden multi-GB downloads in unattended Hottop.

## Immediate next actions

1. Finish PR #31 exact-head CI + production-smoke after the status/research sync; review final diff and merge only when both are green.
2. Verify post-merge main CI + automatically triggered main production-smoke again.
3. When operator-controlled LightX2V/Wan2.2 or compliant WanGP reference-conditioned assets are actually available, generate at least two byte-bound shots for the same rights-safe evaluated subject and serialize thresholded continuity evidence covering **all** of that subject's plan shots before claiming identity preservation.
4. Continue the guaranteed software3d baseline and a real fresh-hotspot + product-mechanism production path independently of optional GPU availability.
5. Continue targeted upstream scans against measured gaps; integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform the targeted ecosystem scan relevant to the measured gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
