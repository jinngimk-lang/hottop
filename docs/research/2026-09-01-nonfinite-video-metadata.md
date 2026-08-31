# Non-finite generated-video metadata proof — 2026-09-01

## Gap

Generated-video quality inspection parsed ffprobe duration and average frame rate as Python floats without rejecting non-finite values. This created two fail-closed failures:

- `duration=nan` bypassed duration comparisons and later raised `ValueError` while converting the expected motion-sample count to `int`, turning malformed metadata into an inspector crash instead of a structured rejection;
- `fps=nan` made the minimum-fps comparison false and could allow an otherwise passing artifact to return `pass_=True` with non-finite frame-rate provenance.

## TDD evidence

- RED `56eec1901d1063803942c8ba3e016e841f485b0c`: CI #2596 completed installation and Ruff, then Python 3.11 failed exactly the two new regressions with `2 failed, 640 passed`. The duration case raised `ValueError: cannot convert float NaN to integer`; the fps case returned `pass_=True` with `fps=nan`.
- GREEN `092038246d8b41458d1fb192a54c5bde04d4d807`: the inspector now uses `math.isfinite` for duration and fps, records explicit `video duration is not finite` / `video fps is not finite` reasons, sanitizes report values to zero, and keeps all downstream threshold/sample-count logic finite.
- exact-head CI #2597 passed Python 3.11 + 3.12 Ruff/full pytest.
- production-smoke #296 passed checked-in anti-polish cow + cinematic Odyssey execution and final-media/provenance verification; artifact `hottop-software3d-production-smoke` was 687,895 bytes with digest `sha256:24f7eb3e92a0be10371ac9eceee1b6b2d7af86b584fa025f1eae8a4437342615`.
- cinematic-delivery-smoke #163 passed actual 720p24 Odyssey delivery, runtime provenance, final-media/seam verification and evidence upload; artifact `hottop-cinematic-software3d-delivery` was 624,449 bytes with digest `sha256:1d7aa075cff2947c7e1ad47ef44c9f8bbd9e29139460038c830439af549dbb9f`.
- PR #375 was SHA-locked squash-merged from the exact GREEN head as `76e64158aeefaac5e4ef9a74d4f0222e8debfee3`.

## Scope

This is a narrow implementation of the existing generated-media integrity doctrine. It does not alter provider selection, models, routing, networking, downloads, billing, ZERO_COST behavior, style routing, identity evaluation or composition policy.

`PROJECT.md` therefore does not change. The next material Production v0.2 gate remains real operator-provisioned LightX2V/Wan2.2 subject-bearing output with separate media, identity, requested-action and provenance evidence.
