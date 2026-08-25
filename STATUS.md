# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Latest production-code `main` at this snapshot: `e5a286e8791d1cc962badeab8976125688cc664f` (`Prevent orphaned mixed-script mobile captions`, squash merge of PR #62).

Verified exact-head evidence:

- PR #62 exact head `30eea89f9d1659f6d4eaab77ec4541abca699b6b`: CI **1584** passed and production-smoke **134** passed;
- the #134 production artifact was downloaded and directly inspected at ~1/3/5/7/9 s for both cow and Odyssey; the short mixed caption `用 InkClawAgent。` remains on one line in the lower safe area rather than creating a one-character orphan;
- PR #62 was squash-merged as `e5a286e8791d1cc962badeab8976125688cc664f`;
- post-merge CI **1585** passed and production-smoke **135** passed again on that exact production commit.

The immediately preceding `main` commit `a99cf5b64d9f403e19de040e2d45363db6de6a61` also closed actual MoviePy dialogue/BGM interaction: dialogue ducking is executed rather than metadata-only, ducking follows actual voice duration, materially clipped dialogue fails closed, and checked-in cow/Odyssey short-form lines were adjusted to fit intelligible windows.

`docs/decisions/2026-08-26-mobile-subject-readability.md` records the durable portrait-readability rule, now covering subject placement, readable subject scale, subtitle block occupancy and line-break quality.

## Guaranteed zero-cost software3d baseline

The checked-in software3d route has reproducible production evidence for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow output;
- mobile-first portrait placement, readable subject scale, bounded subtitle-block occupancy and non-orphaned short mixed-script captions;
- adaptive full-copy caption fitting with a readable font floor, CJK local-font fail-closed behavior and bottom safe-area anchoring;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- role-aware dialogue metadata (`speaker` + `delivery`) preserved into `hottop.video-plan.v1`;
- Mandarin dialogue, original synthetic music and procedural Foley/SFX;
- executed dialogue-aware BGM ducking, actual-voice-duration duck windows and fail-closed materially clipped dialogue;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic quality ceiling.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains integrated as an explicit non-default local route without replacing eSpeak:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- eSpeak remains the guaranteed zero-cost/offline fallback.

Capability boundary: current official 0.6B CustomVoice code discards `instruct`; the Production role-aware route therefore requires an instruct-capable checkpoint such as the current 1.7B path when delivery control is requested. Preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Mobile-first readability closure

Production evidence has now closed four independent portrait-readability defects:

1. principal subjects were too low in frame;
2. key Odyssey characters remained too small after placement was corrected;
3. long Odyssey subtitles were technically inside the bottom safe area but occupied more than one fifth of the portrait canvas and competed with the subject;
4. the short mixed CJK/Latin cow caption `用 InkClawAgent。` passed safe-area/block-height gates but generic wrapping created a one-character first line.

MoviePy now preserves full semantic copy, resolves a real local CJK-capable font, fits long copy within the measured mobile height budget and prefers natural-width single-line layout for short mixed-script captions. If the single line is only slightly too wide, it shrinks within the existing readable font floor before wrapped-caption fallback.

Decision record: `docs/decisions/2026-08-26-mobile-subject-readability.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Targeted freshness check on 2026-08-26 still shows upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018`; the newest commits are SwiftVR BF16 export handling plus MiniMax-H3 deployment/host-pinning work. None is measured against Hottop's tested Wan2.2 path, so the existing tested pin remains preferable to freshness-driven repinning.
- **MiniMax H3 via LightX2V** is now visibly maintained upstream, including 5090 deployment configuration and Qwen host-weight pinning, but this does not clear model/weights/output-rights, hardware, benchmark or local-provisioning gates. It remains an operator benchmark candidate, not an unattended default.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate. The official repository head checked on 2026-08-26 remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no source delta invalidates the existing 0.6B-vs-1.7B capability gate. Real quality comparison still requires an operator-provisioned local 1.7B runtime.
- **CosyVoice3 / cosyvoice.cpp** remain comparison candidates. Current public evidence still includes a repeatable CosyVoice3 TensorRT+FP16 non-finite-audio failure report and additional runtime/dependency requirements, so there is no evidence-backed reason to replace Qwen/eSpeak routing without a same-dialogue benchmark.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk and other candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code. The direct #134 review after the caption fix did not reveal a new specific regression worth coding immediately.
2. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak vs Qwen benchmark using checked-in roles/deliveries; do not claim quality improvement before real audio evidence.
3. When a compliant operator-owned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V or WanGP reference-conditioned runtime + rights-safe assets exist, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
4. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
5. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
6. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
