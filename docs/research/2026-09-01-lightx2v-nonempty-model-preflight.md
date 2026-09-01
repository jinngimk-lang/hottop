# LightX2V non-empty local model provenance preflight — 2026-09-01

## Measured gap

Hottop already bound the recursively hashed local LightX2V model tree before and after generation, but an existing **empty** model directory still produced a deterministic SHA-256 and `0` total bytes. That digest was stable while proving no operator-owned model bytes were actually provisioned.

For an offline/fail-closed operator adapter, directory existence and a stable digest are therefore insufficient. The adapter must prove that at least one local model byte exists before GPU probing or inference can begin.

## TDD evidence

- RED `119ed1bd84d035ecee2a31999a46f1bf04a0b04e`: CI #2617 reached pytest after clean Ruff and Python 3.11 failed on `test_lightx2v_rejects_empty_local_model_tree_before_gpu_generation`; Python 3.12 was cancelled by fail-fast after the demonstrated failure.
- First GREEN implementation `3439331f7f79aa51b038cf08d833992e76eaf98f` added the fail-closed byte-count requirement. CI #2618 then exposed fixture debt: 15 existing tests represented a supposedly provisioned LightX2V model with an empty directory, so the new production contract correctly rejected those fixtures before their intended test boundary.
- Fixture repair made every test that claims a provisioned local model contain minimal non-empty local test bytes. The dedicated empty-model regression intentionally remains empty.
- Final exact head `4bc1e84d120a49b6013dc5851d7c651b0d2ef77d`: CI #2624 passed Ruff + full pytest on Python 3.11 and Python 3.12.
- production-smoke #311 passed on that exact head and uploaded `hottop-software3d-production-smoke`, 688,374 bytes, `sha256:bbef2b1bf25075cfaebca2640897cbb6211164116fedf5c727bd26847d343230`.
- cinematic-delivery-smoke #178 passed the actual 720p24 Odyssey delivery, runtime provenance and final-media verification on that same exact head; artifact `hottop-cinematic-software3d-delivery` was 623,328 bytes, `sha256:b0c86c6de56524eb0b7c5189f636153cf4d60a6bf533df5231b7feee783b4eab`.
- The verified implementation was SHA-locked squash-merged through PR #384 as `ecb6ecf57a577edecb8737e80fdd7a994f0b5de4`. Draft PR #383 was closed without code change only because the connected GitHub ready-for-review GraphQL mutation failed at the tool/schema layer; PR #384 reused the identical verified head.

## Implemented contract

`_model_tree_identity()` still hashes logical relative paths, declared file sizes and every local file byte. It now also requires `total_size > 0`; otherwise it raises `LightX2VError` with an operator-provisioning message.

Because model identity is captured before `gpu_probe()` inside `run_lightx2v_shot()`, an empty local model tree now fails **before GPU probe and before LightX2V invocation**. The existing post-generation model-tree recomputation remains in force, so mutation during inference still invalidates and deletes the output.

This change does not infer model legitimacy from a directory name, does not identify a weight revision by itself, and does not relax the requirement to record exact model-tree SHA-256/bytes. It only closes the false-positive case where a deterministic empty-tree digest could masquerade as evidence of provisioned model content.

## Zero-cost / security boundary

No provider route, network call, dependency, hosted inference, paid fallback, credit use, driver install, model download or automatic provisioning was introduced. Operators still provision reviewed LightX2V code, reviewed Wan2.2 model/config and suitable NVIDIA hardware themselves. Normal unattended `ZERO_COST_MODE=true` remains on the deterministic software3d path.

## Ecosystem radar

LightX2V public tip remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; its newest material change remains SeedVR distributed-ops repair rather than Hottop-measured Wan2.2 I2V identity or requested-action improvement. No freshness-only repin is justified.

Public LightX2V/Wan2.2 issue reports still warn that technically successful generation may yield degraded, static or meaningless content. Non-empty/stable model bytes therefore remain **provenance evidence only**; they do not substitute for media integrity, subject identity, requested-action motion or semantic correctness.

## Rollback

Revert PR #384. That restores acceptance of empty local model directories during model identity calculation; no schema migration, model asset, external service or paid resource is involved.

## Next proof

When a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable operator NVIDIA GPU are genuinely provisioned, generate at least two rights-safe subject-bearing I2V shots and require complete model/request/source/config/reference/generated-byte provenance plus media integrity, identity and requested-action quality across every subject-bearing shot before composition.
