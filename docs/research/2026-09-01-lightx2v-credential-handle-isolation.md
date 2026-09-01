# LightX2V credential-handle isolation — 2026-09-01

## Measured gap

Hottop's operator-owned LightX2V child process already ran with Hugging Face/Transformers/Datasets offline flags and stripped proxy settings, common suffix-style secrets, AWS access keys, AWS shared credential files, Google application credentials, Cloud SDK config, interpreter/loader injection controls and unbound Python user-site packages.

The parent environment could still forward three credential-access handles that are unnecessary for local video inference:

- `AWS_CONFIG_FILE`, which can redirect AWS SDK configuration and credential-provider behavior.
- `AZURE_CONFIG_DIR`, which can redirect Azure CLI/config/auth state.
- `SSH_AUTH_SOCK`, which exposes an SSH agent signing socket.

An offline inference subprocess does not need any of those capabilities. Keeping them would violate the existing least-authority/offline operator boundary even though Hottop itself does not intentionally make network calls.

## TDD evidence

RED exact head: `011436b9329da0871132b2511aa205377f57cdc6`.

CI #2654 proved the previous behavior: Python 3.12 completed setup and Ruff successfully, then failed pytest on the new regression requiring the three handles to be absent. Python 3.11 was cancelled by fail-fast after the defect had already been demonstrated and is not counted as an independent RED pass/fail result.

GREEN exact head: `b90c43931a0f3fed0992fb7ff8a3c94b941b4936`.

The fix adds only `AWS_CONFIG_FILE`, `AZURE_CONFIG_DIR`, and `SSH_AUTH_SOCK` to the existing explicit credential-handle denylist. Legitimate local execution controls such as `CUDA_VISIBLE_DEVICES` and `LD_LIBRARY_PATH` remain available. CI #2655 passed Ruff and the full test suite on Python 3.11 and 3.12.

## Exact-head production evidence

The GREEN head also passed both production media workflows rather than relying on unit tests alone:

- production-smoke #324 succeeded for checked-in anti-polish cow and cinematic Odyssey execution plus final-media/provenance verification. Artifact `hottop-software3d-production-smoke`: 687,895 bytes; `sha256:a85f5e1a868f1c5656cc2f10fb83d100bb7b37d7157c4238b3789d03cdb701db`.
- cinematic-delivery-smoke #191 succeeded for actual 720p24 Odyssey delivery, runtime provenance, final-media verification and evidence upload. Artifact `hottop-cinematic-software3d-delivery`: 624,448 bytes; `sha256:6085d0aabc862eef4a36045c4d42d2551681c1eb05368aab536b17bbbef1f312`.

PR #396 was SHA-locked squash-merged as `61a69be2c60be9ccac91dfd0b9c7413bffe34b6f`.

## Zero-cost / safety impact

This is defense-in-depth for the already-reviewed local operator route. It does not add a provider, hosted call, package installation, model download, paid fallback, credential requirement or GPU provisioning. `ZERO_COST_MODE=true` behavior and the deterministic software3d production baseline are unchanged.

Rollback is narrow: revert the three explicit denylist entries and their regression assertions. No artifact schema or provider contract changed.

## Ecosystem radar

During this production cycle LightX2V public `main` advanced to `d7e064c4ec8dfe6a545e139156498abb8c108a3e` with `fix(mlu): make Sage attention compile safe (#1435)`. That is a runtime/compiler maintenance change, not Hottop evidence that Wan2.2 I2V identity, requested-action fidelity or same-case cinematic quality improved, so there is no freshness-only repin.

Open upstream evidence still argues for keeping execution/media integrity separate from semantic quality: #1170 reports official Wan2.2 TI2V/I2V output degenerating into meaningless color blocks; #603 reports materially worse resolution/content/motion than Diffusers under comparable settings; and #1246 reports four-step Wan2.2 I2V distillation-LoRA image-conditioning keys such as `cross_attn.k_img`, `cross_attn.v_img` and `img_emb` not matching during merge. Distilled/accelerated assets therefore remain gated until exact code+weights/config provenance and rights-safe same-case identity/requested-action evidence are independently verified.

## Durable doctrine decision

`PROJECT.md` does not change for this workstream. Credential-handle isolation is a stricter implementation of existing ZERO_COST, offline, secret-safety, least-authority and fail-closed operator doctrine rather than a new durable product direction.
