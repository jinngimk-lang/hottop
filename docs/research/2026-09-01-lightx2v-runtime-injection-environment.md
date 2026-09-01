# LightX2V runtime injection environment boundary — 2026-09-01

## Measured gap

PR #386 stopped common API credentials/tokens/secrets and proxy variables from reaching the operator-owned LightX2V child process, but the adapter still inherited interpreter/loader controls capable of changing what actually executed independently of the recorded source identity.

The concrete regression covered `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP`, and `PYTHONINSPECT`. Legitimate operator CUDA library configuration such as `LD_LIBRARY_PATH` must remain usable.

## TDD evidence

- RED exact head `653521087bb1f57f892539412037965b20ff854c`: CI #2634 reached clean Ruff and failed pytest on the new runtime-injection regression. Python 3.12 reached the failing pytest step and was cancelled by fail-fast after the failure had already been demonstrated.
- GREEN exact head `5b291939994b611dfd4083786fcf65e2c20652ae`: `_offline_environment()` now strips `LD_PRELOAD`, `PYTHONHOME`, `PYTHONSTARTUP`, and `PYTHONINSPECT` in addition to the existing proxy/secret filters, while preserving `LD_LIBRARY_PATH` and the existing local CUDA/runtime controls.
- CI #2635 passed Ruff and the full pytest suite on Python 3.11 and Python 3.12 at that exact GREEN head.

## Exact-head production evidence

- production-smoke #316 passed the checked-in cow + Odyssey execution, final-media/provenance verification and artifact upload. `hottop-software3d-production-smoke`: 687,895 bytes; `sha256:7f3c4097e14bf192978c5f936853b818d430b4234fe05dca7a32998a80e5d17c`.
- cinematic-delivery-smoke #183 passed the actual 720p24 Odyssey delivery, runtime provenance, final-media verification and artifact upload. `hottop-cinematic-software3d-delivery`: 624,451 bytes; `sha256:e8e3822c6e9cb826d6dc58384632d22446d096c803be28f115bea717d0a4a034`.

## Merge and durable consequence

PR #388 was SHA-locked to exact head `5b291939994b611dfd4083786fcf65e2c20652ae` and squash-merged as `0415e0ff59042dc923c3f08c7e5a1a43da8d09c3`.

Together with #386, this turns environment minimization from a one-off credential filter into a durable operator-inference rule: the child-process environment is part of execution/provenance scope. Offline flags and a clean source revision are not sufficient if ambient credentials, proxies, or interpreter/loader injection controls can alter execution outside the reviewed boundary.

Future exceptions should add the smallest explicit, reviewed environment requirement rather than restoring blanket parent-environment inheritance.

## Safety/cost semantics

No provider, model, download, network route, paid fallback, GPU provisioning, credential, or `ZERO_COST_MODE=true` behavior changed. This is fail-closed local execution hardening.

The rule does not prove identity fidelity, requested action, semantic correctness, or cinematic quality; those remain separate generated-media evidence dimensions.
