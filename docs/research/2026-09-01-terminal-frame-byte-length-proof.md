# Complete terminal-frame byte proof — 2026-09-01

## Measured gap

Production v0.2 already required FFmpeg to return success and emit non-empty bytes for a decoded terminal frame. That was still weaker than the evidence format actually requested by the probe: one `rawvideo` frame in `gray` pixel format at the probed video dimensions.

For that contract, a complete frame is exactly `width × height` bytes. The previous `bool(stdout)` condition could therefore overstate integrity when a successful subprocess returned only a partial/truncated payload such as one byte.

## TDD evidence

- RED head: `f449a2002e81f91b2869f706153d1116ffcaebc8`.
- RED CI: #2581. Python 3.11 completed installation and Ruff successfully, then pytest failed on the new one-byte terminal-payload regression. This isolates the failure to the intended integrity contract rather than environment setup or lint noise.
- GREEN head: `6caa9d75013fdbabff30a3d2fe7bc2aac15b656b`.
- GREEN rule: `terminal_frame_decodable` now requires FFmpeg exit code 0, positive probed dimensions, and exactly `width × height` terminal bytes.
- GREEN CI: #2582 passed full Ruff/pytest on Python 3.11 and 3.12.
- production-smoke #290 passed the checked-in anti-polish cow and cinematic Odyssey executions plus final-media/provenance verification. Artifact `hottop-software3d-production-smoke` was 687,895 bytes with archive digest `sha256:f7d352373c86448080960b0d1d3dc022f095c9e3023a5c71aff9d1855cb38328`.
- cinematic-delivery-smoke #157 passed actual 720p24 Odyssey delivery, runtime provenance, final-media/seam verification and evidence upload. Artifact `hottop-cinematic-software3d-delivery` was 624,451 bytes with archive digest `sha256:261d9fc30ffd8ecb6ef3ee44afd8bcfa600e0060dcec85ab287e84fe5aa1f70c`.
- PR #369 was SHA-locked to the GREEN head and squash-merged as `b9a437e4ac4b588939cc0b76cb667b1d6a43c428`.

## Scope and rollback

This is a shared deterministic integrity tightening only. It does not change provider routing, model/runtime selection, generation parameters, network behavior, downloads, costs, the guaranteed software3d route, or style policy. Rollback is a single predicate/test change, but should only be considered if a conforming FFmpeg raw-gray probe can legitimately return a different byte count for one requested frame.

## Ecosystem radar

LightX2V public `main` remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` as of this check. Its latest material commit restores SeedVR distributed-op exports and reports SeedVR2 BF16/FP8 validation; it does not demonstrate a Hottop Wan2.2 I2V identity, requested-action, continuity, or cinematic-quality gain. Continue **no freshness-only repin**.

Open LightX2V issue #603 reports materially degraded Wan2.2 I2V resolution/content/realistic motion versus the authors' Diffusers implementation under reportedly comparable parameters. This is external issue evidence, not a benchmark result, but it strengthens the existing requirement that runtime success, decodability and generic motion never substitute for Hottop same-case identity/requested-action/semantic quality evidence.

No newly checked candidate clears the admission gate strongly enough to change the guaranteed route or auto-provision large assets.

## Doctrine decision

`PROJECT.md` remains unchanged. Requiring a complete raw terminal frame is a stricter implementation of the existing generated-media/final-media integrity doctrine, not a new durable product or architecture direction.

## Next gate

The real Production v0.2 gate remains operator-provisioned generated media: a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable NVIDIA GPU must generate at least two rights-safe subject-bearing I2V shots, with all subject-bearing shots passing media integrity/quality, identity, requested-action motion, full reference coverage and exact request/source/config/reference/generated-byte provenance before composition.