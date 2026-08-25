# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — inspect real output quality; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current code `main`: `910e8fa1ed8c29385632854410906101a73e6fd9` (`Route role-aware dialogue to operator-local Qwen3 TTS`, squash merge of PR #57).

Latest verified pre-merge evidence for that exact change:

- PR #57 initial RED `94023c05abe0557aef21bda804c3cfa3a43c7d59`: CI **1550** passed Ruff and failed pytest because normal `video-run` did not accept/route `qwen3-customvoice`;
- first GREEN `7ffde866e16fdda3a877f54a5a162f102e90ba7c`: CI **1552** passed after typed local Qwen routing, role→speaker mapping, `delivery→--instruct` and Qwen `--output` fresh-output handling were connected;
- freshness review then found official Qwen inference code discards `instruct` on the **0.6B** CustomVoice checkpoint;
- capability RED `5981adba9a089b01b306df1911112f7ff4d26305`: CI **1553** failed pytest with Ruff green on the new requirement that Production reject 0.6B delivery control and admit an otherwise complete 1.7B checkpoint;
- final PR head `8a1aeb7bd0015f40a8b90595009cc5871452993c`: CI **1555** passed on Python 3.11/3.12 and production-smoke **113** passed the real cow + Odyssey guaranteed software3d path;
- PR #57 was squash-merged as `910e8fa1ed8c29385632854410906101a73e6fd9`.

Post-merge/documentation CI must be re-fetched before claiming a newer exact-head result.

## Real artifact-level closures

### Guaranteed zero-cost software3d baseline

The checked-in software3d route has reproducible production proof for:

- distinct story-specific moving 3D worlds for cow and Odyssey;
- perceptible, style-routed camera/pixel motion rather than slideshow-like output;
- mobile-first portrait placement and principal-subject readability;
- deliberate Anti-Polish cow vs brighter lower-roughness Odyssey presentation;
- role-aware dialogue metadata (`speaker` + `delivery`) preserved into `hottop.video-plan.v1`;
- Mandarin dialogue + readable, safe-area-bounded CJK subtitles;
- original synthetic music + procedural Foley/SFX;
- final AAC that is codec-valid, audibly active and duration-covering;
- MoviePy composition + FFmpeg H.264/AAC/yuv420p finalization;
- per-shot byte/provenance binding + pre-composition re-verification;
- final media verification;
- zero GPU, zero model download, zero credentials and zero paid services.

This is the guaranteed fallback/evidence baseline, not the cinematic quality ceiling.

### Qwen3-TTS role-aware Production routing

PR #57 connects the existing operator-local/offline Qwen3 CustomVoice adapter to normal `video-run` without replacing eSpeak:

- `VideoProductionConfig.audio.voice_backend` can explicitly select `qwen3-customvoice`;
- config carries an operator-local model path, preset-speaker map, language/device/dtype/attention settings;
- dialogue `character` maps to a configured preset speaker and `AudioCue.delivery` maps to `--instruct`;
- Qwen dialogue output uses the same fresh-output execution contract as eSpeak;
- readiness reuses the local Qwen environment inspector and never installs packages or downloads models;
- HF offline mode + `local_files_only=True` remain enforced in the adapter;
- eSpeak remains the guaranteed zero-cost/offline fallback.

**Capability correction:** the CustomVoice API signature alone is not enough to prove delivery control. Current official 0.6B (`tts_model_size=0b6`) discards `instruct`; current 1.7B (`1b7`) supports it. The role-aware Production route therefore fails closed on 0.6B rather than silently dropping `delivery`. Standalone 0.6B synthesis may remain available only when no instruction is requested.

**Rights boundary:** repository/model metadata currently say Apache-2.0, but preset-speaker output/commercial publication rights are treated as a separate operator gate. Hottop does not infer speaker/timbre clearance from software/model licensing alone.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

### Perceptible deterministic motion

Playable MP4 alone is insufficient. The software3d baseline has deterministic pixel-motion and camera-motion contracts: cow uses deliberate Anti-Polish pan/dolly movement; Odyssey uses controlled cinematic pan/crane/dolly/zoom motion. The motion gate is style-routed and does not redefine random failure as roughness.

