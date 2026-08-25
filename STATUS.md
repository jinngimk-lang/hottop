# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — output-side reference/identity continuity proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current `main` at recovery: `829b4bf2085f06464d8c9ce7272c99d131893340` (`docs: sync status after mechanism runtime deployment (#27)`).

Deployed chain:

`fresh/supplied hotspot analysis → hotspot mechanism mapping → product role/outcome change → hottop.generation-preflight.v1 → dynamic format/style selection → render route → voice/music/SFX → quality/provenance/continuity gates → final media verification`

Current deployed guarantees include mandatory fresh-generation preflight, mechanism-first creative mapping, no silent legacy template/archetype fallback, the guaranteed zero-cost software3d → audio → MoviePy → FFmpeg baseline, operator-owned LightX2V/Wan2.2 and WanGP interoperability routes, byte-bound shot provenance, composition-consumption verification, Qwen3-TTS benchmark-ready local audio, and final ffprobe media verification.

Deployed recent milestones:

- PR #23 — fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #27 — status synchronization after #24/#25 deployment, merged as `829b4bf2085f06464d8c9ce7272c99d131893340`.

## Active reference-continuity work

Stale-base PR #21 and failing/stale-base PR #22 were closed as superseded. Their useful contracts were rebuilt on current `main` after PR #27 as the reference-continuity workstream.

The work adds three linked production contracts:

1. The checked-in generated-original signal-orb I2V example uses one stable `subject_id`, role and conservative identity traits across all shots, so the existing identity-anchor prompt contract is actually engaged.
2. `hottop.reference-continuity-benchmark.v1` records exact candidate/revision, evaluator/revision, reference SHA-256, generated-shot SHA-256 values, reference-adherence score, cross-shot-identity score and explicit fail-closed thresholds.
3. Continuity evidence is bound to **actual bytes**, not manually copied hashes: the reference file is re-hashed and generated shots are re-verified through `VideoArtifactManifest` before benchmark hashes are accepted.

TDD evidence from the predecessor fresh-base workstream remains the proof history for the byte-binding layer:

- RED head `95bbddba50a8dc1765e6df87b83ace33d3d815ab`: Ruff passed; pytest failed exactly one test because `verify_reference_continuity_artifacts` did not exist (**1 failed / 432 passed**) in CI run **1418**.
- GREEN implementation head `cb335fc6dd6ba75658cea9b9b94f807bf28cfd3e`: CI run **1419** passed on Python 3.11 and 3.12; production-smoke run **28** passed both checked-in stories plus provenance/final-media verification.

Because `main` advanced during that work, the final state was rebuilt on current `main@829b4bf…` rather than force-merging a diverged branch. Re-fetch the active PR/head and exact-head checks before merge claims.

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

## Ecosystem decision

The measured gap is **generated-output identity**, not another provider abstraction. This cycle therefore admits a provider-neutral benchmark contract rather than a heavyweight evaluator dependency.

- **LightX2V:** framework code is Apache-2.0 and remains the primary operator-owned Wan2.2 inference candidate already integrated in Hottop. Exact model/weights terms remain a separate gate.
- **WanGP:** current `WanGP Community License 2.0` permits broad private/internal use but restricts monetized embedding/API/SaaS/white-label usage without separate licensing. Keep interoperability operator-owned; do not vendor WanGP or make it an unattended/public paid backend.
- **DreamSim:** code is MIT, but documented pretrained use downloads weights on first use. Exact weights/backbone licenses, revision, hidden download behavior and measurable benchmark value must be reviewed before admission. It is not added to the unattended default environment.
- **DINO-family evaluators:** plausible future similarity components, but exact checkpoint/model licenses must be reviewed independently from repository code licenses. No dependency added this cycle.

Durable admission rule remains: **code license != model/weights/data license**. Hidden downloads/network calls are incompatible with normal zero-cost unattended execution unless explicitly operator-controlled and reviewed.

## Immediate next actions

1. Run exact-head CI + production-smoke on the current-main rebuild of the continuity workstream.
2. Review the complete diff; if current-base evidence is green and no new integrity problem appears, mark ready and squash-merge.
3. After merge, produce real operator-owned LightX2V/Wan2.2 or compliant WanGP reference-conditioned shots when local GPU/model assets are actually available; serialize byte-bound continuity evidence and require threshold PASS before claiming the route preserves identity.
4. Continue the guaranteed software3d baseline and a real fresh-hotspot + product mechanism smoke independently of optional GPU availability.
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
