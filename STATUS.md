# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — real-output quality, separate smoke evidence from delivery quality, benchmark operator-local routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Current production `main` at this snapshot: `685ba9497e36b38c140431cff68c710527c9492e` (`Add presentable cinematic software3d delivery profile`, squash merge of PR #78).

PR #78 was TDD-driven:

- RED head `d97ef167e3ea62f89457c92895430cf09e77a9fa`, CI **1640**: Ruff passed; pytest failed because the cinematic delivery profile did not exist; Python 3.12 was cancelled by fail-fast.
- GREEN head `6ace6ac1faeaa4632be3d71a9225b9039cb1ab6f`, CI **1641**: Python 3.11/3.12 passed Ruff + full pytest.
- Production-smoke **164** on the same GREEN head passed both canonical cow and Odyssey config → moving shots → Mandarin dialogue/original music/Foley → MoviePy → FFmpeg → final media/provenance verification.

Post-merge `main@685ba949…` CI / production-smoke are the next exact-head repository-health checks; do not treat this snapshot as proof until those runs complete.

## Guaranteed zero-cost software3d baseline

The lightweight, repeatedly exercised smoke profiles remain intentionally small:

- `anti-polish-software3d.yml`: 360×640, 12 fps;
- `cinematic-software3d.yml`: 360×640, 12 fps.

They exist to keep full config→media→provenance evidence cheap and repeatable in CI. They are **not** a cinematic delivery ceiling.

The guaranteed route has real production-smoke evidence for:

- checked-in render/config → actual moving 3D shots;
- Mandarin eSpeak-NG/eSpeak dialogue with preserved `speaker + delivery` semantics;
- original synthetic music + procedural Foley/SFX;
- dialogue-aware BGM ducking and real voice-duration handling;
- MoviePy composition → FFmpeg H.264/AAC/yuv420p/fast-start finalization;
- final AAC activity/duration coverage;
- byte-bound per-shot provenance plus immediate pre-composition byte re-verification;
- perceptible motion, mobile-first subject placement/scale, subtitle containment and mixed CJK/Latin line-quality protection;
- style-routed deterministic lighting depth for lower-roughness Odyssey while Anti-Polish cow remains intentionally flatter;
- zero GPU, zero model download, zero credentials and zero paid services.

## Cinematic software3d delivery profile

Production artifact inspection exposed a quality-contract mismatch: lower-roughness cinematic output was only represented by the lightweight 360×640/12fps smoke profile, even though `PROJECT.md` already requires cinematic/presentable execution and states the software3d baseline is not the cinematic ceiling.

PR #78 therefore added `config/video/cinematic-software3d-delivery.yml`:

- **720×1280, 24 fps**;
- `software3d → MoviePy → FFmpeg`;
- cinematic/lower-roughness semantics with Anti-Polish disabled;
- Mandarin guaranteed local voice fallback, original synthetic score and procedural Foley;
- no URL/QR;
- no GPU, model, credential, paid API or hidden network requirement.

Durable execution distinction: **smoke quality and delivery quality are separate profiles**. Keep CI smoke lightweight; use the delivery profile for a presentable zero-cost artifact when local execution budget permits. Do not claim a 720×1280/24fps delivery artifact until that profile has actually produced and passed final-media/provenance verification.

## Latest direct real-media inspection

The latest directly inspected guaranteed artifact remains production-smoke **163** from production-code head `a4672fec7c60610acc576c49cc6c5a3238601577`.

Inspection findings:

- cow and Odyssey MP4s were sampled at 1/3/5/7/9/11/13 seconds and retained visible motion in all five shots;
- no new deterministic framing, subtitle, static-shot, clipping or broken-media regression was found;
- current framing contracts remain adequate; do not tune projection/camera without a measurable failure;
- audio diagnostics were approximately **-21.2 LUFS / -4.2 dBFS peak** for cow and **-20.0 LUFS / -3.9 dBFS peak** for Odyssey, with no ≥0.5 s silence at -35 dB. These are diagnostics, not universal loudness targets.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains the preferred non-default role-aware Mandarin benchmark candidate behind fail-closed local preflight:

- eSpeak-NG/eSpeak remains the guaranteed zero-cost/offline fallback;
- normal role-aware production requires a proven Qwen3-TTS CustomVoice config and an instruct-capable checkpoint; current official 0.6B ignores `instruct`, while current 1.7B is the admitted delivery-control benchmark target;
- no package/model auto-install or network model fetch;
- preset-speaker/output publication rights remain an operator gate separate from Apache-2.0 metadata;
- H100/H200 serving stacks remain benchmark-only until an end-to-end Hottop A/B proves value.

No neural-quality improvement claim exists until an operator-provisioned 1.7B runtime is actually benchmarked on the same checked-in dialogue.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

A real identity-preservation claim still requires an operator-owned reference-conditioned runtime plus rights-safe benchmark assets. This environment does not contain a provisioned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V, WanGP or equivalent compliant GPU/model runtime.

Normal unattended Hottop must not auto-download multi-GB weights, provision GPU, consume credits or weaken the evidence boundary. A production identity claim still requires exact reference bytes, stable subject IDs, complete subject-bearing shot coverage, generated-video quality gates, generator/model/evaluator provenance and byte-bound generated artifacts.

## Current ecosystem radar

Targeted 2026-08-26 checks still do not justify changing a tested default:

- **LightX2V** remains the tested Apache-2.0 operator-local inference framework for the current Wan2.2 path; no freshness-only repin without Hottop benchmark evidence.
- **MiniMax H3 through LightX2V** remains an operator benchmark candidate; weights/output-rights, hardware and local benchmark gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local Mandarin role-aware candidate; H100/H200 acceleration stacks do not displace the reviewed local adapter without real A/B evidence.
- **CosyVoice3** remains a comparison candidate; recent TensorRT+FP16 non-finite output and streaming device-mismatch reports reinforce configuration-specific correctness gates.
- **SigLIP 2 Base 256** remains the preferred first local continuity evaluator experiment only when exact local weights/revision/hash are explicitly supplied.
- FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk, DINOv3, DreamSim and newly discovered projects remain behind separate code-license, weights/data/output-rights, hidden-download/network, hardware, security, cost, benchmark-value and rollback gates.

Durable rule: popularity/freshness is not admission evidence; code license is not model/weights/data/output-rights clearance.

## Immediate next actions

1. Verify post-merge `main@685ba949…` CI and production-smoke before treating the merge head as repository-health baseline.
2. Produce and archive a **real 720×1280/24fps Odyssey artifact using `cinematic-software3d-delivery.yml`** when a safe local runner is available; require the same audio, MoviePy, FFmpeg, final-media and provenance gates. Do not overload routine smoke CI merely to prove delivery resolution.
3. Continue direct artifact inspection and change deterministic visuals/audio only when a measurable failure appears.
4. When an operator-provisioned Qwen3-TTS 1.7B runtime exists, run same-dialogue eSpeak-family vs Qwen A/B; no quality claim before real audio evidence.
5. When a compliant operator-owned reference-conditioned runtime plus rights-safe assets exists, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
6. Continue targeted ecosystem scans against measured gaps; integrate only candidates clearing source/license/weights/cost/hardware/security/reversibility/value gates.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain test fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
