# LightX2V user-site isolation — 2026-09-01

## Measured gap

The operator LightX2V child process already pinned `PYTHONPATH` to the reviewed checkout and stripped several direct runtime-injection controls, but it still inherited `PYTHONUSERBASE`. Python can use that value to locate user site-packages outside the reviewed LightX2V checkout, so the effective import/runtime state could diverge from the recorded source provenance.

## TDD evidence

- RED exact head `2927227b8017993754359bfdd8b9962f09d57503`: CI #2638 reached clean Ruff and failed pytest on Python 3.11 when the regression required `PYTHONUSERBASE` to be absent and `PYTHONNOUSERSITE=1`; Python 3.12 was cancelled by fail-fast after the defect had been demonstrated.
- GREEN exact head `6cbca6a940c24221f7fbc1569988759a25c7cb64`: the child environment now strips `PYTHONUSERBASE` and forces `PYTHONNOUSERSITE=1`, while preserving the reviewed checkout `PYTHONPATH`, offline flags and legitimate local runtime controls.
- CI #2640 passed Ruff + full pytest on Python 3.11 and 3.12.

## Exact-head production evidence

The same GREEN head passed both real media workflows:

- production-smoke #318: success; artifact `hottop-software3d-production-smoke`, 687,894 bytes, `sha256:eeaf865f446d215a287c660a97af793401a0b692219bd8b9ae5f4ff4b4febf96`.
- cinematic-delivery-smoke #185: success after actual 720p24 Odyssey delivery, runtime provenance and final-media verification; artifact `hottop-cinematic-software3d-delivery`, 624,450 bytes, `sha256:18c7f2ae1f6bbc40bf84e2e1b472c0aa114c2c53c4324715e84a077618cb557e`.

PR #390 was SHA-locked squash-merged from the verified head. The resulting production commit is `4e93024aee9e58edbd9c2d5304c845462b6d953e`.

## Scope and non-claims

This is source/runtime provenance defense-in-depth for the operator-owned offline route. It does not install software, download weights, provision GPU capacity, call a hosted service, enable paid fallback, or change the guaranteed software3d route. It is not generated-media evidence and does not establish subject identity, requested-action correctness or semantic quality.

## Rollback

Rollback is the narrow environment change from PR #390. If a reviewed operator runtime proves user-site loading is actually required, restore it only through an explicit provenance-bound configuration and bind the additional package/runtime state instead of returning to implicit parent user-site inheritance.