### Mobile-first framing and subject readability

Production evidence closed two independent 9:16 defects:

1. narrative subjects were too low; portrait projection moved the principal point to 42% of frame height while preserving lower subtitle-safe space;
2. Odyssey key characters remained too small after placement passed; Odyssey-only portrait focal scale was raised while landscape behavior stayed unchanged.

Durable rule: mobile-first framing measures both placement and readable subject scale using style/backend/story-specific evidence rather than a universal magic number.

Decision record: `docs/decisions/2026-08-26-mobile-subject-readability.md`.

### Final audio / subtitle / media integrity

- final AAC must contain measurable signal and cover final video duration within 0.25 s codec/container skew tolerance;
- CJK font resolution fails closed instead of rendering tofu; normal execution does not auto-install fonts;
- captions are bottom-anchored from actual rendered height with safe-area clamping;
- final MP4 is re-verified for expected video/audio codecs, pixel format and duration after FFmpeg;
- failed/partial/zero-byte outputs are cleaned up rather than left as apparently consumable artifacts.

### Deterministic story identity

Software3d story routing is explicit and fail-closed. Cow and Odyssey resolve distinct world/character/prop staging; missing/unknown story topics are rejected rather than silently rendering the cow template.

## Generated/reference-conditioned identity gap

The remaining identity claim still requires **real generated-output evidence** from an operator-owned reference-conditioned route. This execution environment does not contain a provisioned LightX2V/Wan2.2 or compliant WanGP model/runtime/assets. Normal unattended Hottop must not auto-download multi-GB models, provision GPU, consume credits or weaken that boundary.

A production identity-preservation claim requires at least two generated byte-bound plan shots for the same rights-safe evaluated subject, exact reference + stable `subject_id`, generated-video quality gates, actual generator source provenance, independently verifiable model/checkpoint provenance when available, complete subject-bearing shot coverage and explicit evaluator identity/revision + fail-closed thresholds.

Generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes remain separate provenance dimensions.

## Current ecosystem radar

- **LightX2V** remains the primary Apache-2.0 operator inference framework for the tested Wan2.2/local path. No fresh upstream delta has yet shown a measured reason to repin the tested Hottop route without a benchmark.
- **SigLIP 2 Base 256** remains the preferred first operator-local continuity evaluator experiment only after explicit local weights + revision/hash are supplied; no implicit download.
- **Qwen3-TTS CustomVoice** is now integrated as a non-default local route, but actual quality evidence still requires an operator-provisioned instruct-capable checkpoint/runtime. Current upstream source establishes the 0.6B vs 1.7B instruct capability split.
- **CosyVoice3** remains an operator-owned comparison candidate; no current evidence justifies replacing eSpeak or the newly integrated Qwen route without a same-dialogue benchmark.
- DINOv3, DreamSim, WanGP and other candidates remain gated by their model/license/runtime boundaries.

Durable rule: code license != model/weights/data/output-rights clearance; popularity/freshness alone is not admission evidence.

## Immediate next actions

1. Re-fetch exact post-merge/documentation CI and production-smoke; repair any regression before opening new work.
2. Continue **direct artifact inspection** of the guaranteed software3d outputs and quantify the next visible/audible deterministic gap before changing code.
3. When an operator-provisioned Qwen3-TTS 1.7B CustomVoice runtime exists, run a same-dialogue eSpeak vs Qwen benchmark using the checked-in cow roles/deliveries; do not claim quality improvement before real audio evidence.
4. When a compliant operator-owned LightX2V/Wan2.2 or WanGP reference-conditioned runtime + rights-safe assets exist, execute the real multi-shot identity benchmark before claiming identity preservation.
5. Prefer SigLIP 2 Base 256 for the first local evaluator benchmark only with explicit local weights + exact revision/hash and same-subject vs identity-drift controls.
6. Continue targeted ecosystem scans against measured gaps and integrate only candidates clearing source/license/weights-license/cost/hardware/security/reversibility/value gates.
7. For fresh creative output, continue current-hotspot research + mechanism mapping + generation preflight rather than treating cow/Odyssey as defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
