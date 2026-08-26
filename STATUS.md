# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Current `main` at this snapshot: `081e25100a76f200aefd9966012443c03041ccb2` (`docs: refresh Qwen3-TTS operator acceleration radar`, squash merge of PR #76).

Exact-head CI **1637** completed successfully on Python 3.11 and 3.12. PR #76 was docs/research-only and did not change runtime behavior.

The latest real software3d production artifact remains production-smoke **163** from production-code head `a4672fec7c60610acc576c49cc6c5a3238601577`. Later commits through `081e251…` are documentation/status-only relative to that production code and therefore do not supersede the actual media artifact.

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

## Latest direct artifact inspection

The production-smoke **163** artifact was downloaded and inspected directly in this owner loop rather than inferred from tests alone.

- Both final MP4s were sampled at **1/3/5/7/9/11/13 seconds**.
- All five cow shots and all five Odyssey shots retained visible motion; sampled frame-difference measurements were non-zero in every shot. Cow remained intentionally rougher/slower, while Odyssey showed stronger motion and spatial contrast.
- Approximate downsampled frame-difference means were **1.92** for cow and **2.83** for Odyssey; per-shot means were also non-zero throughout. These are inspection diagnostics, not a new universal quality threshold.
- No new deterministic subtitle, framing, clipping, static-shot or broken-media regression was found.
- The visible upper dark margin does **not** currently justify another camera change: repository contracts already require Odyssey primary subjects to occupy at least **14%** of frame height, and both cow/Odyssey narrative subjects must enter the upper mobile action zone (`top <= 35%`) while staying above the subtitle-safe lower region (`bottom <= 72%`). The inspected artifacts remain consistent with those measured contracts.

Decision: **do not tune framing or subject scale merely because another parameter exists**. Require a measurable artifact failure against the existing mobile-readability contracts before changing projection/camera geometry again.

## Latest visual-quality closure — style-routed software3d depth

PR #74 added optional deterministic face-normal directional shading while preserving the Anti-Polish default:

- RED CI **1630** isolated the missing directional-depth contract;
- high-roughness cow remains `directional_shading_strength=0`;
- lower-roughness Odyssey opts into strength **0.45**;
- GREEN CI **1632** and production-smoke **162** passed;
- direct artifact comparison showed cow luminance unchanged while Odyssey gained materially wider luminance/spatial-depth spread without black/white clipping.

Durable principle: **style routing may change deterministic lighting depth as well as palette/roughness; Anti-Polish may intentionally remain flatter, while lower-roughness/cinematic software3d should use coherent geometric depth when it improves readability.**

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains integrated as an explicit non-default local route without replacing the guaranteed eSpeak-family fallback:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- an instruct-capable checkpoint such as the current 1.7B path remains the meaningful same-dialogue benchmark target;
- preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

PR #76 refreshed the acceleration radar without changing this decision. H100/H200-oriented serving stacks such as `nari-labs/nari-qwen3-tts` and SGLang-Omni remain **benchmark-only operator candidates**. A claimed optimization is not admitted until it improves an end-to-end Hottop same-dialogue benchmark; one recent SGLang-Omni Qwen3-TTS optimization path was removed after failing to show repeatable end-to-end benefit.

No same-dialogue neural-quality claim exists until an operator-provisioned local 1.7B runtime is actually benchmarked against the checked-in fallback evidence.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP/H3 model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

Targeted freshness checks on 2026-08-26 still do not justify changing a tested default:

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Upstream `main` is still `5dc5d6372654406761474719647763ac7b4bd018`; the latest visible change is a SwiftVR BF16→NumPy export fix. Nearby MiniMax-H3 work adds RTX 5090 deploy configuration and Qwen host-weight pinning controls, but no Hottop benchmark or rights/hardware evidence currently justifies a freshness-only repin or default change.
- **MiniMax H3 via LightX2V** remains an operator benchmark candidate; model/weights/output-rights, hardware, benchmark and local-provisioning gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate; recent acceleration work remains GPU/operator territory and does not displace the reviewed local adapter without real A/B evidence.
- **CosyVoice3** remains a comparison candidate rather than a default. Recent reports still include non-finite TensorRT+FP16 output and streaming STFT device-mismatch failures, reinforcing configuration-specific correctness gates.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + exact revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk and newly discovered candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code. Do not tune merely because another parameter exists.
2. Keep `main@081e251…` CI as the current repository-health baseline; keep production-smoke **163 / production-code `a4672fec…`** as the latest real-media baseline until production code changes again.
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
