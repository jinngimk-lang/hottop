# LightX2V duplicate JSON object keys — 2026-09-01

## Gap

Hottop already required operator-provided LightX2V configs to decode as UTF-8 strict JSON with one top-level object before GPU probing. Python's standard JSON decoder nevertheless accepts duplicate object names and silently keeps the final value. A config such as `{"guidance_scale": 3.0, "guidance_scale": 7.5}` therefore had byte-bound provenance but ambiguous effective semantics.

This is a version-safe preflight gap. Rejecting duplicate object names does not assume any LightX2V revision-specific field or schema.

## TDD evidence

RED exact head: `ba9a13a7d04c50525ef246eecc86d4d958989cfd`.

A regression supplied duplicate `guidance_scale` names and required `run_lightx2v_shot` to raise `LightX2VError` before the injected GPU probe could run. CI #2681 completed setup, install and Ruff successfully on Python 3.11, then full pytest failed because the old decoder accepted the duplicate-name config and reached the injected probe. Python 3.12 is not relied upon as RED evidence.

GREEN exact head: `bfe02fbdb03211bac44c1aba8097d1faea20bd97`.

`_preflight` now passes `object_pairs_hook=_reject_duplicate_json_keys` to `json.loads`. The hook checks every decoded JSON object, so duplicate names are rejected recursively while preserving the existing strict-constant and top-level-object checks. No field-level LightX2V schema is introduced. CI #2682 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

Production merge: PR #404 was SHA-locked squash-merged as `36274812206e0f4a25434bd6ba45154598298264`.

## Real zero-cost production evidence

Both production workflows ran on exact GREEN head `bfe02fbdb03211bac44c1aba8097d1faea20bd97` before merge.

- production-smoke #332 completed the checked-in anti-polish cow story and cinematic Odyssey story, verified both final-media/provenance chains, and uploaded `hottop-software3d-production-smoke`: 688,373 bytes, `sha256:b4cd4cc1619468c4c0b14c673139a74a50ba089e90d124dab0c0d1fb1e267452`.
- cinematic-delivery-smoke #199 completed the actual 720p24 Odyssey render, captured runtime provenance, verified delivery media/provenance, and uploaded `hottop-cinematic-software3d-delivery`: 624,450 bytes, `sha256:65940330d3f9c71b90e757d79cd031a7e484760f915eac7d5d7b7a831991dff2`.

No paid API, hosted generation, credential use, model download, dependency auto-provisioning, or GPU provisioning was added. The guaranteed `ZERO_COST_MODE=true` software3d path remained unchanged.

## Ecosystem check and admission decision

LightX2V public `main` remained at `d7e064c4ec8dfe6a545e139156498abb8c108a3e` during this workstream; its newest observed change is MLU/Sage Attention compile safety, not same-case Wan2.2 I2V identity/requested-action evidence, so there is no freshness-only repin.

Open upstream quality reports continue to demonstrate that execution success is not output correctness: runs can produce static reference frames, meaningless color blocks, or materially worse content/motion than comparable routes. Duplicate-key rejection is therefore a config determinism/preflight gate only; it does not substitute for generated-shot identity, requested-action, semantic, motion or media-quality evidence.

Qwen3-TTS-ncnn remains a gated operator-owned TTS candidate. Its public implementation is active and targets local CPU/Vulkan Qwen3-TTS execution, but Hottop still lacks a rights-safe same-line Mandarin A/B with exact model/runtime provenance. No model or dependency was downloaded or installed during this cycle.

## Rollback

The implementation is isolated to LightX2V JSON parsing and one regression. Rollback is the inverse of PR #404. No persisted media format, artifact schema, software3d behavior or provider routing changed.

## Doctrine impact

No `PROJECT.md` change is warranted. Rejecting ambiguous duplicate JSON names is a stronger implementation of the already-canonical ZERO_COST/local-preflight/fail-closed/provenance doctrine, not a new durable product or architecture direction.
