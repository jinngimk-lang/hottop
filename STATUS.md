# Hottop Status

Last updated: 2026-08-27
Active workstream: **Production v0.2 — repeatable real video output + generated identity/TTS quality readiness**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot, not a self-updating `main` pointer. Always re-fetch GitHub before exact head/CI claims.

## Current verified repository truth

PR #104 **Bind loaded numeric library bytes in delivery provenance** was squash-merged as `40dc5f4e1e7289b8f2c5c1bf7903be01a4b218ac` after exact head `cef9dde7427b9e7ba6e3606496fde34d79a2d3e3` passed CI #1780 and cinematic-delivery-smoke #54. Post-merge `main` then passed CI #1781 and cinematic-delivery-smoke #55, including 720×1280/24fps Odyssey production, numeric-runtime capture, media/provenance verification and artifact upload.

PR #105 **Record native runtime provenance and admit Stand-In benchmark candidate** established the next generated-identity benchmark candidate test-first and was squash-merged as `5e5af2552d1c9a148f372d9db81630d9a72cb922`.

- RED exact `0b596a8bfaafb8e6dde5da26a64d182b24a6e135`, CI #1782: Ruff passed; pytest failed exactly because `stand-in-wan22-a14b` was absent (`1 failed / 505 passed` on Python 3.11; Python 3.12 cancelled by fail-fast).
- GREEN implementation `f53440dda83484de59039bf31598007dfc436713`, CI #1783: full suite passed.
- Final exact head `37039ddb08bd8017dc909af412365458e0e17e03` passed PR CI #1787 and push CI #1788 on Python 3.11/3.12; review threads/comments were empty.
- Post-merge `main` CI #1789 passed on Python 3.11/3.12.

PR #108 **Harden CosyVoice3 runtime correctness gates** was squash-merged as `d59fe60569cf2f4e9da8455d52ae9ea6ccde92c0` after exact head `f7ad5e6f60fa099af141a88b32db2bd80f246a23` passed CI #1795 on Python 3.11/3.12 with no review threads.

- Fresh 2026-08-27 upstream evidence keeps CosyVoice3 as a correctness-gated operator benchmark candidate rather than a production/default route: TensorRT+FP16 has a reported official-checkpoint non-finite-audio failure, and a fresh streaming serving report shows an STFT device mismatch.
- `integrations/model-hub.yml` now registers `cosyvoice3-0b5-2512` only as `benchmark_candidate / integration_ready=false / runtime_status=unprobed`, with local operator provisioning, finite-waveform, TensorRT-FP16 and streaming gates encoded in the runtime boundary.
- The freshness review exposed a concrete Hottop adapter bug: Python `min/max` clamping could silently turn `NaN` into full-scale positive PCM. The local CosyVoice3 adapter now rejects any NaN/Inf sample before creating an output WAV, and the regression contract requires no partial output on failure.
- This closure added no CosyVoice dependency, model download, GPU provisioning, credential, paid behavior, default provider route, renderer change or media-threshold change.

## Native numerical runtime provenance — accepted and post-merge verified

Detailed decision: `docs/decisions/2026-08-27-native-numeric-library-provenance.md`.

The 720p cinematic delivery path now records semantic NumPy/threadpool reports **and** the exact native numerical library bytes loaded into the production process. The collector records resolved runtime path, library API, reported version, byte size and SHA-256, then rereads those bytes in the same job and fails closed on mismatch.

PR-head cinematic #54 artifact digest:

`sha256:29c54db3c3bb67ee5be41018cb09a9b93b3d89dc666b938047a85644c6768cae`

Post-merge cinematic #55 artifact digest:

`sha256:ff4743ed561a3f2da2fe2ca5c82e4b5ee545d68b829b50fb0f85600346559529`

Direct inspection of #55 confirms the actual loaded BLAS identity:

- OpenBLAS `0.3.34.0.0`;
- 25,210,641 bytes;
- SHA-256 `6cad8d2ad994ddc43d2ccdb0fb5d9458373ff1b87ef7ff420f2f94406eb8f082`.

The final #55 Odyssey MP4 remains SHA-256:

`c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`

with seam intra-shot p95 `0.933903`, max seam delta `4.184792` and max ratio `4.480971`.

Canonical rule remains unchanged: **repeatability is quality/media/integrity-contract-first, not universal hash-first**. Native-library byte identity is explanatory runtime provenance, not a reason to redefine success as bitwise equality.

## Guaranteed zero-cost baseline

The software3d → local Mandarin dialogue → original synthetic music/Foley → MoviePy → FFmpeg route remains the guaranteed zero-GPU, zero-model-download, zero-paid baseline. Current production evidence covers:

