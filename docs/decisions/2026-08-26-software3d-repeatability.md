# Software3D repeatability evidence

Date: 2026-08-26
Milestone: Production v0.2
Status: accepted evidence for the guaranteed deterministic baseline

## Question

Does the guaranteed software3d production path merely pass twice, or can it reproduce the same final delivery bytes under the same checked-in workflow/source conditions?

## Evidence

The seam-quality work was executed first on PR #89 exact head `22908f8afa8765f48033281e83b25160bd335d20` in production-smoke #184 and then again after squash-merge on `main@485318a9e299f212729b9b2cf71c5b8a9d47a115` in production-smoke #185.

Both runs completed the real production chain for the checked-in cow and Odyssey fixtures:

`software3d moving shots → local Mandarin dialogue → original synthetic music/Foley → MoviePy → FFmpeg → final-media/provenance verification → seam-quality measurement`

The uploaded final MP4 SHA-256 values were identical between the two independent workflow runs:

| Case | production-smoke #184 | production-smoke #185 |
| --- | --- | --- |
| cow | `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5` | `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5` |
| Odyssey | `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c` | `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c` |

The final seam evidence was also identical:

### Cow

- intra-shot p95: `1.223319`
- seam deltas: `3.852847 / 4.403750 / 4.420903 / 4.431528`
- max seam delta: `4.431528`
- max seam/intra ratio: `3.622543`

### Odyssey

- intra-shot p95: `1.710326`
- seam deltas: `3.847431 / 5.196111 / 4.356736 / 4.919444`
- max seam delta: `5.196111`
- max seam/intra ratio: `3.038082`

Both runs passed the persistent production gate (`max_seam_delta <= 8.0`, `max_seam_ratio <= 5.5`).

## Decision

Within this exact checked-in GitHub Actions/source/profile scope, Hottop may describe the guaranteed software3d route as **byte-repeatable in the observed repeated production runs**, not merely playable or pipeline-green.

This evidence does **not** claim universal bitwise determinism across arbitrary OS/FFmpeg/Python/library versions, hardware, future dependency releases or different production configs. Any change to render/config/runtime/toolchain that can affect bytes must establish its own evidence rather than inheriting this result.

The production principle remains:

- use the deterministic software3d route as the guaranteed zero-cost reproducible baseline;
- measure real final MP4 artifacts, not only stage success;
- preserve byte/provenance binding;
- keep stronger neural/reference-conditioned routes behind their own real output/continuity evidence;
- do not weaken quality gates merely to preserve byte identity.

## Related evidence

- PR #87 — bounded in-place cross-dissolve for deterministic software3d composition.
- PR #89 — persistent final-MP4 seam quality gate.
- production-smoke #184 — exact PR-head production evidence.
- production-smoke #185 — post-merge `main` production evidence.
