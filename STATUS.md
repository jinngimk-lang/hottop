# Hottop Status

Last updated: 2026-08-27
Active workstream: **Production v0.2 — repeatable real video output + generated-quality readiness**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot, not a self-updating `main` pointer. Always re-fetch GitHub before exact head/CI claims.

## Current verified repository truth

PR #102 **Bind numeric runtime provenance in cinematic delivery evidence** was squash-merged as `05575adbbfc9b462a5744c7d3c0994458654d5b0` after exact head `32e93ff079066e126b55811d5be8db62356779b3` passed:

- CI #1773;
- production-smoke #187;
- cinematic-delivery-smoke #51.

The merge commit then passed the full post-merge evidence loop:

- CI #1774 on Python 3.11/3.12;
- production-smoke #188 for both cow and Odyssey;
- cinematic-delivery-smoke #52 for 720×1280/24fps Odyssey.

There were no unresolved review threads on PR #102.

## Numeric runtime provenance — accepted contract

`docs/decisions/2026-08-27-numeric-runtime-provenance.md` is the detailed evidence record. New 720p cinematic software3d delivery evidence now binds material numerical execution identity in addition to source/plan/package/media/font/CPU provenance:

- logical CPU count;
- relevant BLAS/OpenMP thread environment;
- human-readable `numpy.show_config()` and `numpy.show_runtime()` reports plus SHA-256 identities;
- pinned `threadpoolctl==3.6.0` package identity.

PR-head cinematic #51 recorded Python 3.12.14, NumPy 2.5.2, `threadpoolctl 3.6.0`, AMD EPYC 9V74, 4 logical CPUs and OpenBLAS 0.3.34.0.0 / pthreads / 4 runtime threads. Its Actions artifact digest is `sha256:257ff8331775a4025f016ee073e3f566da4495fbeef0b5f421813f27e811f866`.

Post-merge #52 ran on AMD EPYC 7763 instead, while the NumPy/OpenBLAS runtime reports and their SHA-256 identities remained unchanged. The derived video plan, seam metrics and final 720p MP4 were byte-identical to #51. Both runs produced final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, with seam intra-shot p95 `0.933903`, max seam delta `4.184792` and max ratio `4.480971`. The #52 Actions artifact digest is `sha256:1dad9f6e22e211fcb37dc95b518aa978b326e1b3ace4347517615909d1e641c1`.

This strengthens the canonical rule: **repeatability is quality/media/integrity-contract-first, not universal hash-first**. Hardware and numerical-runtime identity are explanatory provenance; neither should be treated as a single-factor causal explanation for byte variance.

## Fresh real production inspection

Post-merge production-smoke #188 was downloaded and inspected directly rather than inferred from workflow success.

- Cow and Odyssey both show continuous real pixel motion at sampled 1/3/5/7/9/11/13s frames.
- CJK subtitles remain readable and inside the established mobile safe area.
- No `-35 dB / 0.5s` long-silence event was detected.
- Cow audio mean/max remains approximately `-24.8 / -4.2 dB`; Odyssey approximately `-23.9 / -4.0 dB`.
- Cow seam max delta / max ratio: `4.433333 / 3.609125`.
- Odyssey seam max delta / max ratio: `5.195625 / 3.036145`.

No new deterministic framing, lighting, transition, subtitle or loudness regression was measured, so no visual/audio tuning was introduced merely to create a change.

## Guaranteed zero-cost baseline

The software3d → local Mandarin dialogue → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-model-download, zero-paid baseline. Current production evidence covers:

- story-specific moving 3D geometry rather than slideshow placeholders;
- mobile subject scale/placement and CJK subtitle/line-break gates;
- role-separated eSpeak-family dialogue, delivery-aware cadence and dialogue ducking;
- lower-roughness directional-light routing;
- bounded cross-shot dissolves plus real-final-MP4 seam gates;
- shot/final byte-bound provenance and pre-composition re-verification;
- H.264/yuv420p + AAC final-media verification;
- CPU/hardware and numerical-runtime identity for new 720p delivery evidence.

The software3d baseline is a guaranteed fallback and production proof, not the cinematic/generated quality ceiling.

## Operator compute / generated-quality boundary

Canonical operator profile: `config/operator/dgx-spark-dual.yml`.
Durable spec: `docs/operations/dgx-spark-local-model-fabric.md`.
Model registry: `integrations/model-hub.yml`.

Declared DGX/local resources remain **unprobed** until the probe runs on the actual machines. Hottop does not infer driver/CUDA/PyTorch/model/network readiness from configuration.

The highest-value generated-quality proof remains a rights-safe reference-conditioned LightX2V/Wan2.2 benchmark with at least two subject-bearing Odyssey I2V shots, exact generator source/model/reference/shot provenance, meaningful motion and complete cross-shot continuity evidence before composition.

Memento remains a gated continuity benchmark candidate. Its released adapter weights are marked Apache-2.0, but the exact GitHub tree still lacks the README-linked root `LICENSE`, base Wan2.2 rights remain separate, and official inference guidance recommends 8×A100 80GB. No normal `video-run` download/routing is admitted.

## Mandarin TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B must not silently discard `delivery`/`instruct` semantics.

A real same-line 1.7B Mandarin A/B still requires an already-provisioned local runtime/model and publication-rights review. No automatic multi-GB model download is allowed.

## Targeted ecosystem radar — 2026-08-27

Fresh exact checks do not justify changing tested defaults:

- ModelTC/LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069`; its latest opt-in MiniMax-H3 DiT residency change does not provide measured Hottop value for the tested Wan2.2 path. **No freshness-only repin.**
- Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no upstream change removes the operator-provisioned 1.7B benchmark gate.
- `ernie-research/Memento` remains `eafe8aa6811d7f27477801c23c54faa33fa4659c`; inference code and adapter weights are public, but license packaging/hardware feasibility still block admission.
- `threadpoolctl 3.6.0` is a small BSD-3-Clause evidence helper, pinned explicitly after a real smoke proved it cannot be assumed as a NumPy transitive dependency.

No heavy dependency, automatic model download, GPU provisioning or paid fallback was admitted from this scan.

## Immediate next actions

1. Inspect fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
3. Once a reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
4. Bind actual generator source revision, local patch/override identity when applicable, independently verifiable checkpoint provenance, exact reference bytes and shot hashes.
5. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
6. Continue targeted ecosystem radar around the measured gap. Do not add abstraction, freshness-only pins or large dependencies without measurable value and rollback.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable creative/video skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
