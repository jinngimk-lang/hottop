# LightX2V runtime-injection environment isolation — 2026-09-01

## Measured gap

After PR #386, the LightX2V operator subprocess no longer inherited common API secrets or proxy settings, but `_offline_environment()` still forwarded interpreter/loader injection controls from the parent process. In particular, `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP`, and `PYTHONINSPECT` could alter the effective Python/native runtime independently of the recorded LightX2V checkout/source provenance.

That is a provenance and execution-integrity gap: a clean generator Git/source identity is not sufficient if the child runtime can be modified by unbound parent environment injection.

## TDD evidence

- RED exact head `653521087bb1f57f892539412037965b20ff854c`: CI #2634 reached clean Ruff and failed pytest on the new runtime-injection regression. Python 3.12 was cancelled by fail-fast after the regression had already been demonstrated.
- GREEN exact head `5b291939994b611dfd4083786fcf65e2c20652ae`: `_offline_environment()` strips `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP`, and `PYTHONINSPECT` while preserving legitimate local runtime configuration such as `LD_LIBRARY_PATH`.
- CI #2635 passed Ruff + full pytest on Python 3.11 and 3.12.

## Exact-head production evidence

The same GREEN head passed both production media workflows:

- production-smoke #316: success; `hottop-software3d-production-smoke`, 687,895 bytes, `sha256:7f3c4097e14bf192978c5f936853b818d430b4234fe05dca7a32998a80e5d17c`.
- cinematic-delivery-smoke #183: success after actual 720p24 Odyssey delivery, runtime provenance and final-media verification; `hottop-cinematic-software3d-delivery`, 624,451 bytes, `sha256:e8e3822c6e9cb826d6dc58384632d22446d096c803be28f115bea717d0a4a034`.

PR #388 was SHA-locked squash-merged from the verified head. The resulting production commit is `0415e0ff59042dc923c3f08c7e5a1a43da8d09c3`.

## Scope and non-claims

This change does not install software, download weights, provision GPU capacity, call hosted services, enable paid fallback, or modify the guaranteed software3d route. It is defense-in-depth for the existing operator-owned offline LightX2V route.

It is not evidence of subject identity, requested-action correctness, semantic quality, or Wan2.2 output quality. Those still require real rights-safe generated I2V media and the separate continuity/action gates.

## Rollback

Rollback is the small environment-filter delta in PR #388. If a reviewed local runtime proves that one of the stripped variables is genuinely required, restore only that variable behind an explicit, provenance-bound operator configuration rather than returning to unrestricted parent-environment inheritance.
