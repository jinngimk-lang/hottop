# LightX2V offline subprocess environment isolation — 2026-09-01

## Measured gap

The operator-owned LightX2V adapter already forced Hugging Face offline flags, but its child-process environment was copied from the full parent process. That allowed unrelated API credentials, secret-like variables and proxy settings to cross the process boundary even though the route is intended to be local/offline and zero-paid.

This was a security and provenance gap, not a video-quality claim: an operator inference process should receive the local runtime controls it needs, not ambient credentials it does not need.

## TDD evidence

- RED head `ad1fa516...`: CI #2629 reached the new regression and failed because inherited `OPENAI_API_KEY`, `HF_TOKEN`, `HTTPS_PROXY` and `ALL_PROXY` were still present while `CUDA_VISIBLE_DEVICES` and required offline flags were expected to remain available.
- GREEN exact head `9691ed8ca8b013ac1987d6d55a8617c33dd0793f`: `_offline_environment()` now removes proxy keys and environment variables whose names end in `_API_KEY`, `_TOKEN`, `_SECRET` or `_PASSWORD`, preserves ordinary local runtime controls, pins `PYTHONPATH` to the reviewed checkout, and forces Hugging Face/Transformers/Datasets offline plus telemetry-disable flags.
- CI #2630 passed Ruff and the full pytest suite on Python 3.11 and 3.12 at the exact GREEN head.

## Production evidence at the exact GREEN head

- production-smoke #314 passed checked-in cow + Odyssey execution, final-media/provenance verification and upload. Artifact `hottop-software3d-production-smoke`: 687,895 bytes; digest `sha256:f217b610d9df7cf8369b49c978061658fc56db53ee04f4700e6ebe8bc4bbea8f`.
- cinematic-delivery-smoke #181 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification. Artifact `hottop-cinematic-software3d-delivery`: 624,450 bytes; digest `sha256:50192c1ba0dd5d841812f27e1e7c46140a8d4ef39584a267e44e2f03bc96c0a9`.

## Merge and rollback

PR #386 was SHA-locked to exact head `9691ed8ca8b013ac1987d6d55a8617c33dd0793f` and squash-merged as `9e19c7a611cd40e5beebc6a5c464362240dd3847`.

Rollback is a normal revert of that merge if a reviewed operator runtime proves that a removed variable is genuinely required. Do not restore blanket parent-environment inheritance; add the smallest explicitly justified local runtime variable instead.

## Safety/cost semantics

This change does not install LightX2V, download models, provision a GPU, enable network access, consume credits, or add a hosted fallback. `ZERO_COST_MODE=true` remains canonical and the software3d route remains the unattended guarantee.

Environment isolation is defense in depth. It does **not** prove generated-shot identity, requested action, semantic correctness, or cinematic quality. Those remain separate generated-media gates.
