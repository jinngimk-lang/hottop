# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — operator-local real cinematic-motion proof on the fail-closed multimodal model fabric**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

PR #86 was squash-merged to `main` as `3f04802c88027833e23b7e14a95592bfbf3ed6e3` after exact-head `f43710f3441e5c1fc3c7a45aeb367aaa9a9d8bff` passed CI #1714, production-smoke #177 and cinematic-delivery-smoke #24. The merge head then passed main CI #1715, and the status-sync head `4555698a40624c80adc35bc1798305f0e542c9e9` passed main CI #1716. There are no open PRs at this recovery point.

The merged capability is deliberately fail-closed: `integrations/model-hub.yml` is a machine-readable registry and `hottop-models list` is a read-only selector. DGX/local entries remain `unprobed` until an operator probe proves runtime readiness. The hub does not install upstream projects, download models, provision GPU, consume credits or turn paid/license-blocked entries into defaults.

## Declared local operator compute

Canonical profile: `config/operator/dgx-spark-dual.yml`.

The declared two-node NVIDIA DGX Spark pool is the preferred heavy-compute surface before paid SaaS, but Hottop does **not** treat aggregate physical memory as one automatic shared GPU address space. Driver/CUDA/PyTorch, disk, local model paths and inter-node networking remain unverified until `scripts/probe_dgx_spark.py` is run on each physical host.

Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.

## Production hierarchy remains above model routing

`fresh/supplied hotspot evidence → promotion objective → hotspot mechanism → product role/outcome change → script/beat sheet → character/world bible + identity locks → keyframes/style frames → model selection → real image/video generation → continuity review → voice/BGM/SFX → post/final media verification → campaign-effect review`

Model quality never substitutes for product relevance, hotspot mechanism, rights safety, character/world continuity or real motion. Cinematic requests cannot be satisfied by still-image pan/zoom. Anti-Polish roughness remains style-routed rather than a license for random failure.

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

Fresh checks do not justify changing the tested defaults. LightX2V remains actively maintained, but recent visible work is concentrated in InfiniteTalk cancellation, MiniMax-H3/model requests and other paths that do not yet provide Hottop evidence for a better Wan2.2 I2V default. MiniMax-H3 reports include incorrect/blocky video and garbled audio on an experimental Intel-XPU port, so model-request activity is not admission evidence. Qwen3-TTS serving work in SGLang-Omni is producing useful H100/H200 execution evidence, including removal of a Talker `torch.compile` path after it failed to show reproducible end-to-end gain; this reinforces Hottop's benchmark-before-optimization rule. No freshness-only repin, new heavy dependency or automatic model download is admitted from this scan.

## Guaranteed zero-cost baseline

The software3d → local Mandarin audio → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-download, zero-paid baseline. The checked-in 720×1280/24fps Odyssey delivery proof remains the deterministic presentable baseline with source-byte, shot-byte, final-media and codec evidence. It is not a generated/reference-conditioned identity claim and is not the cinematic quality ceiling.

## Immediate next actions

1. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines; keep private host/runtime details out of Git when appropriate.
2. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
3. Bind actual generator source revision, checkpoint provenance when independently available, exact reference bytes and shot hashes; require motion and complete cross-shot continuity evidence before composition.
4. Run the existing role-aware Mandarin/audio/post chain and final H.264/AAC verification; visually reject slideshow motion, identity drift, broken geography or weak product/hotspot mapping.
5. If operator runtime remains unavailable, continue improving only measured defects in the guaranteed software3d production path and continue targeted ecosystem radar; do not add abstraction or large dependencies without evidence.
6. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not creative defaults.

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
