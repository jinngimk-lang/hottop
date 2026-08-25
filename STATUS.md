# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Latest production-code `main` at this snapshot: `de975c26acdf21d7c3dcd102e95da9d119fc8adf` (`Keep mobile captions out of the subject area`, squash merge of PR #59).

Verified evidence for that change:

- valid RED `35038dd997b3ca061ec2a62b2e6155829532dd51`: CI **1560** passed Ruff and failed pytest because the adaptive caption fitter did not exist;
- GREEN PR head `20946c913409b75797647f5f73d5c1c084afeeaf`: CI **1561** passed on Python 3.11/3.12 and production-smoke **115** passed both checked-in cow and Odyssey full production chains;
- direct inspection of smoke #115 MP4s measured Odyssey subtitle-block occupancy improving from about **22.8% → 10.2%** of portrait frame height at ~3 s and **21.4% → 15.8%** at ~7 s, with full text retained;
- PR #59 was squash-merged as `de975c26acdf21d7c3dcd102e95da9d119fc8adf`;
- post-merge CI **1562** passed and production-smoke **116** passed again on that exact production commit.

`docs/decisions/2026-08-26-mobile-subject-readability.md` records the durable mobile-readability rule. Documentation/status-only commits may advance `main` after this production snapshot; re-fetch before quoting the repository head.

## Guaranteed zero-cost software3d baseline

The checked-in software3d route has reproducible production evidence for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow output;
- mobile-first portrait placement, readable subject scale and bounded subtitle-block occupancy;
- adaptive full-copy caption fitting with a readable font floor, CJK local-font fail-closed behavior and bottom safe-area anchoring;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- role-aware dialogue metadata (`speaker` + `delivery`) preserved into `hottop.video-plan.v1`;
- Mandarin dialogue, original synthetic music and procedural Foley/SFX;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic quality ceiling.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice is integrated as an explicit non-default local route without replacing eSpeak:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- eSpeak remains the guaranteed zero-cost/offline fallback.

Capability boundary: current official 0.6B CustomVoice code discards `instruct`; the Production role-aware route therefore requires an instruct-capable checkpoint such as the current 1.7B path when delivery control is requested. Preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Mobile-first readability closure

Production evidence has now closed three independent portrait-readability defects:

1. principal subjects were too low in frame;
2. key Odyssey characters remained too small after placement was corrected;
3. long Odyssey subtitles were technically inside the bottom safe area but occupied more than one fifth of the portrait canvas and competed with the subject.

MoviePy now starts captions at the existing readable default size and only reduces long copy when the rendered block exceeds the mobile height budget, preserving full semantic content and a readable floor. The ~3 s Odyssey caption is now two lines; the ~7 s line remains three shorter lines but stays under the measured subject-area occupancy cap rather than forcing an excessively small font.

Decision record: `docs/decisions/2026-08-26-mobile-subject-readability.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Freshness checks continue to show active Wan2.2 maintenance, but no measured upstream delta currently justifies repinning the tested Hottop route without a benchmark.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate. Fresh issue activity reinforces the need for bounded generation/runtime safeguards; it does not justify replacing the guaranteed eSpeak fallback or bypassing the 1.7B instruction-capability gate.
- **CosyVoice3 / cosyvoice.cpp** remain comparison candidates. Current runtime/dependency and reported CUDA-audio caveats do not justify replacing the Qwen/eSpeak routing without a same-dialogue benchmark.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat and other candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of the guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code. Do not create a change merely to keep the loop busy.
2. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak vs Qwen benchmark using checked-in roles/deliveries; do not claim quality improvement before real audio evidence.
3. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets exist, execute the real multi-shot identity benchmark before claiming identity preservation.
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
