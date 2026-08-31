# LightX2V stable-source provenance closure — 2026-08-31

## Why this exists

Hottop already required generated artifacts to bind the **actual generator source identity** rather than a reviewed registry pin. The LightX2V operator route exposed a concrete refinement of that doctrine: a Git HEAD is not sufficient evidence when executable/importable code can exist outside the tracked tree, or when the checkout changes between preflight and artifact acceptance.

This is an implementation-level strengthening of the existing `PROJECT.md` provenance doctrine, not a new provider strategy or a new default backend.

## Closed gaps

The LightX2V route now:

1. isolates the child process from inherited `PYTHONPATH` and sets `PYTHONPATH` only to the reviewed operator checkout root;
2. requires a Git checkout to have no tracked uncommitted changes before generation;
3. enumerates untracked paths **including Git-ignored paths** and rejects importable/runtime-code suffixes (`.py`, `.pyc`, `.pyd`, `.so`, `.pth`), while unrelated operator data such as text notes remains allowed;
4. captures the exact local source revision before spawning generation;
5. after generation returns, re-checks checkout cleanliness and exact source revision before accepting quality/provenance;
6. deletes the generated output if the post-generation source check fails, so no artifact manifest can bind output bytes to stale source provenance.

The implementation intentionally does **not** add network access, model downloads, GPU provisioning, paid fallback, credentials, or a new provider route.

## TDD and production evidence

- Initial RED: `ccfe2c4b6092c0158fba5f751d50969e11af3f52`; CI #2455 passed Ruff and failed exactly because untracked importable Python was not rejected (`1 failed / 609 passed`).
- Exact GREEN feature head: `4ba114005f78e2a9396ead2787f527551859145a`.
- Exact-head verification: CI #2460 success; production-smoke #220 success; cinematic-delivery-smoke #87 success.
- Squash merge: `9cac3f1cce404f702ad07e7aa0f58931bb6f95fc`.

## Evidence semantics and remaining limit

The contract proves that the operator checkout is clean at preflight and again immediately after generation, and that the accepted artifact is associated with the same recorded source revision at both boundaries. It is designed to catch accidental/ordinary source drift and persistent untracked runtime-code contamination.

It is **not** a claim that Hottop can detect a hostile concurrent actor that mutates source during execution and restores the exact clean tree before the post-generation check. If the threat model ever expands to adversarial concurrent mutation, the stronger solution is an independently materialized immutable execution snapshot (for example a reviewed detached worktree/content-addressed source bundle), which must be benchmarked for LightX2V compatibility before adoption.

## Fresh upstream check

LightX2V public `main` advanced on 2026-08-31 from `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6` to `f85a5c6f5d97a2a031a9f11b8e7f521bde5fb691`. The new commit fixes MiniMax-H3 tensor-parallel sharding for one-dimensional column-parallel biases/scales. It does not provide Hottop-measured continuity, quality, or runtime improvement for the tested Wan2.2 I2V subset, so **no freshness-only repin** is justified.

## Operating consequence

Keep LightX2V as the primary reviewed operator-owned Wan2.2 framework, but treat source checkout cleanliness/stability as part of generator provenance. Runtime success still does not prove identity fidelity, requested-action motion fidelity, geography, reference adherence, or final-media quality; those output-side gates remain independent.
