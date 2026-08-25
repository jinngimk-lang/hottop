# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — obtain real reference-conditioned continuity evidence**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current deployed `main`: `cdcaa24024aaf84b588ea5245ad43865213a091e` (`Production v0.2: require complete continuity shot coverage (#31)`).

Post-merge evidence for #31 is complete:

- main CI run **1445** passed;
- automatically triggered main-push production-smoke run **50** passed;
- the production smoke executed both checked-in cow and Odyssey software3d stories through real config → moving shots → Mandarin audio/music/SFX → MoviePy → FFmpeg → final media/provenance verification and uploaded the reproducible evidence bundle.

The deployed continuity verifier now has three fail-closed layers:

1. evaluator evidence is bound to the exact planned reference bytes;
2. claimed shot bytes must belong to plan shots carrying the same `reference.subject_id`;
3. for every subject actually included in continuity evaluation, evidence must cover **all** byte-bound subject-bearing plan shots, preventing routes from cherry-picking only their best-looking shots and omitting identity-drift failures.

Benchmark scope remains explicit. Incidental or single-shot subjects are not forced into cross-shot evaluation merely because they carry a `subject_id`.

Recent deployed milestones:

- PR #23 — fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #28 — output-side identity evidence and exact-byte continuity binding, merged as `3fd869a93b8fc651cc3f2e624767c13498076de7`.
- PR #29 — post-merge `main` production evidence, merged as `fb3c8dea92591f8872cd5fc89197a2b8fd914cd3`.
- PR #30 — subject→planned-reference→subject-shot continuity binding, merged as `eac3beed84f9a9481c3ee9b7e9716803ef9bcdc9`.
- PR #31 — complete shot coverage for each evaluated subject, merged as `cdcaa24024aaf84b588ea5245ad43865213a091e`.

## Current measured gap

The remaining identity gap is no longer structural benchmark integrity. It is **real generated-output evidence** from an operator-owned reference-conditioned route.

Hottop does not currently have an operator-provided local LightX2V/Wan2.2 or compliant WanGP runtime/model/assets available in this execution environment, and normal unattended operation must not auto-download multi-GB models, provision a GPU, consume credits or weaken that boundary. The guaranteed software3d baseline remains fully usable and continuously smoke-tested.

The next identity claim therefore requires an actual operator-controlled run, not another unproven provider abstraction:

- at least two generated, byte-bound plan shots for the same rights-safe evaluated subject;
- the exact planned local reference and stable `subject_id`;
- quality-gated shot artifacts and provenance;
- continuity evidence covering **every** subject-bearing plan shot for that evaluated subject;
- explicit evaluator identity/revision and fail-closed thresholds before the route may be described as identity-preserving.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current evaluator admission posture:

- **SigLIP 2 Base 256** remains the preferred first operator-local evaluator experiment: official Apache-2.0 model-card posture, roughly 1.54 GB repository / 1.5 GB main safetensors, but local-path-only because standard Transformers loading can download implicitly.
- **SigLIP 2 SO400M** remains a higher-capacity multi-GB fallback candidate, not the first experiment.
- **DINOv3** remains operator-owned/local-only because code + released weights use the custom DINOv3 License and pretrained access requires upstream acceptance.
- **DreamSim** remains gated because MIT code does not establish the rights/runtime boundary for downloaded pretrained weights/backbones.
- **LightX2V** remains the primary Apache-2.0 operator inference framework; exact model/weights terms remain separate.
- **WanGP** remains operator-owned under its current community-license restrictions; upstream reference/continuation and LTX/H3 quality work remains useful for later benchmarks but does not change the license/runtime boundary or justify vendoring/auto-provisioning.

Durable rule remains: **code license != model/weights/data license**, and permissive code/model terms do not justify hidden multi-GB downloads in unattended Hottop.

## Immediate next actions

1. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime and rights-safe assets are actually present, execute the real multi-shot identity benchmark and serialize full evaluated-subject continuity evidence before making an identity-preservation claim.
2. Prefer the reviewed SigLIP 2 Base 256 local-path route for the first model-based evaluator experiment, but only after explicit local weights are supplied; pin exact revision/hash, perform no implicit download, and require same-subject vs identity-drift control separation before admission.
3. Continue the guaranteed software3d cow/Odyssey production proof and real fresh-hotspot + product-mechanism production independently of optional GPU availability.
4. Continue Mandarin dialogue quality benchmarking through reviewed operator-owned local Qwen3-TTS/CosyVoice routes when their local runtimes/models are supplied; eSpeak remains the guaranteed fallback.
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
