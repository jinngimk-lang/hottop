# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — bind continuity evidence to subject-bearing shots**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current deployed `main`: `fb3c8dea92591f8872cd5fc89197a2b8fd914cd3` (`Production v0.2: keep main production evidence green (#29)`).

Post-merge evidence for #29 is complete:

- main CI run **1427** passed;
- automatically triggered main-push production-smoke run **35** passed;
- the production smoke executed both checked-in cow and Odyssey software3d stories through real config → moving shots → Mandarin audio/music/SFX → MoviePy → FFmpeg → ffprobe/provenance verification and uploaded the reproducible evidence bundle.

The deployed chain now keeps this deterministic production proof green after relevant video-path changes reach `main`, rather than relying only on PR-time evidence.

Recent deployed milestones:

- PR #23 — fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #28 — output-side identity evidence and exact-byte continuity binding, merged as `3fd869a93b8fc651cc3f2e624767c13498076de7`.
- PR #29 — post-merge `main` production evidence, merged as `fb3c8dea92591f8872cd5fc89197a2b8fd914cd3`.

## Active workstream — PR #30

Draft PR #30, **Production v0.2: bind continuity evidence to subject shots**, closes a multi-subject integrity gap in `hottop.reference-continuity-benchmark.v1`.

Before this change, the verifier recomputed exact reference bytes and verified exact generated-shot bytes, but a subject's claimed shot hashes only had to appear somewhere in the global artifact manifest. In a multi-subject plan, hero and rival shot hashes could therefore be reassigned across subjects while still satisfying the global byte-membership check.

TDD evidence:

- corrected RED head `e679691705fdc223784ec2e7e3a3dbadbab45bac`: CI run **1429** failed in pytest on Python 3.11/3.12 with Ruff green; the test no longer accepts an unsupported-API `TypeError` as a valid rejection.
- GREEN implementation culminates at `6dc0ed1f7953ba343dfa353c548f020de030ade5`: `verify_reference_continuity_artifacts(...)` now requires the real `VideoProductionPlan`, maps manifest artifacts by `shot_index`, derives subject→allowed-shot hashes from `VideoShot.reference.subject_id`, and rejects evidence that claims another subject's shot bytes. The legacy no-plan weak path was intentionally removed rather than retained as a bypass.
- exact-head CI run **1432** passed on Python 3.11 and 3.12. Exact-head production-smoke run **38** was still running when this status entry was written; re-fetch before merge claims.

This is provider-neutral and adds no evaluator model, GPU requirement, paid service or network dependency.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current measured gap remains **real generated-output identity on operator-owned reference-conditioned runs**, not another provider abstraction.

Fresh evaluator admission findings this cycle:

- **DINOv3:** strong dense visual features, but code + released weights use the custom DINOv3 License; pretrained weights require upstream acceptance/access and normal helpers can download them. Operator-owned/local-only candidate.
- **SigLIP 2 SO400M:** reviewed model card is Apache-2.0, but the checkpoint is roughly 4.54 GB and standard loading downloads it. Promising operator-local candidate only; any adapter must use explicit local paths, pin revision/hash and prove benchmark value.
- **DreamSim:** MIT code, but pretrained construction downloads weights; still gated pending exact weight/backbone rights and measured value.
- **LightX2V:** remains the primary Apache-2.0 operator inference framework; exact model/weights terms remain a separate gate.
- **WanGP:** remains operator-owned because its current community license restricts monetized embedding/API/SaaS/white-label use without a separate commercial license.

Durable rule remains: **code license != model/weights/data license**, and permissive code/model terms do not justify hidden multi-GB downloads in unattended Hottop.

## Immediate next actions

1. Finish PR #30 exact-head production-smoke; review the final diff and merge only if CI + real production smoke remain green.
2. Verify post-merge main CI + automatically triggered main production-smoke again, preserving the #29 evidence lifecycle guarantee.
3. When operator-controlled LightX2V/Wan2.2 or compliant WanGP reference-conditioned assets are actually available, generate at least two byte-bound shots for the same rights-safe subject and serialize thresholded continuity evidence before claiming identity preservation.
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
