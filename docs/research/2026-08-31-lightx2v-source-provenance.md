# LightX2V stable-source provenance closure — 2026-08-31

## Why this exists

Hottop already required generated artifacts to bind the **actual generator source identity** rather than a reviewed registry pin. The LightX2V operator route exposed concrete refinements: Git HEAD alone is not sufficient when executable/importable code can exist outside the tracked tree, when a checkout changes during generation, when a linked Git worktree stores refs through a common Git directory that a manual ref reader does not resolve correctly, or when identical framework source is executed with materially different generation-config bytes.

This is an implementation-level strengthening of the existing `PROJECT.md` provenance doctrine. It does not change provider strategy or make LightX2V the unattended default.

## Closed gaps

The LightX2V route now:

1. isolates the child process from inherited `PYTHONPATH` and sets `PYTHONPATH` only to the operator checkout root;
2. requires a Git checkout to have no tracked uncommitted changes before generation;
3. enumerates untracked paths, including Git-ignored paths, and rejects importable/runtime-code suffixes (`.py`, `.pyc`, `.pyd`, `.so`, `.pth`) while unrelated local data may remain;
4. resolves source identity with the locally available Git executable using `git -C <root> rev-parse --verify HEAD`, so linked worktrees, common-dir refs and packed refs bind the actual commit;
5. fails closed if a path is a real Git checkout but its commit cannot be provenance-verified; the `source-sha256:<infer.py>` fallback remains only for deliberately non-Git operator source trees;
6. captures the exact local source revision before spawning generation and re-checks checkout cleanliness plus exact source revision after generation, before quality/provenance acceptance;
7. deletes the produced video if post-generation source verification fails, so no artifact manifest can bind output bytes to stale source provenance;
8. captures the exact `config_json` SHA-256 and byte size before generation, re-reads it after generation and deletes the output if the generation-config bytes changed;
9. persists that generation-config byte identity into each LightX2V shot artifact, and continuity verification requires all evaluated LightX2V subject-bearing shots to carry config provenance and share one exact config byte identity.

No network access, model download, GPU provisioning, paid fallback, credential use or new provider route was added.

## TDD and production evidence

Stable-source closure before linked-worktree refinement:

- initial RED: `ccfe2c4b6092c0158fba5f751d50969e11af3f52`; CI #2455 passed Ruff and failed exactly because untracked importable Python was not rejected (`1 failed / 609 passed`);
- exact GREEN feature head: `4ba114005f78e2a9396ead2787f527551859145a`;
- exact-head verification: CI #2460 success; production-smoke #220 success; cinematic-delivery-smoke #87 success;
- squash merge: `9cac3f1cce404f702ad07e7aa0f58931bb6f95fc`.

Linked-worktree refinement:

- RED exact head: `e4ec3ff3bc8c6a78979e91d78a0fc3fd3f796179`; CI #2464 passed Ruff and failed the linked-worktree provenance contract;
- exact GREEN head: `2bf92a433732d2420cb0157a6e7c7f68ebe63865`;
- exact-head verification: CI #2465 success; production-smoke #223 success; cinematic-delivery-smoke #90 success;
- squash merge: `29afecc37ed8fc414ff9a0e06f4e02e6ca677e5c`;
- post-merge CI #2467 and cinematic-delivery-smoke #92 succeeded.

Generation-config byte provenance:

- generation-time config binding was exact-head verified at `d26db1e3652637d47b1330803c59e0d24c8553ad`: CI #2475, production-smoke #227 and cinematic-delivery-smoke #94 succeeded;
- squash merge: `d6157d10d1f9f5822c8e04a3fb6b138d5623c6f5`; post-merge CI #2477, production-smoke #229 and cinematic-delivery-smoke #96 succeeded;
- continuity-coherence RED exact head `edfe08e845a2f3e1d8bfb924ff6d63d82719df6f`, CI #2478: Ruff passed and pytest failed because mixed generation-config bytes were still accepted under one continuity result;
- exact GREEN head `70a32d6e854def28e5dc1d2bc871d385ee5024ab`: CI #2479, production-smoke #230 and cinematic-delivery-smoke #97 succeeded;
- squash merge: `aa697506616c91acb902514b443a9fd0852e837a`.

## Evidence semantics and remaining limit

The contract proves that the operator checkout is clean at preflight and again immediately after generation, that accepted artifacts are associated with the same verifiable source revision at both boundaries, and that accepted LightX2V output binds the exact generation-config bytes used across the run. Continuity evidence may not combine LightX2V subject-bearing shots produced under different config-byte identities into one candidate result.

This still **does not prove checkpoint/model-directory byte identity or rights**. `model_path` remains a separately operator-provisioned local input. Framework source revision plus config bytes must not be presented as a checkpoint revision. A future model-byte provenance contract should only be added when a real operator model layout can be measured without introducing implicit downloads or a misleading partial manifest.

The source contract is designed to catch ordinary source drift, persistent untracked runtime-code contamination and linked-worktree revision misidentification. It is **not** a claim that Hottop can detect a hostile concurrent actor that mutates source during execution and restores the exact clean tree before the post-generation check. If that threat model becomes material, the stronger option is an independently materialized immutable execution snapshot or content-addressed source bundle, which must be benchmarked for LightX2V compatibility before adoption.

## Fresh upstream check

LightX2V public `main` advanced again on 2026-08-31 to `e7262940e8fcd63a91659ef1e9a2c2bb611480f2`. The tip fixes Hunyuan SR transformer weight loading and removes a stale run-step path; its parent `f85a5c6f5d97a2a031a9f11b8e7f521bde5fb691` fixes MiniMax-H3 tensor-parallel sharding for one-dimensional column-parallel biases/scales. Neither change provides Hottop-measured continuity, quality or runtime improvement for the tested Wan2.2 I2V subset, so **no freshness-only repin** is justified.

## Operating consequence

Keep LightX2V as the primary reviewed operator-owned Wan2.2 framework, but treat checkout cleanliness, import surface, commit resolution and exact generation-config bytes as generator provenance. Runtime success still does not prove checkpoint identity, identity fidelity, requested-action motion fidelity, geography, reference adherence or final-media quality; those rights/provenance/output-side gates remain independent.