- story-specific moving 3D geometry rather than slideshow placeholders;
- mobile subject scale/placement and CJK subtitle/line-break gates;
- role-separated eSpeak-family dialogue, delivery-aware cadence and dialogue ducking;
- lower-roughness directional-light routing;
- bounded cross-shot dissolves plus real-final-MP4 seam gates;
- shot/final byte-bound provenance and pre-composition re-verification;
- H.264/yuv420p + AAC final-media verification;
- CPU/hardware, NumPy/thread runtime and exact loaded native numerical-library identity for the 720p delivery evidence.

The software3d baseline is a guaranteed fallback and production proof, not the cinematic/generated quality ceiling.

## Operator compute / generated-quality boundary

Canonical operator profile: `config/operator/dgx-spark-dual.yml`.
Durable spec: `docs/operations/dgx-spark-local-model-fabric.md`.
Model registry: `integrations/model-hub.yml`.

Declared DGX/local resources remain **unprobed** until the probe runs on the actual machines. Hottop does not infer driver/CUDA/PyTorch/model/network readiness from configuration.

The highest-value generated-quality proof remains a rights-safe reference-conditioned benchmark with at least two subject-bearing Odyssey shots, exact generator source/model/reference/shot provenance, meaningful motion and complete cross-shot continuity evidence before composition.

### Identity-continuity candidates

Targeted 2026-08-27 review now distinguishes the mechanism-level candidates explicitly:

- **LightX2V/Wan2.2** remains the existing tested operator-owned base route. LightX2V `main` remains `b220e26198fc90769114b6751236be96a3838069`; no freshness-only repin.
- **Stand-In/Wan2.2** is admitted to `integrations/model-hub.yml` as `benchmark_candidate / integration_ready=false / runtime_status=unprobed`. Exact reviewed source `WeChatCV/Stand-In@e351224366be169076e94af1454115d91d458313` contains Apache-2.0 `LICENSE`; its public model card declares Apache-2.0 and includes Wan2.2-compatible Stand-In weights. The upstream automatic model-download path is explicitly excluded from Hottop; base Wan2.2 checkpoint rights/runtime remain separate, and no identity claim is allowed before output-side evaluator evidence.
- **Memento** remains gated: exact GitHub source packaging lacks the README-linked root `LICENSE`, and official inference guidance is 8×A100 80GB.
- **IPVG** remains gated despite a mechanism closely matching the identity problem: exact source `cd70f169e9a86d47e7860392b8b80c8d59a6d75a` lacks the README-linked MIT `LICENSE` and the documented path adds Qwen3-8B + HyperLoRA + Wan2.2 provisioning.
- **WildActor** is a promising Wan2.2-5B multi-reference human-identity research candidate, but exact source `c858c2100ed14b32c36883e0570948f4c09e0d28` has no root license file in the inspected tree and introduces separate human-data/reference-rights questions. Keep it research-only.

No newly surfaced route is allowed to auto-install, auto-download multi-GB weights, fabricate DGX readiness or enter unattended/default routing.

## Mandarin TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B must not silently discard `delivery`/`instruct` semantics.

CosyVoice3 0.5B 2512 is now explicitly tracked as a separate **correctness-gated benchmark candidate**, not a fallback or default. Exact reviewed code source is `QwenAudio/CosyVoice@074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc` (Apache-2.0 code license); checkpoint/data/output/reference-audio rights remain separate. A future local benchmark must use already-provisioned runtime/model assets, reject non-finite waveforms, and keep TensorRT FP16 and streaming disabled unless the exact operator stack independently proves them correct end-to-end. Detailed note: `docs/research/2026-08-27-cosyvoice3-runtime-correctness.md`.

Official Qwen3-TTS `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`. A real same-line 1.7B Mandarin A/B still requires an already-provisioned local runtime/model and publication-rights review. No automatic multi-GB model download is allowed.

## Immediate next actions

1. Inspect fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Do not fabricate DGX readiness. Run `scripts/probe_dgx_spark.py` only on the actual operator machines.
3. Once a reviewed local LightX2V/Wan2.2 runtime and rights-safe references are genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
4. If Stand-In's exact reviewed local source/weights are genuinely provisioned later, use it as a same-shot identity benchmark against the LightX2V/Wan2.2 base route; do not invoke its automatic downloader and do not promote it without measured continuity gain.
5. Bind actual generator source revision, local patch/override identity when applicable, independently verifiable checkpoint provenance, exact reference bytes and shot hashes.
6. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
7. If CosyVoice3 is benchmarked later, keep it isolated and operator-local: exact source/checkpoint provenance, finite-waveform validation, rights-safe reference audio, and end-to-end actual-hardware evidence are mandatory; TensorRT FP16/streaming stay gated until independently green.
8. Continue targeted ecosystem radar around the measured gap. Do not add abstraction, freshness-only pins or large dependencies without measurable value and rollback.
9. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable creative/video skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
