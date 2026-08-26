# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — measured repeatability + runtime provenance**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Recovery base `main` for this workstream is `49c89a08e6e5eab08deed833638ce80e520b62eb`.

Recent completed work:

- PR #89 made low-resolution cow + Odyssey final-MP4 seam quality a persistent production-smoke gate.
- PR #93 added the same persistent real-final-MP4 seam gate to the 720×1280/24fps cinematic-delivery workflow. RED CI #1734 failed exactly one new contract; exact-head CI #1735 and real cinematic-delivery-smoke #31 passed; post-merge CI #1736 and smoke #32 passed.
- PR #94 persisted Qwen3-TTS serving benchmark provenance, including model/runtime/image/source identities and the fact that public headline latency can depend on local source patches or compatibility overrides. It changed no runtime/default TTS route.
- Concurrent main work recorded #29/#32 720p byte-equality evidence. The complete #29/#31/#32 set below narrows that interpretation.

## Real artifact evidence — software3d

The guaranteed software3d route remains a real config → moving shots → Mandarin dialogue/original music/Foley → MoviePy → FFmpeg → verified MP4 path with byte-bound shot/final provenance.

### Quality repeatability is the hard contract

Persistent final-MP4 seam limits are:

- `max_seam_delta <= 8.0`;
- `max_seam_ratio <= 5.5` against intra-shot p95 motion.

The 360×640/12fps production-smoke and 720×1280/24fps cinematic-delivery paths both enforce those limits. Final-media verification also requires valid H.264/yuv420p + AAC, audio coverage within 0.25s of video duration and non-silent delivery.

### Scoped byte-equality observations

Production-smoke #184/#185 produced byte-identical final MP4s within that exact scope:

- cow: `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`;
- Odyssey: `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`.

For the 720p Odyssey route:

- #29 final SHA: `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`;
- #31 final SHA: `a3895434d17b857f752cea05a14b46a2de6943f7e70158755c88589fe9da0222`;
- #32 final SHA: `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`.

Thus #29/#32 match, but #31 is a real counterexample to treating the 720p route itself as universally bitwise deterministic. All five software3d shot bytes in #31 differ from #32 even though the derived plan and then-recorded package/executable/font runtime provenance are byte-identical.

This is **not currently a visual quality failure**. #31 seam evidence was intra p95 `0.933076`, max delta `4.178889`, ratio `4.478614`; #32 was `0.933903`, `4.184792`, `4.480971`. Both pass with margin. A decoded 90×160 grayscale comparison has mean absolute difference about **0.043/255** and only about **0.31%** of sampled pixels differ by more than one level.

The durable definition is therefore: **repeatable production quality/integrity contracts first; byte equality is additional scoped observation evidence, never the universal success criterion.** See `docs/decisions/2026-08-26-software3d-repeatability.md`.

## Runtime provenance closure in progress

#31 and #32 used the same recorded packages, FFmpeg/FFprobe/eSpeak executable bytes and caption font, but different hosted workers/regions. CPU/hardware execution identity was missing from `hottop.runtime-provenance.v1` capture in the 720p workflow.

PR #97 starts from a TDD RED that requires:

- `platform.machine()`;
- first-processor `/proc/cpuinfo` model name and vendor ID;
- SHA-256 of the complete `/proc/cpuinfo` bytes.

RED CI #1745 passed Ruff and failed exactly the new CPU-provenance contract (`1 failed / 500 passed`). The GREEN adds only provenance capture/self-verification; it does **not** alter renderer math, FFmpeg settings or quality thresholds and does not claim CPU differences caused the #31/#32 byte variance.

## Operator compute / generated-quality boundary

Canonical profile: `config/operator/dgx-spark-dual.yml`.
Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.
Model registry: `integrations/model-hub.yml`.

The declared two-node DGX Spark pool is preferred before paid SaaS, but Hottop does **not** infer runtime readiness. Driver/CUDA/PyTorch, disk/model paths and inter-node networking remain unverified until probe output from the actual operator hosts exists.

Priority generated-quality route remains reviewed local LightX2V + Wan2.2 I2V with rights-safe references, shared motion/quality/provenance gates and complete subject-bound continuity evidence. No automatic model download, GPU provisioning or paid fallback is admitted.

## Targeted ecosystem radar — 2026-08-26

- LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069` in the latest checked state. Its opt-in MiniMax-H3 residency work has no Hottop-measured benefit to the tested Wan2.2 route, so no freshness-only repin is admitted.
- Official Qwen3-TTS remains on the reviewed operator-local path; there is still no operator-provisioned 1.7B same-line Mandarin A/B evidence that justifies replacing the guaranteed eSpeak-family fallback.
- `docs/research/2026-08-26-qwen3-tts-serving-provenance.md` records exact identities for reviewed M*, vLLM-Omni and SGLang-Omni public reports. Their latency numbers depend on pinned patched/compatibility runtimes and primarily English traffic; they do not prove Mandarin naturalness or delivery control.

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

1. Verify PR #97 exact-head GREEN CI and real 720p cinematic-delivery artifact. Inspect the newly bound CPU identity; use it to interpret future cross-run evidence without asserting causality unsupported by data.
2. Inspect fresh real cow/Odyssey MP4 evidence and improve only a **measured** visual/audio defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
3. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
4. Once one reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run the first true-motion Odyssey benchmark with at least two subject-bearing I2V shots.
5. Bind actual generator source revision, local patch/override identity where applicable, checkpoint provenance when independently available, exact reference bytes and shot hashes; require meaningful motion plus complete cross-shot continuity evidence before composition.
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
