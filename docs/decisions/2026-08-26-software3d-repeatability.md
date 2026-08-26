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

Four successful real cinematic-delivery runs show why byte equality must remain **observed evidence**, not the production definition of repeatability.

- #29 on `main@c0474a070e7dffa272cc46c7351c780f5c58f2fb` produced final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.
- #31 on PR #93 exact head `abadcec84bab9de96e1eabb16f300b9887b91aef` produced final SHA-256 `a3895434d17b857f752cea05a14b46a2de6943f7e70158755c88589fe9da0222`.
- #32 on post-merge `main@593282ea6f605968658c210837bc43ecba648fd9` again produced `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.
- #38 on PR #97 exact production head `420301788aa4c6a967772ffdaeb175ee48a14335` again produced `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df` after CPU/hardware provenance capture was added.

Thus #29, #32 and #38 are byte-identical, but #31 is a counterexample to treating the 720p route itself as universally bitwise deterministic. All five software3d shot bytes in #31 differ from #32 even though the derived video plan and the then-recorded runtime-provenance JSON are byte-identical.

The important quality result is stable:

- #31 intra-shot p95 `0.933076`, max seam delta `4.178889`, max ratio `4.478614`;
- #32 intra-shot p95 `0.933903`, max seam delta `4.184792`, max ratio `4.480971`;
- #38 intra-shot p95 `0.933903`, max seam delta `4.184792`, max ratio `4.480971`.

All pass the persistent seam gate with margin. A decoded 90×160 grayscale comparison between #31/#32 has mean absolute difference about `0.043/255`; only about `0.31%` of sampled pixels differ by more than one level. The outputs are visually near-identical despite different encoded/shot bytes.

The older records bound the runner image plus package/FFmpeg/FFprobe/eSpeak/font identities but not CPU/hardware execution identity. PR #97 closes that evidence gap for future 720p runs. #38 records:

- machine `x86_64`;
- CPU `AMD EPYC 7763 64-Core Processor`;
- vendor `AuthenticAMD`;
- `/proc/cpuinfo` SHA-256 `e8c8a04bfd1dcda906a9b8e1116f3db8b87b00df7e0265072c3b0083a62a37d3`;
- Actions artifact digest `sha256:ec3cd28eebdb41b62ef9098f63918f0052e814879ddfa14d7a1a4cb61808869f`.

This proves new evidence can bind CPU identity. It does **not** prove CPU differences caused #31 because historical #31/#32 CPU identities were not captured. Different hosted workers/regions remain only a correlation.

There is also no reason to weaken production merely to chase a universal hash. FFmpeg's own community guidance notes that real multithreaded encoders are not generally expected to emit byte-identical output across runs, and NumPy selects CPU/SIMD kernels at runtime. Hottop therefore records the material environment and enforces real artifact quality/integrity instead of forcing single-threaded or otherwise degraded execution solely for bitwise identity.

### 2026-08-27 cross-CPU follow-up

PR #97 exact-head cinematic-delivery-smoke #41 and its post-merge main smoke #42 provide the first immediately comparable 720p runs where CPU identity is captured on both sides.

Both runs used the **same** derived `hottop-video-plan.json` SHA-256 `40d5b341e357572bfe10c4d9e0ba8bbc81038f31ba0b3b8f7467e94109b4031f`. Their recorded package versions, FFmpeg/FFprobe/eSpeak executable identities and caption-font identity are the same; the runtime-provenance diff is limited to CPU identity fields.

- #41 CPU: `AMD EPYC 9V74 80-Core Processor` / `AuthenticAMD`, `/proc/cpuinfo` SHA-256 `834f99405c6a7b1f13d93fc5bf45599e669d1e1ad2fdaacfe4b61eab1fd62bed`; final MP4 SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.
- #42 CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz` / `GenuineIntel`, `/proc/cpuinfo` SHA-256 `3eb16c7de185a902dff4f30e09295791d52ec77beab06b95bd942ef8dab2d6ed`; final MP4 SHA-256 `a3895434d17b857f752cea05a14b46a2de6943f7e70158755c88589fe9da0222`.

All five software3d shot hashes differ between #41 and #42, yet both pass the same quality/media gates. #41 seam metrics are intra p95 `0.933903`, max delta `4.184792`, ratio `4.480971`; #42 is `0.933076`, `4.178889`, `4.478614`. A 30-frame decoded 90×160 grayscale comparison has mean absolute difference about **`0.0425/255`**, with about **`0.324%`** of sampled pixels differing by more than one level.

This materially strengthens the interpretation that CPU/runtime execution identity can explain scoped byte variance while accepted visual quality remains stable. It still does **not** establish formal single-factor causality: hosted-runner execution includes details beyond the fields currently captured. The production rule therefore remains contract-first, with CPU identity retained as material provenance rather than a requirement for universal byte equality.

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

This supersedes the earlier wording that generalized the observed #29/#32 byte match into a 720p route-level byte-repeatability claim. It does not invalidate the actual #184/#185 or #29/#32/#38 byte-equality observations.

## Related evidence

- PR #87 — bounded in-place cross-dissolve.
- PR #89 — persistent production-smoke final-MP4 seam gate.
- production-smoke #184 / #185 — scoped 360p byte-equality evidence.
- cinematic-delivery-smoke #29 — earlier 720p delivery.
- PR #93 / cinematic-delivery-smoke #31 — persistent 720p seam gate, different-byte counterexample.
- cinematic-delivery-smoke #32 — post-merge 720p evidence.
- PR #97 / cinematic-delivery-smoke #38 — CPU-bound runtime provenance plus matching quality/hash evidence.
- cinematic-delivery-smoke #41 / #42 — same-plan, different-CPU follow-up with different shot/final bytes but near-identical decoded output and passing gates.
