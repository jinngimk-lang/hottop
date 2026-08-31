# LightX2V stable-source provenance closure — 2026-08-31

## Why this exists

Hottop already required generated artifacts to bind the **actual generator source identity** rather than a reviewed registry pin. The LightX2V operator route exposed concrete refinements: Git HEAD alone is not sufficient when executable/importable code can exist outside the tracked tree, when a tracked symlink resolves to mutable bytes outside the checkout, when a checkout changes during generation, or when a linked Git worktree stores refs through a common Git directory that a manual ref reader does not resolve correctly.

This is an implementation-level strengthening of the existing `PROJECT.md` provenance doctrine. It does not change provider strategy or make LightX2V the unattended default.

## Closed gaps

The LightX2V route now:

1. isolates the child process from inherited `PYTHONPATH` and sets `PYTHONPATH` only to the operator checkout root;
2. requires a Git checkout to have no tracked uncommitted changes before generation;
3. enumerates untracked paths, including Git-ignored paths, and rejects importable/runtime-code suffixes (`.py`, `.pyc`, `.pyd`, `.so`, `.pth`) while unrelated local data may remain;
4. enumerates tracked Git entries and rejects mode-`120000` symlinks whose resolved targets escape the checkout, because a clean HEAD binds the link record but not mutable bytes behind an external target;
5. resolves source identity with the locally available Git executable using `git -C <root> rev-parse --verify HEAD`, so linked worktrees, common-dir refs and packed refs bind the actual commit;
6. fails closed if a path is a real Git checkout but its commit cannot be provenance-verified; the `source-sha256:<infer.py>` fallback remains only for deliberately non-Git operator source trees;
7. captures the exact local source revision before spawning generation and re-checks checkout cleanliness plus exact source revision after generation, before quality/provenance acceptance;
8. deletes the produced video if post-generation source verification fails, so no artifact manifest can bind output bytes to stale source provenance.

Tracked symlinks that resolve inside the checkout are not rejected by the new boundary. No network access, model download, GPU provisioning, paid fallback, credential use or new provider route was added.

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
- post-merge CI #2467 succeeded. The post-merge 720p cinematic-delivery smoke is tracked separately as execution evidence and must not be inferred from CI alone.

Tracked-symlink escape refinement:

- RED exact head: `ddedc38d136f48a863f35269c5ee4e57ee9d70ec`; CI #2518 passed Ruff and failed pytest on a clean temporary Git checkout whose tracked `lightx2v/runtime.py` symlink resolved to executable Python outside the checkout;
- initial GREEN implementation head: `27b7cd816ffe20455911c5dc6a0bbe3982c309d8`; CI #2519 succeeded on Python 3.11 and 3.12 before durable-memory synchronization;
- the final PR head is re-verified after `PROJECT.md`, this record and `STATUS.md` are synchronized, so the earlier GREEN result is evidence for the behavior but not a substitute for final-head CI/smoke.

## Evidence semantics and remaining limit

The contract proves that the operator checkout is clean at preflight and again immediately after generation, that tracked source links do not escape the checkout at those boundaries, and that accepted artifacts are associated with the same verifiable source revision at both boundaries. It is designed to catch ordinary source drift, persistent untracked runtime-code contamination, linked-worktree revision misidentification and clean-HEAD external-symlink provenance escapes.

It is **not** a claim that Hottop can detect a hostile concurrent actor that mutates source during execution and restores the exact clean tree before the post-generation check. If that threat model becomes material, the stronger option is an independently materialized immutable execution snapshot or content-addressed source bundle, which must be benchmarked for LightX2V compatibility before adoption.

## Fresh upstream check

LightX2V public `main` advanced on 2026-08-31 to `d6cf4f13d152e636ae6daac604d46531077e8670`. The tip refactors ERNIE Image runner aliases/example plumbing, while same-day preceding changes affect Flux2/Hunyuan paths. The current recursive tree contains no tracked Git symlinks (`120000` entries), and the fresh changes do not provide Hottop-measured continuity, quality or runtime improvement for the tested Wan2.2 I2V subset. Therefore **no freshness-only repin** is justified.

## Operating consequence

Keep LightX2V as the primary reviewed operator-owned Wan2.2 framework, but treat checkout cleanliness, import surface, tracked-link containment and commit resolution as part of generator provenance. Runtime success still does not prove identity fidelity, requested-action motion fidelity, geography, reference adherence or final-media quality; those output-side gates remain independent.
