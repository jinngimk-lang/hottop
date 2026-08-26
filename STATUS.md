# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable real video output with measured artifact quality**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

`main` is currently `593282ea6f605968658c210837bc43ecba648fd9` (**Gate 720p cinematic delivery seam quality**). Exact-head CI #1736 passed. The same head's cinematic-delivery-smoke #32 is currently executing the real 720×1280/24fps Odyssey delivery and will decide the new persistent 720p seam gate; do not claim that smoke green until the run completes.

There are currently no open pull requests on `main`. The guaranteed software3d route already has the bounded in-place cross-dissolve introduced by PR #87 and the 360p production-smoke seam gate from PR #89. The current main change extends the same real-final-MP4 measurement to cinematic delivery: `seam-quality.json`, `HOTTOP_SEAM_QUALITY`, `max_seam_delta <= 8.0`, and seam/intra-shot p95 ratio `<= 5.5` are now part of `.github/workflows/cinematic-delivery-smoke.yml`.

## Real artifact evidence — shot seams

The original hard cuts exposed seam deltas around **10.5–12.3** for cow and **12.0–16.1** for Odyssey versus normal intra-shot p95 around **1.27 / 1.84**. A fade-to-black experiment was rejected despite pipeline-green because direct MP4 measurement worsened peaks to roughly **18.5–20.5 / 25.8–27.0**.

The accepted cross-dissolve produced:

- production-smoke #181 (360×640/12fps): cow seams **4.54 / 5.18 / 5.53 / 5.54**; Odyssey **4.76 / 6.49 / 5.57 / 5.78**;
- cinematic-delivery-smoke #28 (720×1280/24fps Odyssey): seams **3.46 / 4.56 / 3.79 / 4.34**;
- production-smoke #184: persistent seam gate passed on both final MP4s; archived evidence measured cow max delta **4.43** / ratio **3.62** and Odyssey max **5.20** / ratio **3.04**;
- post-merge production-smoke #185: the persistent gate passed again on `main`;
- current `main@593282ea...`: 720p cinematic delivery now carries the same explicit seam gate in workflow code; cinematic-delivery-smoke #32 is the exact-head real-artifact verification still in progress.

The durable lesson remains: pipeline-green is not visual-quality proof; real MP4 inspection and measured artifact contracts can reject technically valid output.

## Repeatability evidence

`docs/decisions/2026-08-26-software3d-repeatability.md` records observed byte-repeatability for the checked-in cow and Odyssey software3d production runs. This is scoped evidence, not a universal cross-platform bitwise-determinism claim. Changes to render/config/runtime/toolchain that can affect bytes must establish their own evidence.

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

- LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069` as of the latest exact check, with an opt-in MiniMax-H3 DiT pre/post residency optimization. It does not change default behavior and has no Hottop-measured gain for the tested Wan2.2 route, so no freshness-only repin is admitted.
- Wan2.2 ecosystem reports continue to show that successful execution can still produce smeared/mosaic/corrupted output under some backend/runtime combinations. This reinforces Hottop's generated-artifact quality/provenance gates rather than motivating a blind backend switch.
- Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; there is still no operator-provisioned 1.7B same-line A/B evidence that justifies replacing the guaranteed eSpeak-family fallback or changing the reviewed Qwen adapter.
- Community local MiniMax-H3/LTX wrappers remain research candidates only until code/model/output rights, hidden download/runtime behavior, hardware practicality and Hottop-measured value pass admission. No heavy dependency or automatic model download is admitted from this scan.

## Guaranteed zero-cost baseline

The software3d → local Mandarin audio → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-download, zero-paid baseline. It includes:

- actual moving 3D geometry and story-specific staging;
- measured mobile framing and subtitle line-break quality;
- deterministic role-separated eSpeak-family dialogue and dialogue-aware ducking;
- geometric directional-light routing for lower-roughness cinematic profiles;
- controlled cross-shot dissolves with persistent real-final-MP4 seam gates;
- shot/final byte-bound provenance, pre-composition re-verification and final H.264/AAC/yuv420p media verification.

The checked-in 720×1280/24fps Odyssey delivery proof remains a deterministic presentable baseline. It is not a generated/reference-conditioned identity claim and is not the cinematic quality ceiling.

## Immediate next actions

1. Finish cinematic-delivery-smoke #32 on exact `main@593282ea...`; if it fails, repair the measured 720p seam regression before opening unrelated work. If it passes, record the exact real-artifact metrics and keep the gate.
2. Inspect fresh real cow/Odyssey MP4 evidence and improve only a **measured** visual/audio defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
3. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
4. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
5. Bind actual generator source revision, checkpoint provenance when independently available, exact reference bytes and shot hashes; require meaningful motion plus complete cross-shot continuity evidence before composition.
6. Run the existing role-aware Mandarin/audio/post chain and final H.264/AAC verification; visually reject slideshow motion, identity drift, broken geography or weak product/hotspot mapping.
7. Continue targeted ecosystem radar around the **measured current gap**. Do not add abstraction, freshness-only pins or large dependencies without measurable value and a rollback path.
8. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not creative defaults.

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
