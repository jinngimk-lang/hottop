# Generated-media output floor — 2026-09-01

## Measured gap

The shared generated-video quality gate already rejected missing/empty media, missing video streams, zero duration, invalid dimensions, terminal decode failure, insufficient observable motion, and excessive duplicate frames. It did not enforce a minimum non-zero media shape. A moving clip that was only 96×64, 0.2 seconds long, and 4 fps could therefore satisfy the old checks and be treated as compositor-usable generated media.

That was a real Production v0.2 evidence gap: successful inference plus generic motion is not enough if the returned artifact is implausibly small, short, or low-frame-rate for a moving-shot pipeline.

## TDD evidence

RED commit: `d99f4fdf6da56db9e6a1c823f5dbdeff8aa6c60e`.

CI #2571 reached pytest failure on both Python 3.11 and Python 3.12 after dependency installation and Ruff succeeded. The new regression case deliberately supplied a valid video stream, decodable terminal frame, and changing sampled frames while advertising only 96×64, 0.2 s, 4 fps metadata. This isolated the missing output-floor contract rather than motion/decode behavior.

GREEN exact head: `13a900a5a6027f7f36abf2db782ee8a6cd5e511a`.

`VideoQualityPolicy` now has conservative shared defaults:

- minimum duration: 0.5 s;
- minimum width: 256 px;
- minimum height: 256 px;
- minimum frame rate: 8 fps.

These are fail-closed compositor-usability floors, not target delivery geometry. Cinematic profiles may still generate or compose at larger resolutions such as 720×1280/24 fps, and MoviePy/FFmpeg may still perform later scaling. Style routing does not waive basic media integrity.

## Exact-head production verification

On GREEN head `13a900a5a6027f7f36abf2db782ee8a6cd5e511a`:

- CI #2572: Python 3.11 and 3.12 jobs both completed successfully, including Ruff and the full pytest suite;
- production-smoke #286: completed successfully, including checked-in anti-polish cow and cinematic Odyssey execution, final-media/provenance verification, and evidence upload. Artifact `hottop-software3d-production-smoke` was 687,894 bytes with archive digest `sha256:758597fb2597e70b1d3446255a197b50e63c0fcda438b3b9f920d445af3dc9b9`;
- cinematic-delivery-smoke #153: completed successfully, including actual 720×1280/24 fps Odyssey delivery, runtime provenance capture, final media/provenance verification, seam-quality checks, and evidence upload. Artifact `hottop-cinematic-software3d-delivery` was 624,450 bytes with archive digest `sha256:f548b98770b9090dbdc5d7408d424e90448521a8857a6c5a8b2e7582ebdcd7b2`.

PR #365 was SHA-locked squash-merged from that exact head as `3a9e8e1d1103229564b4b7f049c775396a356788`.

## Zero-cost and routing impact

No provider routing, model provisioning, network behavior, credentials, paid fallback, driver installation, or large model download was added. `ZERO_COST_MODE=true` and the guaranteed software3d path are unchanged.

## Ecosystem radar

ModelTC/LightX2V public tip remained `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` during this cycle. Its latest material change repairs SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it does not provide Hottop-measured Wan2.2 I2V identity or requested-action quality improvement. Continue **no freshness-only repin**.

A specialized Wan2.2 acceleration fork also surfaced with aggressive quantization/4-step claims, but it depends on a compound set of external model/LoRA/compiled assets. Until exact code/weights/artifact licenses and provenance are reviewed as one runtime bundle and Hottop obtains a same-case quality benchmark, it remains gated: no vendoring, auto-install, or multi-GB download.

Community Qwen3-TTS lower-hardware ports remain benchmark candidates only. Routes that auto-download model-family weights conflict with the unattended no-auto-download invariant unless the operator has already provisioned and pinned the required assets locally.

## Next gate

The real LightX2V/Wan2.2 gate remains operator-provisioned generated media: a reviewed local checkout, exact model/config, suitable NVIDIA GPU, and at least two rights-safe subject-bearing I2V shots that pass media quality, identity fidelity, requested-action motion fidelity, complete reference coverage, exact request/source/config/reference provenance, and composition/final-media verification.
