# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — prove presentable zero-cost delivery output; benchmark operator-local generated/TTS routes when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Current production `main` at this snapshot: `685ba9497e36b38c140431cff68c710527c9492e` (`Add presentable cinematic software3d delivery profile`, squash merge of PR #78).

PR #78 was TDD-driven:

- RED head `d97ef167e3ea62f89457c92895430cf09e77a9fa`, CI **1640**: Ruff passed; pytest failed because the cinematic delivery profile did not exist; Python 3.12 was cancelled by fail-fast.
- GREEN head `6ace6ac1faeaa4632be3d71a9225b9039cb1ab6f`, CI **1641**: Python 3.11/3.12 passed Ruff + full pytest.
- Production-smoke **164** on the same GREEN head passed both canonical cow and Odyssey config → moving shots → Mandarin dialogue/original music/Foley → MoviePy → FFmpeg → final media/provenance verification.
- Post-merge `main@685ba949…` CI **1642** passed on Python 3.11/3.12 and production-smoke **165** passed the same full cow + Odyssey production/provenance chain.

## Guaranteed zero-cost software3d baseline

The lightweight, repeatedly exercised smoke profiles remain intentionally small:

- `anti-polish-software3d.yml`: 360×640, 12 fps;
- `cinematic-software3d.yml`: 360×640, 12 fps.

They exist to keep full config→media→provenance evidence cheap and repeatable in CI. They are **not** a cinematic delivery ceiling.

The guaranteed route has real production-smoke evidence for checked-in render/config → actual moving 3D shots → Mandarin eSpeak-NG/eSpeak dialogue with preserved `speaker + delivery` semantics → original synthetic music/procedural Foley → dialogue-aware MoviePy composition → FFmpeg H.264/AAC/yuv420p/fast-start finalization. It also carries final AAC activity/duration checks, byte-bound per-shot provenance + immediate pre-composition re-verification, perceptible-motion/mobile-framing/subtitle contracts, and zero GPU/model-download/credential/paid-service requirements.

## Cinematic software3d delivery profile

Production artifact inspection exposed a quality-contract mismatch: lower-roughness cinematic output was only represented by the lightweight 360×640/12fps smoke profile, even though `PROJECT.md` already requires cinematic/presentable execution and states the software3d baseline is not the cinematic ceiling.

PR #78 therefore added `config/video/cinematic-software3d-delivery.yml`:

- **720×1280, 24 fps**;
- `software3d → MoviePy → FFmpeg`;
- cinematic/lower-roughness semantics with Anti-Polish disabled;
- Mandarin guaranteed local voice fallback, original synthetic score and procedural Foley;
- no URL/QR;
- no GPU, model, credential, paid API or hidden network requirement.

Durable execution distinction: **smoke quality and delivery quality are separate profiles**. Keep CI smoke lightweight; use the delivery profile for a presentable zero-cost artifact when local execution budget permits. The profile contract and regression safety are verified, but a 720×1280/24fps Odyssey final artifact has **not yet** been archived; do not claim delivery-media proof until that full profile actually passes the media/provenance chain.

## Latest direct real-media inspection

The latest directly inspected guaranteed artifact is production-smoke **163** from production-code head `a4672fec7c60610acc576c49cc6c5a3238601577`; later smoke runs re-prove the same lightweight baseline but were not separately visually sampled in this snapshot.

Inspection findings:

- cow and Odyssey MP4s sampled at 1/3/5/7/9/11/13 seconds retained visible motion in all five shots;
- no new deterministic framing, subtitle, static-shot, clipping or broken-media regression was found;
- current framing contracts remain adequate; do not tune projection/camera without a measurable failure;
- audio diagnostics were approximately **-21.2 LUFS / -4.2 dBFS peak** for cow and **-20.0 LUFS / -3.9 dBFS peak** for Odyssey, with no ≥0.5 s silence at -35 dB. These are diagnostics, not universal loudness targets.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains the preferred non-default role-aware Mandarin benchmark candidate behind fail-closed local preflight. eSpeak-NG/eSpeak remains the guaranteed zero-cost/offline fallback. Current official 0.6B CustomVoice ignores `instruct`; current 1.7B is the admitted delivery-control benchmark target. No package/model auto-install or network model fetch is allowed, and preset-speaker/output publication rights remain an operator gate separate from Apache-2.0 metadata.

Fresh 2026-08-26 runtime review does not justify a default change: H100/H200 acceleration stacks remain operator benchmark infrastructure, while CosyVoice3 still has recent correctness reports including TensorRT+FP16 non-finite audio and streaming device-mismatch failures. No neural-quality improvement claim exists until a provisioned 1.7B runtime is benchmarked on the same checked-in dialogue.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

A real identity-preservation claim still requires an operator-owned reference-conditioned runtime plus rights-safe benchmark assets. This environment does not contain a provisioned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V, WanGP or equivalent compliant GPU/model runtime.

Normal unattended Hottop must not auto-download multi-GB weights, provision GPU, consume credits or weaken the evidence boundary. A production identity claim still requires exact reference bytes, stable subject IDs, complete subject-bearing shot coverage, generated-video quality gates, generator/model/evaluator provenance and byte-bound generated artifacts.

## Current ecosystem radar

Targeted 2026-08-26 checks still do not justify changing a tested default:

- **LightX2V** upstream `main` remains `5dc5d6372654406761474719647763ac7b4bd018`; the latest visible change is a SwiftVR BF16→NumPy export fix, with no measured Hottop Wan2.2 benefit that justifies a freshness-only repin.
- **MiniMax H3 through LightX2V** remains an operator benchmark candidate; weights/output-rights, hardware and local benchmark gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local Mandarin role-aware candidate; acceleration stacks do not displace the reviewed local adapter without real A/B evidence.
- **CosyVoice3** remains a comparison candidate rather than a default because recent configuration-specific correctness failures reinforce finite-audio/device correctness gates.
- **SigLIP 2 Base 256** remains the preferred first local continuity evaluator experiment only when exact local weights/revision/hash are explicitly supplied.
- FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk, DINOv3, DreamSim and newly discovered projects remain behind separate code-license, weights/data/output-rights, hidden-download/network, hardware, security, cost, benchmark-value and rollback gates.

Durable rule: popularity/freshness is not admission evidence; code license is not model/weights/data/output-rights clearance.

## Immediate next actions

1. Produce and archive a **real 720×1280/24fps Odyssey artifact using `cinematic-software3d-delivery.yml`** with the same dialogue/music/Foley, MoviePy, FFmpeg, final-media and provenance gates. Use a dedicated/on-demand delivery evidence path rather than making every ordinary PR pay the 720p render cost.
2. Continue direct artifact inspection and change deterministic visuals/audio only when a measurable failure appears.
3. When an operator-provisioned Qwen3-TTS 1.7B runtime exists, run same-dialogue eSpeak-family vs Qwen A/B; no quality claim before real audio evidence.
4. When a compliant operator-owned reference-conditioned runtime plus rights-safe assets exists, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
5. Continue targeted ecosystem scans against measured gaps; integrate only candidates clearing source/license/weights/cost/hardware/security/reversibility/value gates.
6. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain test fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production-smoke.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
