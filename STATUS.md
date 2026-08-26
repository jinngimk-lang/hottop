# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Latest production-code `main` at this snapshot: `a4672fec7c60610acc576c49cc6c5a3238601577` (`Improve lower-roughness software3d depth`, squash merge of PR #74).

The guaranteed software3d production route has real CI/production-smoke evidence for:

- checked-in render/config → moving 3D shots → Mandarin dialogue + original music + procedural Foley/SFX → MoviePy → FFmpeg;
- H.264/AAC/yuv420p final MP4 verification;
- byte-bound per-shot provenance plus pre-composition re-verification;
- perceptible camera/pixel motion, mobile-first subject placement and subtitle safe-area/readability contracts;
- mixed CJK/Latin line-quality protection, including the resolved `用 InkClawAgent。` orphan-line regression;
- role-aware `speaker + delivery` preservation into execution;
- native `espeak-ng` preferred when installed, with legacy `espeak` retained as the guaranteed local fallback family;
- deterministic named-role pitch separation plus delivery-aware cadence, with production smoke checking stable recurring-role pitch and minimum canonical cow-role separation;
- dialogue-aware BGM ducking using actual generated voice duration and fail-closed materially clipped dialogue;
- final AAC that is codec-valid, audibly active and duration-covering;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic, generated-video or natural-voice quality ceiling.

## Latest visual-quality closure — style-routed software3d depth

Direct inspection of production-smoke #160 found a deterministic quality gap: lower-roughness Odyssey was brighter than Anti-Polish cow, but the core rasterizer still shaded faces by face index rather than 3D orientation. Across sampled frames, Odyssey and cow therefore had nearly the same luminance spread despite very different roughness intent.

PR #74 closed this with a narrow style-routed change:

- RED CI **1630** passed Ruff and failed pytest on the missing directional-depth contract;
- the legacy/high-roughness path remains `directional_shading_strength=0`, preserving the Anti-Polish cow appearance;
- `Scene3D` now supports optional deterministic face-normal directional shading with an explicit light vector;
- lower-roughness Odyssey opts into strength **0.45** while story geometry, subtitles, audio, provider routing, provenance and final-media gates remain unchanged;
- GREEN CI **1632** passed on Python 3.11 and 3.12;
- production-smoke **162** passed cow + Odyssey execution, final media verification and provenance verification;
- direct smoke #160 → #162 artifact comparison at 1/3/5/7/9/11/13 seconds showed cow luminance statistics unchanged frame-for-frame;
- Odyssey luminance standard deviation increased from roughly **10.3–13.8** to **12.2–15.4**, while p5–p95 luminance range increased from roughly **19–32** to **25–39**. The change therefore adds orientation-dependent depth rather than merely applying a global brightness lift.

Durable implementation principle: **style routing may change deterministic lighting depth as well as palette/roughness; Anti-Polish may intentionally remain flatter, while lower-roughness/cinematic software3d should use coherent geometric depth when it improves readability.** Surface polish remains optional; continuity, subtitles, story semantics, audio, provenance and encoding integrity remain hard gates.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains integrated as an explicit non-default local route without replacing the guaranteed eSpeak-family fallback:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- the official 0.6B CustomVoice path does not provide the required instruct behavior for the current role-aware production contract; an instruct-capable checkpoint such as the current 1.7B path remains the benchmark target;
- preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

No same-dialogue neural-quality claim exists until an operator-provisioned local 1.7B runtime is actually benchmarked against the checked-in fallback evidence.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP/H3 model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

Targeted freshness checks on 2026-08-26 did not justify changing a tested default:

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Recent visible activity is still concentrated on InfiniteTalk cancellation and new-model requests rather than a measured improvement to Hottop's tested Wan2.2 route; do not freshness-only repin.
- **MiniMax H3 via LightX2V** remains an operator benchmark candidate. Low-step support interest exists, but model/weights/output-rights, hardware, benchmark and local-provisioning gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate; recent acceleration work remains GPU/operator territory and does not displace the reviewed local adapter without real A/B evidence.
- **CosyVoice3** remains a comparison candidate rather than a default. Current reports still include non-finite TensorRT+FP16 output and streaming STFT device-mismatch failures, reinforcing configuration-specific correctness gates.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + exact revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk and newly discovered candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code. Do not tune merely because another parameter exists.
2. Verify post-merge `main@a4672fec…` CI and production-smoke before treating the merged head as the next evidence baseline.
3. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak-NG/eSpeak vs Qwen benchmark using checked-in roles/deliveries; do not claim quality improvement before real audio evidence.
4. When a compliant operator-owned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V or WanGP reference-conditioned runtime + rights-safe assets exist, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
5. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
6. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
7. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
