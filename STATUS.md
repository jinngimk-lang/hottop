# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current verified production baseline

Latest production-code `main` at this snapshot: `8ae92f664d79c73e804f2445e89d0ab07f5e2977` (`audio: strengthen zero-cost eSpeak role separation`, squash merge of PR #69).

Verified evidence:

- PR #62 closed the mixed CJK/Latin orphan-line defect; its production artifact was directly inspected and `用 InkClawAgent。` remained on one line in the lower safe area;
- later Production v0.2 work preserved dialogue/BGM ducking, actual-voice-duration windows, clipping fail-close, mobile framing and subtitle contracts;
- PR #65 restored both cow and Odyssey provenance archives in production smoke after a workflow regression;
- PR #66 made runtime readiness/execution prefer native `espeak-ng` when available while retaining `espeak` compatibility as the guaranteed local fallback family;
- PR #67 first operationalized preserved `speaker + delivery` metadata in the guaranteed eSpeak-family fallback through stable character pitch plus delivery-aware cadence;
- merged `main@2d11b02a35e2dbe460917bb4b15d4b6ec4e941a6`: CI **1611** passed on Python 3.11/3.12 and production-smoke **154** passed the role-aware probe + cow + Odyssey + final media/provenance chain;
- direct smoke #154 inspection exposed a weak canonical role distinction: `young-cow` pitch **44** vs `mother-cow` pitch **46**. The prior test required only inequality, which was insufficient as a useful fallback-separation contract;
- PR #69 RED CI **1614** failed exactly the new minimum-separation contract: `abs(44 - 46) = 2 < 6` after Ruff passed;
- the first spaced-bucket implementation was independently falsified by CI **1615** because the two canonical cow roles collided at pitch **62**, preventing a false GREEN;
- final PR #69 head `b69833884cb640d1a921e0d26c7dc2dc4cd1c504`: CI **1616** passed on Python 3.11/3.12 and production-smoke **156** passed;
- smoke #156 measured `young-cow` pitch **32**, `mother-cow` pitch **50**, `witch` pitch **62**. Young-cow delivery cadence still changed **169 → 162 wpm** across canonical cues, while each recurring role kept a stable pitch;
- smoke #156 also re-executed both complete production chains: checked-in render/config → software3d moving shots → Mandarin dialogue/original music/procedural SFX → MoviePy → FFmpeg → H.264/AAC/yuv420p MP4 + five byte-bound shot manifests each.

`docs/decisions/2026-08-26-mobile-subject-readability.md` records the durable portrait-readability rule. `docs/research/2026-08-26-qwen3-customvoice-routing.md` records the operator-local neural TTS boundary and the deterministic role-aware fallback relationship.

## Guaranteed zero-cost software3d baseline

The checked-in software3d route has reproducible production evidence for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow output;
- mobile-first portrait placement, readable subject scale, bounded subtitle-block occupancy and non-orphaned short mixed-script captions;
- adaptive full-copy caption fitting with a readable font floor, CJK local-font fail-closed behavior and bottom safe-area anchoring;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- role-aware dialogue metadata (`speaker` + `delivery`) preserved into `hottop.video-plan.v1` and operationalized by the eSpeak-family fallback;
- native eSpeak-NG preferred when installed, legacy `espeak` retained as compatible guaranteed local fallback;
- recurring named roles mapped deterministically into conservative spaced pitch buckets while delivery changes bounded cadence; the canonical cow production now has an 18-point eSpeak pitch separation instead of the earlier 2-point separation;
- original synthetic music and procedural Foley/SFX;
- executed dialogue-aware BGM ducking, actual-voice-duration duck windows and fail-closed materially clipped dialogue;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- both cow and Odyssey provenance archives retained by production smoke;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic or natural-voice quality ceiling. The deterministic eSpeak pitch space remains intentionally compact and can still collide for arbitrary role labels, so it is a best-effort role-differentiation mechanism, not a universal speaker-identity guarantee or a neural-voice quality claim.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains integrated as an explicit non-default local route without replacing the guaranteed eSpeak-family fallback:

- normal `video-run` can select `qwen3-customvoice` through typed audio config;
- dialogue `character` maps to configured preset speakers and `delivery` maps to `--instruct`;
- local checkout/model/runtime preflight is fail-closed and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- current official 0.6B CustomVoice code discards `instruct`; Production role-aware routing therefore requires an instruct-capable checkpoint such as the current 1.7B path when delivery control is requested;
- preset-speaker output/commercial-use clearance remains an operator rights gate separate from repository/model licensing.

No same-dialogue neural-quality claim exists until an operator-provisioned local 1.7B runtime is actually benchmarked against the checked-in fallback evidence.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

The remaining identity-quality claim still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime plus rights-safe benchmark assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. Upstream `main` was still `5dc5d6372654406761474719647763ac7b4bd018` on the 2026-08-26 check; its latest visible change fixes SwiftVR BF16 image conversion before NumPy export and does not materially improve the Hottop-tested Wan2.2 path, so there is no freshness-only repin.
- **MiniMax H3 via LightX2V** remains an operator benchmark candidate: upstream interest includes low-step LoRA/support requests, but model/weights/output-rights, hardware, benchmark and local-provisioning gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local role-aware Mandarin candidate; no newly observed runtime displaces the reviewed official adapter without local evidence.
- **CosyVoice3** remains a comparison candidate rather than a default. Current upstream reports include non-finite audio with `load_trt=True + fp16=True` on the official Fun-CosyVoice3-0.5B-2512 checkpoint and a separate streaming STFT device-mismatch failure, reinforcing configuration-specific correctness gates rather than automatic promotion of accelerated paths.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- DINOv3, DreamSim, WanGP, FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk and other candidates remain subject to code-license, weights/data/output-rights, hardware, hidden-download/network, cost, security, benchmark-value and rollback gates.

Durable rule: code license != model/weights/data/output-rights clearance; popularity or freshness alone is not admission evidence.

## Immediate next actions

1. Continue **direct artifact inspection** of guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code; do not keep tuning eSpeak merely because more numeric separation is possible.
2. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak-NG/eSpeak vs Qwen benchmark using checked-in roles/deliveries; do not claim quality improvement before real audio evidence.
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
