# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable real video output with measured artifact quality**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

PR #89, **Gate software3d shot seam quality**, was squash-merged to `main` as `485318a9e299f212729b9b2cf71c5b8a9d47a115` after exact-head `22908f8afa8765f48033281e83b25160bd335d20` passed CI #1726 and production-smoke #184 with no unresolved review threads.

The guaranteed software3d route now has both the bounded in-place cross-dissolve introduced by PR #87 and a real-artifact production gate that measures final cow + Odyssey MP4 seam deltas. Production-smoke writes `seam-quality.json`, logs `HOTTOP_SEAM_QUALITY`, and fails when `max_seam_delta > 8.0` or seam/intra-shot p95 ratio exceeds 5.5. This converts the prior one-time visual improvement into a regression contract without changing renderer/provider/provenance/cost behavior.

Post-merge production-smoke #185 for `main@485318a9...` completed successfully. PR #90 then refreshed this execution snapshot; its merge head `bf8709fe4dbc2377c941c6deab6dfaba26378ebe` passed post-merge CI #1729.

## Real artifact evidence — shot seams

The original hard cuts exposed seam deltas around **10.5–12.3** for cow and **12.0–16.1** for Odyssey versus normal intra-shot p95 around **1.27 / 1.84**. A fade-to-black experiment was rejected despite pipeline-green because direct MP4 measurement worsened peaks to roughly **18.5–20.5 / 25.8–27.0**.

The accepted cross-dissolve produced:

- production-smoke #181 (360×640/12fps): cow seams **4.54 / 5.18 / 5.53 / 5.54**; Odyssey **4.76 / 6.49 / 5.57 / 5.78**;
- cinematic-delivery-smoke #28 (720×1280/24fps Odyssey): seams **3.46 / 4.56 / 3.79 / 4.34**;
- production-smoke #184: the new persistent seam gate passed on both real final MP4s; archived seam evidence measured cow max delta **4.43** / ratio **3.62** and Odyssey max delta **5.20** / ratio **3.04**;
- post-merge production-smoke #185: the same persistent gate passed again on `main`.

The durable lesson remains: pipeline-green is not visual-quality proof; real MP4 inspection and measured artifact contracts can reject technically valid output.

## Declared local operator compute

Canonical profile: `config/operator/dgx-spark-dual.yml`.
Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.

The declared two-node NVIDIA DGX Spark pool remains the preferred heavy-compute surface before paid SaaS, but Hottop does **not** infer runtime readiness or treat aggregate physical memory as one automatic shared GPU address space. Driver/CUDA/PyTorch, disk, model paths and inter-node networking remain unverified until `scripts/probe_dgx_spark.py` runs on the actual hosts. Private host/runtime details should stay out of Git where appropriate.

## One-stop multimodal model hub

Canonical registry: `integrations/model-hub.yml`.
Safe discovery surface: `hottop-models list`.

Priority remains:

1. LightX2V + Wan2.2 I2V A14B for reviewed local reference-conditioned motion.
2. LightX2V Wan2.2 NVFP4 sparse Blackwell as a benchmark candidate, not an assumed speedup.
3. Wan2.2 TI2V/Animate/S2V for real motion, character animation and speech-driven motion when separately provisioned and rights-cleared.
4. Qwen-Image for keyframe/image work and Qwen3-TTS 1.7B CustomVoice for operator-local Mandarin delivery benchmarks.
5. Real-ESRGAN/RIFE only for restoration/interpolation; neither may masquerade as a motion generator.
6. ComfyUI/WanGP and other external stacks remain isolated interop candidates under their own license/runtime gates.

Popularity or freshness alone is not admission evidence. Code license remains separate from weights/model/data/output rights.

## Targeted ecosystem radar — 2026-08-26

Fresh checks still do not justify changing tested defaults.

- LightX2V `main` moved to `b220e26198fc90769114b6751236be96a3838069` on 2026-08-26 with an opt-in MiniMax-H3 memory-residency optimization that keeps DiT pre/post weights on the accelerator while transformer blocks use block offload. It does not change default behavior and is not a Hottop-measured improvement to the tested Wan2.2 route, so no freshness-only repin is admitted.
- Wan2.2 upstream remains active, including packaging/community work, but no current change demonstrates a Hottop-measured gain over the tested local subset. A June 2026 SGLang issue documented mosaic/corrupted Wan2.2 T2V output on one native backend while Diffusers produced correct output, reinforcing Hottop's rule that successful execution is not sufficient quality proof.
- Qwen3-TTS ecosystem work continues, including GPU-serving/optimization experiments, but there is still no operator-provisioned 1.7B same-line A/B evidence that justifies replacing the guaranteed eSpeak-family fallback or changing the reviewed Qwen adapter.

No heavy dependency, automatic model download or new paid route is admitted from this scan.

## Guaranteed zero-cost baseline

The software3d → local Mandarin audio → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-download, zero-paid baseline. It includes:

- actual moving 3D geometry and story-specific staging;
- measured mobile framing and subtitle line-break quality;
- deterministic role-separated eSpeak-family dialogue and dialogue-aware ducking;
- geometric directional-light routing for lower-roughness cinematic profiles;
- controlled cross-shot dissolves with a persistent seam-quality gate;
- shot/final byte-bound provenance, pre-composition re-verification and final H.264/AAC/yuv420p media verification.

The checked-in 720×1280/24fps Odyssey delivery proof remains a deterministic presentable baseline. It is not a generated/reference-conditioned identity claim and is not the cinematic quality ceiling.

## Immediate next actions

1. Inspect fresh real cow/Odyssey MP4 evidence and improve only a **measured** visual/audio defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
3. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
4. Bind actual generator source revision, checkpoint provenance when independently available, exact reference bytes and shot hashes; require meaningful motion plus complete cross-shot continuity evidence before composition.
5. Run the existing role-aware Mandarin/audio/post chain and final H.264/AAC verification; visually reject slideshow motion, identity drift, broken geography or weak product/hotspot mapping.
6. Continue targeted ecosystem radar around the **measured current gap**. Do not add abstraction, freshness-only pins or large dependencies without measurable value and a rollback path.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable creative/video skills.
4. `docs/operations/dgx-spark-local-model-fabric.md`, `config/operator/dgx-spark-dual.yml`, `integrations/model-hub.yml`.
5. newest relevant benchmark/spec/decision/research record.
6. current `main`, open PRs and exact-head CI/production evidence.
7. targeted ecosystem scan for the measured gap.
8. fresh hotspot/mechanism analysis for new creative generation.
9. continue the highest-value safe action autonomously.
