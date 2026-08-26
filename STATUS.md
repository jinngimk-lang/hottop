# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable real video output with measured artifact quality**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Current `main` is `6918b40144e98a63aa0400e9a232b888cc59eca6`.

Recent completed work:

- PR #89 made low-resolution cow + Odyssey final-MP4 seam quality a persistent production-smoke gate.
- `docs/decisions/2026-08-26-software3d-repeatability.md` records observed byte-repeatability across production-smoke #184 and post-merge #185 for the exact checked-in 360×640/12fps workflow/source/profile scope. The 720p evidence below is a direct counterexample to any broader bitwise-determinism interpretation.
- PR #93, **Gate 720p cinematic delivery seam quality**, was squash-merged as `593282ea6f605968658c210837bc43ecba648fd9`. RED CI #1734 failed exactly one new workflow contract (`1 failed / 499 passed`); GREEN exact-head CI #1735 passed on Python 3.11/3.12 and cinematic-delivery-smoke #31 passed the real 720×1280/24fps Odyssey chain.
- PR #94, **Record Qwen3-TTS serving benchmark provenance**, was squash-merged as `6918b40144e98a63aa0400e9a232b888cc59eca6` after exact-head CI #1738. It changes research/provenance expectations only; no runtime/provider/default TTS route changed.

Post-merge CI #1736 for the PR #93 production merge passed. Post-merge cinematic-delivery-smoke #32 also passed the real 720p24 Odyssey chain and the new persistent seam gate.

## Real artifact evidence — software3d

The guaranteed software3d route remains a real config → moving shots → Mandarin dialogue/original music/Foley → MoviePy → FFmpeg → verified MP4 path with byte-bound shot/final provenance.

### 360×640/12fps production baseline

The accepted cross-dissolve plus persistent seam gate currently enforces:

- max final-MP4 seam delta `<= 8.0`;
- max seam / intra-shot p95 ratio `<= 5.5`.

Production-smoke #184 measured cow max delta **4.431528** / ratio **3.622543**, and Odyssey max delta **5.196111** / ratio **3.038082**. Post-merge #185 passed the same gate. Across those two runs, final MP4 SHA-256 values were byte-identical within the exact tested scope:

- cow: `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`;
- Odyssey: `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`.

This is an observed result for those exact runs, not a universal requirement or guarantee.

### 720×1280/24fps cinematic delivery

Cinematic-delivery-smoke now runs the **same final-MP4 seam-quality contract continuously**, rather than relying on a one-time historical measurement.

Exact-head PR #93 smoke #31 produced:

- intra-shot p95: **0.933076**;
- seam deltas: **3.225000 / 4.127847 / 3.456250 / 4.178889**;
- max seam delta: **4.178889**;
- max seam/intra ratio: **4.478614**;
- final MP4 SHA-256: `a3895434d17b857f752cea05a14b46a2de6943f7e70158755c88589fe9da0222`;
- Actions artifact digest: `sha256:292e32d69628051dff1264050191903e5f0ff206c08910c5107f15b11031179a`;
- final media: H.264 / yuv420p, 720×1280, 24fps, AAC, 15.0s.

Post-merge smoke #32 produced:

- intra-shot p95: **0.933903**;
- seam deltas: **3.221250 / 4.145278 / 3.467778 / 4.184792**;
- max seam delta: **4.184792**;
- max seam/intra ratio: **4.480971**;
- final MP4 SHA-256: `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`;
- Actions artifact digest: `sha256:c664862b01b809fd7e759856478aed48dbda1370dc286e04bf51fa9f6058cda9`.

Both runs retain clear margin under the accepted seam thresholds, but **they are not byte-identical**. All five software3d shot artifact hashes also differ between #31 and #32 even though the video plan and checked runtime-provenance JSON are byte-identical. A decoded 90×160 grayscale comparison shows very small visual variance (mean absolute difference about **0.043/255**; about **0.31%** of sampled pixels differ by more than one level), so this is not currently a visible quality failure, but it is a reproducibility-provenance finding.

