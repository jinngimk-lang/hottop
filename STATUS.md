# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — output-side reference/identity continuity proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current `main` at recovery: `829b4bf2085f06464d8c9ce7272c99d131893340` (`docs: sync status after mechanism runtime deployment (#27)`).

Deployed creative/runtime chain:

`fresh/supplied hotspot analysis → hotspot mechanism mapping → product role/outcome change → hottop.generation-preflight.v1 → dynamic format/style selection → render route → voice/music/SFX → quality/provenance/continuity gates → final media verification`

The repository currently enforces:

1. **Fresh-generation gate** — every new image/video request re-resolves subject, hotspot, style and format; historical examples are grammar only.
2. **Mechanism-first creative mapping** — extract recognition hook, causal/relationship mechanism, native visual/dialogue/audio grammar; the product must perform a functional role that changes the outcome.
3. **No-template runtime** — legacy keyword/archetype/four-panel inference cannot silently generate a generic brief without an explicit mechanism mapping.
4. **Video production integrity** — generated/deterministic shots pass motion/media gates, byte-bound provenance and composition-consumption verification; final delivery passes FFmpeg/ffprobe compatibility verification.
5. **Reference-conditioned quality recovery** — rights-safe reference I2V may recover weak direct-video identity/style quality, but input-side reference locks are not accepted as proof that generated output preserved identity.

## Deployed milestones

- PR #23 — mandatory fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned video quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #27 — post-deployment status synchronization, merged as `829b4bf2085f06464d8c9ce7272c99d131893340`.

Supporting production baseline remains deployed:

- deterministic zero-cost software3d → audio → MoviePy → FFmpeg → verified MP4;
- cow/snake and Odyssey repeatable production-smoke cases;
- operator-managed LightX2V/Wan2.2 T2V/I2V route with local checkout/model/config preflight and no auto-provisioning;
- operator-managed WanGP interoperability route;
- byte-bound shot provenance before composition;
- Qwen3-TTS benchmark-ready offline local adapter plus eSpeak guaranteed fallback;
- rights-safe references and structured subject/identity locks.

## Active PR #26 — output-side identity proof

PR #26, **Production v0.2: prove reference identity continuity**, replaces stale-base PR #21 and failing/stale-base PR #22. Both old PRs are closed as superseded.

The fresh-base workstream adds three linked contracts:

1. The checked-in generated-original signal-orb I2V example now uses one stable `subject_id`, role and conservative identity traits across every shot, engaging Hottop's existing identity-anchor prompt contract.
2. `hottop.reference-continuity-benchmark.v1` records exact candidate/revision, evaluator/revision, reference SHA-256, generated-shot SHA-256 values, reference-adherence score, cross-shot-identity score and explicit fail-closed thresholds.
3. Continuity evidence is bound to **actual bytes**, not manually copied hashes: the reference file is re-hashed and generated shots are re-verified through `VideoArtifactManifest` before benchmark hashes are accepted.

TDD evidence for the byte-binding layer:

- RED head `95bbddba50a8dc1765e6df87b83ace33d3d815ab`: Ruff passed; pytest failed exactly one test because `verify_reference_continuity_artifacts` did not exist (**1 failed / 432 passed**) in CI run **1418**.
- GREEN implementation head `cb335fc6dd6ba75658cea9b9b94f807bf28cfd3e`: CI run **1419** passed on Python 3.11 and 3.12; production-smoke run **28** also passed both checked-in stories and provenance/final-media verification.

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

## Current ecosystem decision

The measured gap is generated-output identity, not another provider abstraction. This cycle therefore admits a **provider-neutral benchmark contract**, not a heavyweight evaluator dependency.

- **LightX2V:** framework code remains Apache-2.0 and is the primary operator-owned Wan2.2 inference candidate already integrated in Hottop. Model/weights terms remain a separate gate.
- **WanGP:** current `WanGP Community License 2.0` permits broad private/internal use but restricts monetized embedding/API/SaaS/white-label usage without separate licensing. Keep interoperability operator-owned; do not vendor WanGP code or make it the unattended/public paid backend.
- **DreamSim:** code is MIT, but documented pretrained use downloads weights on first use. Exact weight/backbone licenses, revision, download behavior and hardware value must be reviewed before admission. Do not add it to the default unattended environment.
- **DINO-family evaluators:** plausible future similarity components, but exact checkpoint/model licenses must be reviewed independently from repository code licenses. No dependency added this cycle.

Durable admission rule remains: **code license != model/weights/data license**, and hidden downloads/network calls are incompatible with normal zero-cost unattended execution unless explicitly operator-controlled and reviewed.

## Immediate next actions

1. Re-run exact-head CI + production-smoke after the research/status documentation commits on PR #26.
2. Review the complete PR #26 diff; if exact-head evidence remains green and no new integrity issue appears, mark ready and squash-merge.
3. After merge, produce real operator-owned LightX2V/Wan2.2 or compliant WanGP reference-conditioned shots when local GPU/model assets are actually available; serialize byte-bound continuity evidence and require threshold PASS before claiming the route preserves identity.
4. Continue the guaranteed software3d production baseline and the real fresh-hotspot + product mechanism smoke independently of optional GPU availability.
5. Continue targeted upstream scans against measured gaps; integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Recovery order

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read the relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform the targeted ecosystem scan relevant to the active measured gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
