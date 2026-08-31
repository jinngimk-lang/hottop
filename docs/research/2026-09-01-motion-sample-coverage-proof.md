# Motion sample coverage proof — 2026-09-01

## Gap

The generated-video motion gate already rejected rawvideo payloads with trailing partial frames, but a multi-second clip could still return only a small number of complete, frame-aligned samples from the beginning of the stream and be evaluated as if coverage were complete. Byte alignment proved sample framing, not temporal coverage.

## TDD change

PR #373 adds a fail-closed minimum sample-count check after exact raw `gray` frame alignment:

```text
expected_samples = max(2, int(duration * sample_fps) - 1)
```

The one-sample tolerance absorbs FFmpeg boundary/timestamp rounding while still rejecting severe early truncation. The change does not alter provider routing, models, network behavior, downloads, billing, ZERO_COST behavior, style routing, or compositor policy.

## Evidence

- RED `575092828db2d25f858fcf422483dd3145154c6a`: CI #2591 reached pytest after install + Ruff and failed the new regression on Python 3.11, proving the previous implementation accepted a four-second clip represented by only two complete sampled frames.
- GREEN `73ee202831efb998c1f151ec3a9a2c0799b68723`: exact-head CI #2592 passed Python 3.11 and 3.12 Ruff/full pytest.
- production-smoke #294 passed on the exact GREEN head; artifact `hottop-software3d-production-smoke` was 687,894 bytes, digest `sha256:583d4b66e4a183921554e4e5b0f16a810742c6cc435623c6ffaef73b6040de86`.
- cinematic-delivery-smoke #161 passed on the exact GREEN head; artifact `hottop-cinematic-software3d-delivery` was 624,449 bytes, digest `sha256:36e166a16a5ff495b00508f03b28ec7138cdb223c3f82ea0ffae5fc910cfec73`.
- PR #373 was SHA-locked squash-merged from that exact head as `ce7ce2c9b046b7d3090ba7db626b9cc567b1a21d`.

## Ecosystem implication

Fresh LightX2V issue evidence continues to show that successful inference, correct duration/frame count, decodability, or generic motion are insufficient evidence of useful I2V output. Open reports include static-frame I2V completion and degraded/meaningless Wan2.2 output. These are external warnings rather than Hottop benchmarks; Hottop therefore keeps identity fidelity, requested-action motion fidelity, semantic quality, media integrity, and provenance as separate fail-closed evidence dimensions.

No freshness-only LightX2V repin or new provider was admitted in this cycle. The measured next gate remains real operator-provisioned Wan2.2/LightX2V subject-bearing output.
