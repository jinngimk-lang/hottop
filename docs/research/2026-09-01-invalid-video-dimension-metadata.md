# Invalid generated-video dimension metadata — 2026-09-01

## Measured gap

`inspect_video_quality()` converted ffprobe `width` and `height` with bare `int(...)`. A malformed/non-integer dimension therefore raised `ValueError` and crashed the quality inspector instead of returning a deterministic fail-closed rejection report. In unattended Production v0.2, corrupt or abnormal generated media must be rejected as evidence, not turn validation into an exception path.

## TDD evidence

- RED head `62784f0e9bc052d4de01c1a64f2bfee3b617a37d`, CI #2601: Python 3.11 completed installation + Ruff, then failed exactly the new regression with `1 failed, 642 passed`; traceback ended at `width = int(video.get("width") or 0)` for `width="not-a-number"`.
- GREEN head `c2feb7d73feadc3cf6940a79cdb87b50fdbd4c6f`, CI #2602: Python 3.11 and 3.12 Ruff/full pytest both passed.
- production-smoke #298 passed the checked-in anti-polish cow + cinematic Odyssey pipeline and final-media/provenance verification. Evidence artifact `hottop-software3d-production-smoke`: 687,894 bytes, digest `sha256:9d0c680393376c30697b31e1ff281d36fee46bb98ca19adaae04eb40344f8568`.
- cinematic-delivery-smoke #165 passed actual 720p24 Odyssey delivery, runtime provenance and final-media verification. Evidence artifact `hottop-cinematic-software3d-delivery`: 624,452 bytes, digest `sha256:250ddba8fc8499639cd124e1875e1fec6854b71f1860e9a15837aecf35b85e2f`.

## Change

Generated-video dimensions now use bounded parsing that catches `TypeError`, `ValueError` and `OverflowError`. Non-integer metadata is normalized to zero for the invalid dimension, reported as `video dimensions are invalid`, and rejected before terminal-frame or motion decoding. Valid integer dimensions keep the existing floor, terminal-byte, sampling, motion and duplicate checks unchanged.

## Doctrine / rollback

This is implementation hardening of the existing generated-media integrity doctrine, not a new project direction; `PROJECT.md` does not need to change. Rollback is the single PR #377 squash merge if later evidence shows an ffprobe representation that is valid but not integer-convertible; no provider, network, paid-service, model-download or ZERO_COST routing changed.

## Radar context

LightX2V public tip remained `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; its newest material commit was still SeedVR distributed-ops repair, with no Hottop-measured Wan2.2 I2V identity/requested-action gain. Open upstream reports #603, #895 and #1170 continue to show that successful execution, correct duration/frame count, or decodable MP4s can still have degraded, static, or meaningless content. No freshness-only repin or new dependency was admitted in this cycle.
