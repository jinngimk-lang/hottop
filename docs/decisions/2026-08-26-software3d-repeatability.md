# Software3D repeatability evidence

Date: 2026-08-26
Milestone: Production v0.2
Status: accepted scoped evidence for the guaranteed software3d baseline

## Question

What does “repeatable” mean for Hottop's guaranteed software3d production route: stable quality invariants, or universal byte-for-byte identity?

## Evidence

### 360×640 / 12fps production-smoke

Production-smoke #184 (PR #89 exact head) and #185 (post-merge main) completed the real chain:

`software3d moving shots → local Mandarin dialogue → original synthetic music/Foley → MoviePy → FFmpeg → final-media/provenance verification → seam-quality measurement`

For those two runs, final MP4 bytes happened to be identical:

- cow: `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`;
- Odyssey: `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`.

The accepted final-MP4 seam gate also repeated within limits: `max_seam_delta <= 8.0`, `max_seam_ratio <= 5.5`.

### 720×1280 / 24fps Odyssey

Three successful real cinematic-delivery runs show why byte equality must remain **observed evidence**, not the production definition of repeatability.

- #29 on `main@c0474a070e7dffa272cc46c7351c780f5c58f2fb` produced final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.
- #31 on PR #93 exact head `abadcec84bab9de96e1eabb16f300b9887b91aef` produced final SHA-256 `a3895434d17b857f752cea05a14b46a2de6943f7e70158755c88589fe9da0222`.
- #32 on post-merge `main@593282ea6f605968658c210837bc43ecba648fd9` again produced `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.

Thus #29 and #32 are byte-identical, but #31 is a counterexample to treating the 720p route itself as universally bitwise deterministic. All five software3d shot bytes in #31 differ from #32 even though the derived video plan and the then-recorded runtime-provenance JSON are byte-identical.

The important quality result is stable across #31/#32:

- #31 intra-shot p95 `0.933076`, max seam delta `4.178889`, max ratio `4.478614`;
- #32 intra-shot p95 `0.933903`, max seam delta `4.184792`, max ratio `4.480971`.

Both pass the persistent seam gate with margin. A decoded 90×160 grayscale comparison between #31/#32 has mean absolute difference about `0.043/255`; only about `0.31%` of sampled pixels differ by more than one level. The outputs are visually near-identical despite different encoded/shot bytes.

The two runs used the same checked runner-image version and identical recorded package/FFmpeg/FFprobe/eSpeak/font identities, but different hosted workers/regions. The old runtime-provenance record did not bind CPU model/hardware execution identity. That is an evidence gap, **not proof that CPU differences caused the byte variance**.

## Decision

For Production v0.2, **repeatability is defined first by reproducible production contracts and measured final-artifact quality invariants**, not by universal byte equality.

Byte-identical outputs remain useful additional evidence when observed, but they are always scoped to the exact runs and bound runtime identities. A later non-identical output is not automatically a regression if the source/plan/provenance are valid and the accepted visual/audio/media gates still pass.

Therefore:

- keep software3d as the guaranteed zero-cost reproducible baseline;
- preserve exact shot/final byte binding on every run;
- measure real final MP4 quality, not only stage success;
- bind material runtime/hardware identity needed to interpret cross-run byte differences;
- never weaken visual/audio/media gates merely to preserve byte identity;
- keep neural/reference-conditioned routes behind their own real output and continuity evidence.

This supersedes the earlier wording that generalized the observed #29/#32 byte match into a 720p route-level byte-repeatability claim. It does not invalidate the actual #184/#185 or #29/#32 byte-equality observations.

## Related evidence

- PR #87 — bounded in-place cross-dissolve.
- PR #89 — persistent production-smoke final-MP4 seam gate.
- production-smoke #184 / #185 — scoped 360p byte-equality evidence.
- cinematic-delivery-smoke #29 — earlier 720p delivery.
- PR #93 / cinematic-delivery-smoke #31 — persistent 720p seam gate, different-byte counterexample.
- cinematic-delivery-smoke #32 — post-merge 720p evidence.
