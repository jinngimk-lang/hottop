# LightX2V cloud-credential environment isolation — 2026-09-01

## Measured gap

The operator-owned LightX2V route already forced offline Hugging Face/Transformers/Datasets behavior and stripped proxy settings, common secret suffixes, Python/loader injection controls and user-site injection. However, the subprocess environment still inherited common cloud credential handles whose names do not match the generic `_API_KEY`, `_TOKEN`, `_SECRET` or `_PASSWORD` suffixes: `AWS_ACCESS_KEY_ID`, `AWS_SHARED_CREDENTIALS_FILE`, `GOOGLE_APPLICATION_CREDENTIALS`, and `CLOUDSDK_CONFIG`.

Those variables are unnecessary for an offline local inference subprocess and can expose credentials or credential-file locations to code that should only see reviewed local generation assets.

## TDD evidence

RED exact test commit: `4c8f4ceda3eb1370eea2beec48b2437f9d61aed5`.

CI #2644 reached clean Ruff and failed pytest on the new regression that asserts the four cloud credential handles are absent while `CUDA_VISIBLE_DEVICES` remains available. Python 3.11 demonstrated the defect; the parallel 3.12 job was cancelled after fail-fast/branch progression and is not counted as independent RED evidence.

GREEN exact production head: `0280bb751db022a37a3f6e02fc220cc95517bb06`.

The implementation adds a narrow explicit sensitive credential-key denylist to `_offline_environment()`. It does not convert the environment into an unusable global allowlist: operator-local execution controls such as CUDA visibility and library paths remain available, while the four reviewed cloud credential handles are removed in addition to the existing proxy/secret/runtime/user-site filters.

CI #2645 passed Ruff + full pytest on Python 3.11 and 3.12.

## Same-head production evidence

Production smoke #320 passed the checked-in anti-polish cow story plus cinematic Odyssey execution, final-media verification and provenance verification. Uploaded artifact `hottop-software3d-production-smoke` is 687,895 bytes with digest `sha256:70fa5774ecf9db34761cfd08db7cd037f67f42e3bf1e15cdd486804a034906bc`.

Cinematic-delivery-smoke #187 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification. Uploaded artifact `hottop-cinematic-software3d-delivery` is 623,330 bytes with digest `sha256:3dcb6f2525421f9dedfc1a466bd36b7b52ee6c0260f65e37cd6a6e50658d97c7`.

PR #392 was SHA-locked squash-merged from exact GREEN head `0280bb751db022a37a3f6e02fc220cc95517bb06` as `e36456495a05ba5985a04b840a8678edd79af1cc`.

## Scope and non-claims

This is defense-in-depth for the existing ZERO_COST/offline operator route. It does not install dependencies, download models, provision GPU hardware, call hosted services, consume credits, change providers, change model pins, alter software3d output or relax any quality gate.

It also does not prove real LightX2V I2V quality. Runtime/environment integrity, media integrity, identity fidelity and requested-action fidelity remain distinct evidence dimensions.

## Ecosystem check

The current LightX2V/Wan2.2 ecosystem still offers materially interesting acceleration routes such as Wan2.2-Lightning four-step I2V, but those routes require additional base-model/LoRA assets and do not yet provide Hottop same-case identity/requested-action evidence. Public issue reports also continue to include slow-motion behavior in newer MoE I2V variants. No freshness-only repin or unattended model download is justified by this workstream.

## Rollback

Rollback is the isolated `_SENSITIVE_CREDENTIAL_ENV_KEYS` filter addition plus its regression test. If a future reviewed local runtime genuinely requires one of these credential handles, add a narrowly justified explicit opt-in contract with tests rather than restoring ambient credential inheritance.
