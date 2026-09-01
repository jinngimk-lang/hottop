# LightX2V AWS secret access-key isolation — 2026-09-01

## Measured gap

The operator-owned LightX2V subprocess was already forced offline and stripped common suffix-style secrets plus several explicit cloud credential handles. One AWS secret remained outside both filters: `AWS_SECRET_ACCESS_KEY` does not end in `_API_KEY`, `_TOKEN`, `_SECRET`, or `_PASSWORD`, and it was not present in the explicit credential denylist.

That meant an unrelated parent-shell AWS secret could still be inherited by the supposedly isolated inference subprocess. The companion `AWS_ACCESS_KEY_ID` was already stripped, but forwarding any unused cloud secret into local model execution is unnecessary authority and violates the project's fail-closed secret-hygiene intent.

This is operator-runtime hardening, not a generated-video quality claim.

## RED → GREEN evidence

RED exact head `d39cace8035e7057a75183e864504e993787e761` added only the regression assertion that `AWS_SECRET_ACCESS_KEY` must not reach `_offline_environment()`. CI #2649 reached clean Ruff and then failed full pytest on Python 3.11 at that assertion. The parallel Python 3.12 job was cancelled by fail-fast after the defect was demonstrated and is not counted as a second RED failure.

GREEN exact head `e88690315c38bda7d16c41e66d7691b2aa3d4190` added `AWS_SECRET_ACCESS_KEY` to the existing explicit credential denylist. CI #2650 passed Ruff and full pytest on Python 3.11 and 3.12.

The same exact GREEN head also passed both production-media workflows:

- production-smoke #322 executed the checked-in anti-polish cow and cinematic Odyssey stories, verified final media and provenance, and uploaded `hottop-software3d-production-smoke`: 687,895 bytes, `sha256:8235f5eaf2fe3902f1f6e654da9a45c37e06ab6fa3a668e4b7bcd621def0d478`.
- cinematic-delivery-smoke #189 completed the actual 720p24 Odyssey delivery, captured runtime provenance, verified delivery media/provenance, and uploaded `hottop-cinematic-software3d-delivery`: 623,330 bytes, `sha256:2a164c5f0cba1959c33a2b0181643b1fab1b07ad6743f0f8471bdb0459966345`.

PR #394 was SHA-locked to the GREEN head and squash-merged as `df532d7939b5ef462c0bcf27a52a22f73d2b9782`.

## Ecosystem radar

LightX2V public `main` advanced on 2026-09-01 to `fabd8fcad22b877ed332d567225b806c24ccd7be` (`Update LightX2V Studio models (#1468)`). Inspection of the exact commit shows only README/README_zh Studio-model advertising changes: the listed Studio examples changed to include MiniMax H3 and SwiftVR. It does not modify Wan2.2 I2V inference code, Hottop's reviewed command contract, runtime configuration, or model weights. Therefore freshness alone is not evidence for repinning the Hottop operator route.

Open LightX2V issue #1246 reports that a four-step Wan2.2 I2V distillation LoRA merge can leave image-conditioning weights such as `cross_attn.k_img`, `cross_attn.v_img`, and `img_emb` unmatched, with unused LoRA weights reported. That is directly relevant to reference-conditioned identity/action quality, so distilled/accelerated assets remain gated until the exact weight/config path is reviewed and demonstrates same-case rights-safe identity plus requested-action quality under Hottop's provenance gates.

No new model, LoRA, hosted service, dependency, network path, payment, or automatic download was introduced by this workstream.

## Doctrine and non-claims

`PROJECT.md` remains unchanged. Explicitly stripping this AWS secret is a narrower implementation of existing ZERO_COST, offline, least-authority, secret-safety, and fail-closed operator doctrine; it does not establish a new durable product direction.

The successful production/cinematic workflows validate the guaranteed software3d delivery path after the change. They do not claim that real LightX2V/Wan2.2 media was generated. The next meaningful reference-conditioned quality gate remains operator-provisioned real I2V media with complete media-integrity, identity, requested-action, and byte-bound provenance evidence.

## Rollback

Rollback is local and reversible: remove `AWS_SECRET_ACCESS_KEY` from the explicit credential denylist and remove its regression assertion. No persisted artifact schema, provider contract, model pin, or paid/network integration depends on this change.
