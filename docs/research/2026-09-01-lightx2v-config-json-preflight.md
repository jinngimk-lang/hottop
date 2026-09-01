# LightX2V config JSON preflight — 2026-09-01

## Measured gap

Hottop's operator-owned LightX2V preflight previously proved that the configured JSON path existed, but it did not prove that the file was parseable JSON or that the root value was an object. A malformed file or a syntactically valid non-object payload such as `[]` could therefore survive local preflight and reach GPU probing/inference.

That is avoidable operator cost and weakens the fail-closed boundary: cheap deterministic config-shape failures should be rejected before any GPU work. The fix deliberately stops at a version-safe structural contract. It does **not** hard-code upstream fields such as `target_video_length`, because Hottop can admit different reviewed LightX2V revisions/configs and a field becomes mandatory only when the exact admitted runtime contract proves it is mandatory.

## TDD evidence

RED exact head: `cd165df41f49ccc839dd4f7f1084f4b1c6bf3108`.

CI on the RED commit reached the test suite and Python 3.12 failed the new regression proving malformed JSON was not rejected before the injected GPU probe. Python 3.11 was cancelled by fail-fast after the defect had already been demonstrated and is not counted as independent RED evidence.

GREEN exact head: `24d07cf602b2bea695694dd3f80ac3f633ded04e`.

The minimal production change resolves the configured JSON file, reads it as UTF-8, parses with `json.loads`, converts read/Unicode/JSON-decode failures into `LightX2VError`, and requires one top-level object. Both malformed JSON and a valid non-object root fail before GPU probing. Exact-head CI passed Ruff/full pytest on Python 3.11 and 3.12.

PR #400 was SHA-locked squash-merged as `a69fb29b8cda3df0b838e4f02fa0184070761a8f`.

## Exact-head production evidence

The GREEN head also passed both real-media workflows:

- production-smoke succeeded for the checked-in zero-cost software3d baseline and final-media/provenance verification. Artifact `hottop-software3d-production-smoke`: **687,895 bytes**, `sha256:916af766cda2195a0ab88a6df14212d53c2dbeb7ca9edd855f4099a9a3789e3d`.
- cinematic-delivery-smoke #195 completed the actual 720p24 Odyssey delivery, runtime provenance capture, final-media/provenance verification and artifact upload. Artifact `hottop-cinematic-software3d-delivery`: **624,451 bytes**, `sha256:923dc548c6d904a5207f5a3c24d9849644002a9968e3f0e7aa7bb4eedc31254b`.

No paid provider, model download, package auto-install, GPU provisioning or fallback behavior changed. `ZERO_COST_MODE=true` and the deterministic software3d guarantee remain unchanged.

## Ecosystem radar

LightX2V public `main` advanced to `d7e064c4ec8dfe6a545e139156498abb8c108a3e` on 2026-09-01 with `fix(mlu): make Sage attention compile safe (#1435)`. That is MLU/Sage Attention compiler/runtime maintenance, not same-case Wan2.2 I2V identity or requested-action quality evidence, so there is no freshness-only repin.

Open upstream #1086 reports a Wan2.2 I2V failure from a missing `target_video_length` config field. That supports doing cheap config validation before GPU work, but does not by itself justify making that field a universal Hottop requirement across independently reviewed LightX2V revisions. Existing reports of meaningless output, frozen I2V frames, quality regression versus Diffusers and image-conditioning LoRA key mismatches continue to justify keeping runtime/media integrity separate from identity/requested-action/semantic quality.

A separate zero-cost TTS radar candidate, `mingshi2333/Qwen3-TTS-ncnn@7c58a6756367e38abe19b0fc2639e56aa1e8bf74`, is Apache-2.0 and reports token-parity CustomVoice plus CPU/Vulkan execution for Qwen3-TTS 0.6B. It is **not admitted**: its default build can fetch ncnn, model conversion requires separately provisioned Qwen weights/source, it does not provide the current 1.7B CustomVoice target, and Hottop has no same-line Mandarin listening benchmark. Any future use must be an operator-provisioned, fail-closed local adapter with exact runtime/model provenance and no unattended downloads.

## Durable doctrine decision

`PROJECT.md` does not change. Parseable/object-shaped local config validation is a stricter implementation of existing ZERO_COST, local-preflight and fail-closed operator doctrine. The durable rule remains evidence-driven and version-safe: validate what the admitted runtime contract can prove, and do not turn one upstream issue or one revision's field set into a universal schema by assumption.

Rollback is narrow: revert the JSON parse/root-object preflight and its regressions. No artifact schema, provider routing or production baseline changed.
