# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable real video output with measured artifact quality**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

PR #87, **Smooth deterministic software3d shot seams**, was squash-merged to `main` as `c0474a070e7dffa272cc46c7351c780f5c58f2fb` after exact-head `8e463e9ef1a73a56155658c5558840d6e4933cb2` passed CI #1721, production-smoke #181 and cinematic-delivery-smoke #28. The PR had no unresolved review threads and remained limited to deterministic `software3d` MoviePy composition.

The accepted transition is an in-place bounded cross-dissolve around existing shot boundaries. It does not insert black frames, change total duration, shift captions/dialogue/audio or alter provider/provenance/ZERO_COST behavior.

## Real artifact evidence — shot seams

Production-smoke #178 exposed abrupt hard-cut seam deltas around **10.5–12.3** for cow and **12.0–16.1** for Odyssey versus normal intra-shot p95 around **1.27 / 1.84**. A first fade-to-black attempt was rejected even though pipeline smoke passed because direct MP4 measurement worsened seam peaks to roughly **18.5–20.5 / 25.8–27.0**.

The final cross-dissolve implementation passed real artifact inspection:

- production-smoke #181 (360×640/12fps): cow seams **4.54 / 5.18 / 5.53 / 5.54**; Odyssey **4.76 / 6.49 / 5.57 / 5.78**;
- cinematic-delivery-smoke #28 (720×1280/24fps Odyssey): seams **3.46 / 4.56 / 3.79 / 4.34**;
- direct visual inspection shows short transparent blends rather than black flashes or unrelated hard cuts;
- total duration and dialogue/subtitle timing remain unchanged.

Seams remain deliberate transitions rather than ordinary intra-shot adjacent-frame motion. The durable lesson is unchanged: pipeline-green is not visual-quality proof; real MP4 inspection can reject a technically green artifact.

## Declared local operator compute

Canonical profile: `config/operator/dgx-spark-dual.yml`.

The declared two-node NVIDIA DGX Spark pool remains the preferred heavy-compute surface before paid SaaS, but Hottop does **not** infer current runtime readiness or treat aggregate physical memory as one automatic shared GPU address space. Driver/CUDA/PyTorch, disk, model paths and inter-node networking stay unverified until `scripts/probe_dgx_spark.py` is run on each physical host.

Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.

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

Fresh checks still do not justify changing tested defaults. LightX2V remains active and continues to expose Wan2.2 I2V examples, but recent visible work remains concentrated in InfiniteTalk maintenance and model-support requests rather than a Hottop-measured improvement to the tested Wan2.2 route. Wan2.2 upstream still has active packaging/community work but no evidence that should override Hottop's tested local subset.

Qwen3-TTS serving work in SGLang-Omni continues to reinforce benchmark-before-optimization: the current tracker records removal of Talker `torch.compile` after compile-off matched or exceeded compile-on under a fixed end-to-end protocol. No freshness-only repin, new heavy dependency or automatic model download is admitted from this scan.

## Guaranteed zero-cost baseline

The software3d → local Mandarin audio → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-download, zero-paid baseline. It now includes measured mobile framing, subtitle line-break quality, role-separated eSpeak-family dialogue, dialogue-aware ducking, geometric directional-light routing for lower-roughness cinematic profiles, byte-bound provenance, final-media verification and controlled cross-shot transitions.

The checked-in 720×1280/24fps Odyssey delivery proof remains the deterministic presentable baseline. It is not a generated/reference-conditioned identity claim and is not the cinematic quality ceiling.

## Immediate next actions

1. Verify post-merge `main@c0474a070e7dffa272cc46c7351c780f5c58f2fb` CI/production evidence when those runs appear; repair any regression before opening redundant work.
2. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines; keep private host/runtime details out of Git when appropriate.
3. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
4. Bind actual generator source revision, checkpoint provenance when independently available, exact reference bytes and shot hashes; require motion and complete cross-shot continuity evidence before composition.
5. Run the existing role-aware Mandarin/audio/post chain and final H.264/AAC verification; visually reject slideshow motion, identity drift, broken geography or weak product/hotspot mapping.
6. If operator runtime remains unavailable, continue improving only **measured** defects in real software3d MP4s and continue targeted ecosystem radar. Do not add abstraction or large dependencies without evidence.
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