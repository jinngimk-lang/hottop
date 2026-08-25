# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — keep merged production evidence continuously green**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current `main` at recovery: `3fd869a93b8fc651cc3f2e624767c13498076de7` (`Production v0.2: enforce output identity evidence (#28)`). Main CI run **1422** passed.

PR #28 is merged. The deployed chain now includes output-side continuity evidence:

`fresh/supplied hotspot analysis → hotspot mechanism mapping → product role/outcome change → hottop.generation-preflight.v1 → dynamic format/style selection → render route → voice/music/SFX → quality/provenance gates → byte-bound reference/shot continuity evidence → final media verification`

Current deployed guarantees include mandatory fresh-generation preflight, mechanism-first creative mapping, no silent legacy template/archetype fallback, the guaranteed zero-cost software3d → audio → MoviePy → FFmpeg baseline, operator-owned LightX2V/Wan2.2 and WanGP interoperability routes, byte-bound shot provenance, composition-consumption verification, Qwen3-TTS benchmark-ready local audio, final ffprobe media verification, and provider-neutral `hottop.reference-continuity-benchmark.v1` evidence bound to actual reference and generated-shot bytes.

Recent deployed milestones:

- PR #23 — fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — mechanism-first creative doctrine + optional image-first/reference-conditioned quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.
- PR #27 — status synchronization after #24/#25 deployment, merged as `829b4bf2085f06464d8c9ce7272c99d131893340`.
- PR #28 — output-side identity evidence and exact-byte continuity binding, merged as `3fd869a93b8fc651cc3f2e624767c13498076de7`.

## Active workstream — PR #29

Draft PR #29, **Production v0.2: keep main production evidence green**, starts from current `main` and closes an evidence-lifecycle gap: `.github/workflows/production-smoke.yml` previously ran only for pull requests/manual dispatch, so a merged video-path change did not itself receive the same post-merge full production proof.

TDD evidence:

- RED head `22105f1d8f91a1c50d12beaad6f6d6f08a915fea`: CI run **1423** failed after adding a contract that requires the production-smoke workflow to run on `main` pushes.
- GREEN implementation head `2b96eecc888477222a647a16eae4803ebfd01078`: the existing software3d production smoke now also triggers on relevant `main` pushes, using the same path filter and the same real cow + Odyssey config→moving shots→audio→MoviePy→FFmpeg→ffprobe/provenance verification. Exact-head CI/production-smoke were still running at the time this status entry was written; re-fetch before merge claims.

This change adds no paid service, credential, GPU/model dependency or new runtime package. It makes merged production evidence continuous rather than PR-only.

## Reference-continuity evaluator radar

Research record: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

Current measured gap remains **real generated-output identity on operator-owned reference-conditioned runs**, not another provider abstraction.

Fresh evaluator admission findings added this cycle:

- **DINOv3:** technically strong dense visual features, but code + weights use the custom DINOv3 license; pretrained weights require upstream acceptance/access and normal hub helpers can download them. Keep operator-owned/local-only; do not admit to unattended default.
- **SigLIP 2 SO400M:** reviewed model card declares Apache-2.0, but the checkpoint is about 4.54 GB and standard loading downloads it. Keep as a promising operator-local evaluator candidate only; any future adapter must be local-path-only, pin exact revision/hash and prove benchmark value before preference.
- **DreamSim:** MIT code but pretrained construction downloads weights; remains gated until exact weight/backbone rights and value are reviewed.
- **LightX2V:** remains the primary Apache-2.0 operator inference framework; exact model/weights terms remain separate.
- **WanGP:** remains operator-owned due its current community-license restrictions on monetized embedding/API/SaaS/white-label use.

Durable rule remains: **code license != model/weights/data license**, and a permissive license does not justify hidden multi-GB downloads in unattended Hottop.

## Immediate next actions

1. Finish PR #29 exact-head CI + production-smoke; review the complete diff, then mark ready and squash-merge if evidence is green.
2. Confirm the new `main` push trigger produces a post-merge production-smoke run and archive that result as the new baseline.
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
