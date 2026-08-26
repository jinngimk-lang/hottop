# Hottop Status

Last updated: 2026-08-27
Active workstream: **Production v0.2 — measured repeatability + generated-quality readiness**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

`main` is `98aa1534c7b249f5a740a2c0b7c5cd751d46c2b2`, squash-merged from PR #98 **Sync repeatability doctrine and runtime status** after PR #97.

PR #97 exact head `8538d7b5515f7300528dd7fd82c72a52826d8e4a` passed:

- CI #1753;
- cinematic-delivery-smoke #41.

PR #97 post-merge `main@baa5888f...` CI #1754 **and cinematic-delivery-smoke #42** both passed. PR #98 exact-head CI #1755 passed, and its post-merge `main@98aa1534...` CI #1756 passed on Python 3.11/3.12. PR #98 was docs-only and did not alter renderer/runtime/provider/quality-threshold behavior.

There are no unresolved PR comments/review threads from #97.

## Durable repeatability correction

`docs/decisions/2026-08-26-software3d-repeatability.md` is the detailed evidence record. The canonical rule is now also in `PROJECT.md`:

**Production repeatability is quality-contract-first, not hash-first.**

The 720×1280/24fps Odyssey evidence includes successful runs #29/#31/#32/#38. #29/#32/#38 produced the same final MP4 SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`; #31 produced different shot/final bytes while remaining visually near-identical and passing the same seam/media/integrity gates. Therefore:

- reproducible visual/audio/media/integrity contracts are the hard success definition;
- shot/final bytes remain bound on every run;
- byte equality is useful additional **scoped observed evidence**, not a universal route-level requirement;
- material runtime/hardware identity is bound so later differences can be interpreted;
- Hottop does not degrade quality or throughput solely to chase a universal hash.

PR #97 added CPU runtime provenance for future 720p evidence: `platform.machine()`, first-processor model/vendor and SHA-256 of complete `/proc/cpuinfo` bytes. Its successful #38 proof recorded `x86_64 / AMD EPYC 7763 64-Core Processor / AuthenticAMD` plus `/proc/cpuinfo` SHA-256 `e8c8a04bfd1dcda906a9b8e1116f3db8b87b00df7e0265072c3b0083a62a37d3`. This does not retroactively prove CPU variance caused #31 because historical #31/#32 CPU identities were not captured.

## Guaranteed zero-cost baseline

The software3d → local Mandarin dialogue → original synthetic music/Foley → MoviePy → FFmpeg path remains the guaranteed zero-GPU, zero-model-download, zero-paid baseline. Current production contracts include:

- moving story-specific 3D geometry rather than slideshow placeholders;
- mobile principal-subject scale/placement and CJK subtitle readability/line-break gates;
- role-separated eSpeak-family dialogue plus delivery-aware cadence and BGM ducking;
- lower-roughness directional-light routing;
- bounded cross-shot dissolves with real-final-MP4 seam gates;
- shot/final byte-bound provenance and pre-composition re-verification;
- H.264/yuv420p + AAC final-media verification;
- CPU/hardware runtime identity for new 720p delivery evidence.

The software3d baseline is production evidence and a guaranteed fallback, not a cinematic/generated quality ceiling.

## Operator compute / generated-quality boundary

Canonical operator profile: `config/operator/dgx-spark-dual.yml`.
Durable spec: `docs/operations/dgx-spark-local-model-fabric.md`.
Model registry: `integrations/model-hub.yml`.

The declared DGX Spark pool is preferred before paid SaaS, but Hottop does **not** infer readiness from declaration. Driver/CUDA/PyTorch, disk/model paths and inter-node networking remain unverified until the probe runs on the actual hosts.

The highest-value generated-quality proof remains a rights-safe reference-conditioned LightX2V/Wan2.2 benchmark with at least two subject-bearing Odyssey I2V shots, exact generator source/model/reference/shot provenance, meaningful motion and complete subject-bound continuity evidence before composition. No automatic model download, GPU provisioning or paid fallback is admitted.

## Mandarin TTS boundary

The eSpeak-family route remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B is not allowed to silently discard `delivery`/`instruct` semantics.

A real same-line 1.7B Mandarin A/B still requires an already-provisioned local model/runtime. Preset speaker/output publication rights remain a separate operator review boundary from repository/model licensing.

## Targeted ecosystem radar — 2026-08-27

Fresh exact checks do not justify changing tested defaults:

- ModelTC/LightX2V `main` is `b220e26198fc90769114b6751236be96a3838069`. The latest visible change keeps MiniMax-H3 DiT pre/post weights resident behind an opt-in setting; default behavior is unchanged and Hottop has no measured gain for the tested Wan2.2 path. **No freshness-only repin.**
- Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no upstream change removes the need for a real operator-provisioned 1.7B Mandarin benchmark.
- Recent CosyVoice3 ecosystem correctness reports around TensorRT FP16 non-finite audio and streaming device mismatch reinforce candidate-only status; they do not justify replacing the guaranteed fallback or reviewed Qwen route without a Hottop benchmark.

No heavy dependency, automatic model download or paid route is admitted from this scan.

## Immediate next actions

1. Inspect fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
3. Once a reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
4. Bind actual generator source revision, local patch/override identity when applicable, checkpoint provenance when independently available, exact reference bytes and shot hashes; require meaningful motion plus complete cross-shot continuity evidence before composition.
5. When the operator-local Qwen3-TTS 1.7B runtime is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
6. Continue targeted ecosystem radar around the measured gap. Do not add abstraction, freshness-only pins or large dependencies without measurable value and a rollback path.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable creative/video skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
