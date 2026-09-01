# LightX2V strict JSON constants — 2026-09-01

## Gap

Hottop already required the operator-provided LightX2V config to decode as UTF-8 JSON with one top-level object before GPU probing. Python's standard `json.loads`, however, is intentionally permissive by default and accepts the non-standard constants `NaN`, `Infinity`, and `-Infinity`. Those values are not valid standard JSON, so the previous preflight could produce a false-positive "valid JSON" result and let an invalid generation config reach expensive/local GPU work.

This is a version-safe validation gap. Rejecting non-standard JSON syntax does not assume any LightX2V revision-specific field or schema.

## TDD evidence

RED exact head: `60f1828d59add16823f9b32f38788b2d483d0bda`.

A regression wrote `{"guidance_scale": NaN}` and required `run_lightx2v_shot` to fail with `LightX2VError` before the injected GPU probe could run. CI #2676 reached pytest after successful setup/install/Ruff and failed on Python 3.11; Python 3.12 was cancelled by fail-fast after the defect was demonstrated.

GREEN exact head: `ee34a8dc9b479c762faaedf7a96f2070f4a58649`.

`_preflight` now uses `json.loads(..., parse_constant=...)` with a fail-closed callback that rejects non-standard numeric constants. Existing object-shape validation remains unchanged. CI #2677 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

Production merge: PR #402 was SHA-locked squash-merged as `c1c1ee0634613a17e9a334a28ba8b998596abbea`.

## Real zero-cost production evidence

Both production workflows were run on exact GREEN head `ee34a8dc9b479c762faaedf7a96f2070f4a58649` before merge.

- production-smoke #330 completed the checked-in anti-polish cow story and cinematic Odyssey story, verified both final-media/provenance chains, and uploaded `hottop-software3d-production-smoke`: 687,895 bytes, `sha256:23be225f19135731fa122ddd97ba2d5828b2d156eb0823b15e22d3db6878811b`.
- cinematic-delivery-smoke #197 completed the actual 720p24 Odyssey render, captured runtime provenance, verified H.264/AAC/yuv420p delivery plus seam/media evidence, and uploaded `hottop-cinematic-software3d-delivery`: 623,342 bytes, `sha256:9b2d0aadd5d214447ad9b1c4cf6f053173137d73c0cd90f55c56266e43f540a6`.

No paid API, hosted generation, credential use, model download, dependency auto-provisioning, or GPU provisioning was added. The guaranteed `ZERO_COST_MODE=true` software3d path remained unchanged.

## Ecosystem check and admission decision

LightX2V public `main` remained at `d7e064c4ec8dfe6a545e139156498abb8c108a3e` during this workstream; the latest observed change was the MLU/Sage Attention compile-safety fix, not same-case Wan2.2 I2V identity/requested-action evidence, so there is no freshness-only repin.

Open upstream issue #1086 continues to show that fields such as `target_video_length` can vary across config/runtime combinations. It supports cheap local config validation before GPU work, but it does **not** justify hard-coding that field as a universal Hottop schema requirement. The durable rule remains: validate standard JSON syntax and only add field-level constraints when an exact admitted revision/config contract proves them version-safe through evidence.

Other open LightX2V quality reports still separate execution from output correctness: successful runs can produce static reference frames, meaningless color blocks, or materially worse motion/content than comparable routes. Therefore this strict-JSON improvement remains a preflight/integrity gate only; it does not substitute for generated-shot identity, requested-action, semantic, or media-quality evidence.

## Rollback

The implementation is isolated to LightX2V config parsing and one regression. Rollback is the inverse of PR #402. No persisted media/config format changed, and the deterministic software3d route does not depend on this parser.

## Doctrine impact

No `PROJECT.md` change is warranted. Strict standard-JSON parsing is a stronger implementation of the already-canonical ZERO_COST/local-preflight/fail-closed operator doctrine, not a new durable product or architecture direction.
