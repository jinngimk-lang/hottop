# Complete motion-sample payload integrity — 2026-09-01

## Measured gap

The shared generated-video gate already required complete terminal-frame bytes, but its separate motion sampler still accepted a weaker framing contract. FFmpeg emits sampled `rawvideo` in `gray` format at `sample_width × sample_height`, so every sample frame is exactly `sample_width × sample_height` bytes.

The previous implementation extracted every complete frame and silently ignored any trailing bytes. A successful FFmpeg process returning two complete sample frames plus one truncated byte could therefore still produce a passing motion report. That overstates evidence integrity because the sampler cannot distinguish a cleanly framed rawvideo stream from a truncated/corrupt tail merely by discarding the remainder.

## TDD evidence

- RED head: `93c5aac662a6c578a94a4cbdd19441f6affb47be`.
- RED CI: #2586. Installation and Ruff succeeded, then Python 3.11 pytest failed exactly on `test_inspect_video_quality_rejects_partial_motion_sample_payload` with `1 failed, 638 passed`; the old implementation returned `pass_=True`, `frame_count=2`, `mean_motion_delta=10.0`, and no reasons for a payload containing two complete 96×54 gray frames plus one trailing byte.
- GREEN head: `97ac5f6fae35bc71fee4469ea533db64bb0aeac3`.
- GREEN rule: when the sampling FFmpeg process succeeds, its rawvideo stdout length must be an exact multiple of `sample_width × sample_height`. Any remainder fails closed with `motion sample payload incomplete`; partial bytes are never interpreted or silently discarded.
- GREEN CI: #2587 passed full Ruff/pytest on Python 3.11 and 3.12.
- production-smoke #292 passed checked-in anti-polish cow + cinematic Odyssey execution and final-media/provenance verification. Artifact `hottop-software3d-production-smoke` was 687,894 bytes with archive digest `sha256:106f9fdf0eeff5cc88ec1232b0a7ea45d32a717e235725cffb9585031285d7c2`.
- cinematic-delivery-smoke #159 passed actual 720p24 Odyssey delivery, runtime provenance, final-media/seam verification and evidence upload. Artifact `hottop-cinematic-software3d-delivery` was 624,448 bytes with archive digest `sha256:842de6346b627e371db67234471b9563297ab0da798e25e6eb6b4b32345d7617`.
- PR #371 was SHA-locked to the GREEN head and squash-merged as `15d0d1832bbbb8292fb35a3a12f5b37c2b311899`.

## Scope and rollback

This is a narrow shared integrity tightening. It does not change provider routing, generated-video backends, model/runtime selection, generation parameters, network behavior, downloads, costs, deterministic software3d visuals/audio, or style policy. Rollback is isolated to the sampling payload-framing predicate and its regression test, and should only be considered if conforming FFmpeg rawvideo output can legitimately terminate with a non-frame-aligned payload while still constituting trustworthy motion evidence.

## Ecosystem radar

LightX2V public `main` remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` during this production cycle. Its latest material work restores SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it does not demonstrate a Hottop-measured Wan2.2 I2V identity, requested-action, continuity or cinematic-quality improvement. Continue **no freshness-only repin**.

Public LightX2V issue evidence continues to show why transport/runtime success is insufficient: issue #603 reports Wan2.2 I2V resolution/content/realistic-motion degradation versus a Diffusers implementation under reportedly comparable parameters, and issue #1170 reports a Wan2.2-TI2V-5B run producing meaningless color-block/light-pattern output. These are external reports, not Hottop benchmarks, but they reinforce the existing separation between media integrity, generic motion, identity fidelity, requested-action fidelity and semantic quality.

No newly checked candidate clears admission strongly enough to replace the guaranteed software3d route, repin LightX2V solely for freshness, or justify unattended large-asset provisioning.

## Doctrine decision

`PROJECT.md` remains unchanged. Exact motion-sample framing is a stricter implementation of the existing generated-media/final-media integrity doctrine, not a new durable product or architecture direction.

## Next gate

The real Production v0.2 gate remains operator-provisioned generated media: a reviewed local LightX2V checkout, exact Wan2.2 model/config and suitable NVIDIA GPU must generate at least two rights-safe subject-bearing I2V shots. Every subject-bearing shot must pass byte-bound media integrity/quality, identity, requested-action motion, complete reference coverage, and exact request/source/config/reference/generated-byte provenance before composition.