The two runs used the same GitHub runner image version and identical recorded FFmpeg/FFprobe/eSpeak/package/font identities but different hosted workers/regions (`westus3` for #31, `eastus` for #32). Current runtime provenance does not bind CPU model/hardware execution identity. Do **not** infer that CPU variance is the proven cause; it is an unbound dimension revealed by the counterexample.

The existing final-media verifier requires audio duration to cover the final video within 0.25s and rejects effectively silent audio, so a separate duplicate workflow-only audio-duration gate is not required.

The 720p proof remains a deterministic-code, presentable quality baseline with repeatable quality invariants, **not** a bitwise-deterministic delivery guarantee. It is also not a generated/reference-conditioned identity claim or the cinematic quality ceiling.

## Operator compute / generated-quality boundary

Canonical operator profile: `config/operator/dgx-spark-dual.yml`.
Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.
Model registry: `integrations/model-hub.yml`.

The declared two-node DGX Spark pool is preferred before paid SaaS, but Hottop does **not** infer runtime readiness. Driver/CUDA/PyTorch, disk/model paths and inter-node networking remain unverified until probe output from the actual operator hosts exists.

Priority generated-quality route remains reviewed local LightX2V + Wan2.2 I2V with rights-safe references, shared motion/quality/provenance gates and complete subject-bound continuity evidence. No automatic model download, GPU provisioning or paid fallback is admitted.

## Targeted ecosystem radar — 2026-08-26

- LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069` in the latest checked state. Its current MiniMax-H3 memory-residency optimization is opt-in and has no Hottop-measured benefit to the tested Wan2.2 route, so no freshness-only repin is admitted.
- Qwen3-TTS upstream remains on the reviewed operator-local path; there is still no operator-provisioned 1.7B same-line Mandarin A/B evidence that justifies replacing the guaranteed eSpeak-family fallback.
- Fresh public Qwen3-TTS serving benchmarks show that headline latency can depend on **local source patches or compatibility overrides**. `docs/research/2026-08-26-qwen3-tts-serving-provenance.md` records exact model/runtime/image/source identities for reviewed M*, vLLM-Omni and SGLang-Omni reports. Future Hottop acceleration evidence must bind patch/override identity and actual operator runtime, not only an upstream Git SHA. Those reports are primarily English throughput/latency evidence and do not prove Mandarin delivery quality.

No heavy dependency, automatic model download or new paid route is admitted from this scan.

## Guaranteed zero-cost baseline

The software3d → local Mandarin audio → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-download, zero-paid baseline. It includes:

- actual moving 3D geometry and story-specific staging;
- measured mobile framing and subtitle line-break quality;
- deterministic role-separated eSpeak-family dialogue and dialogue-aware ducking;
- geometric directional-light routing for lower-roughness cinematic profiles;
- controlled cross-shot dissolves with persistent seam-quality gates at both production-smoke and 720p cinematic-delivery surfaces;
- shot/final byte-bound provenance, pre-composition re-verification and final H.264/AAC/yuv420p media verification.

## Immediate next actions

1. Close the measured 720p reproducibility-provenance gap by binding CPU/hardware execution identity in cinematic-delivery runtime provenance. Use it to explain future cross-run differences; do not claim it caused #31/#32 without evidence.
2. Preserve quality-invariant repeatability as the production requirement; treat byte equality as additional observed evidence, not a universal success criterion.
3. Inspect fresh real cow/Odyssey MP4 evidence and improve only a **measured** visual/audio defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
4. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
5. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
6. Bind actual generator source revision, local patch/override identity where applicable, checkpoint provenance when independently available, exact reference bytes and shot hashes; require meaningful motion plus complete cross-shot continuity evidence before composition.
7. Run the existing role-aware Mandarin/audio/post chain and final H.264/AAC verification; visually reject slideshow motion, identity drift, broken geography or weak product/hotspot mapping.
8. Continue targeted ecosystem radar around the **measured current gap**. Do not add abstraction, freshness-only pins or large dependencies without measurable value and a rollback path.
9. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not creative defaults.

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
