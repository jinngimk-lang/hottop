# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable presentable zero-cost delivery; operator-local generated/TTS quality when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Current production `main` at this snapshot: `f30eabf60f6f18ad1f0196806de6253e3726d50c` (`ci: prove cinematic software3d delivery output`, squash merge of PR #80).

PR #80 closed the previously open delivery-evidence gap without making every ordinary PR pay the full 720p render cost:

- exact PR head: `1cab4dfb4afb6b2611235025fd0cc04b7e2ab0ec`;
- normal CI **1647** passed Ruff + full pytest on Python 3.11/3.12;
- on-demand `cinematic-delivery-smoke` **1** completed successfully on Ubuntu 24.04;
- the real `video-run --execute` 720×1280/24fps Odyssey stage took about **9m51s**, well inside its scoped 25-minute evidence budget;
- media/provenance verification and artifact upload succeeded;
- the archived workflow artifact `hottop-cinematic-software3d-delivery` is bound to the exact PR head and has GitHub artifact digest `sha256:eb5c67f3d6c0cf3e88d52045e9e3ef60492fbbe395f5ebc9fb1590faf54d55b4`.

Post-merge `main@f30eabf6…` CI **1648** passed. The same scoped cinematic-delivery workflow is also configured to re-prove the delivery path on relevant `main` pushes; re-fetch its newest run before citing it.

## Guaranteed zero-cost software3d baseline

The lightweight, repeatedly exercised smoke profiles remain intentionally small:

- `anti-polish-software3d.yml`: 360×640, 12 fps;
- `cinematic-software3d.yml`: 360×640, 12 fps.

They exist to keep full config→media→provenance evidence cheap and repeatable in CI. They are **not** a cinematic delivery ceiling.

The guaranteed route has real production evidence for checked-in render/config → actual moving 3D shots → Mandarin eSpeak-NG/eSpeak dialogue with preserved `speaker + delivery` semantics → original synthetic music/procedural Foley → dialogue-aware MoviePy composition → FFmpeg H.264/AAC/yuv420p/fast-start finalization. It also carries final AAC activity/duration checks, byte-bound per-shot provenance + immediate pre-composition re-verification, perceptible-motion/mobile-framing/subtitle contracts, and zero GPU/model-download/credential/paid-service requirements.

## Presentable cinematic software3d delivery evidence — PROVEN

`config/video/cinematic-software3d-delivery.yml` is the current deterministic presentable-delivery profile:

- **720×1280, 24 fps**;
- `software3d → MoviePy → FFmpeg`;
- cinematic/lower-roughness semantics with Anti-Polish disabled;
- Mandarin guaranteed local voice fallback, original synthetic score and procedural Foley;
- no URL/QR;
- no GPU, model, credential, paid API or hidden network requirement.

The prior statement that no 720×1280/24fps Odyssey delivery artifact existed is now obsolete. `cinematic-delivery-smoke` **1** produced and archived a real 15.0-second MP4 and evidence bundle.

Independent artifact re-inspection after the workflow completed confirmed:

- final MP4: **720×1280, 24/1 fps, 15.000 s**;
- video: **H.264 / yuv420p**;
- audio: **AAC**, 15.000 s;
- final MP4 SHA-256: `a22fc5bb03bee2815d2dca532c123ac6de1454e737719b3e702f1e35189f8fa6`;
- five shot sidecars all identify `planned_generation_backend=software3d`, `artifact_kind=deterministic-generated`, exact shot SHA-256 and byte size;
- sampled frames at 1/4/7/10/13 seconds retained stable Odyssey staging, lower-roughness directional depth and readable Mandarin subtitles; no delivery-profile-specific deterministic visual regression was found;
- sampled luminance stayed stable around mean **47–48/255** with useful geometric contrast and no evidence from this sample that another global brightness/framing adjustment is warranted.

Durable execution distinction already follows `PROJECT.md`'s “software3d baseline is not the cinematic ceiling” rule: **smoke evidence and delivery evidence serve different budgets**. Keep ordinary smoke lightweight; use the scoped delivery workflow when a presentable artifact must be proved. Do not treat lightweight CI success alone as delivery-quality proof.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains the preferred non-default role-aware Mandarin benchmark candidate behind fail-closed local preflight. eSpeak-NG/eSpeak remains the guaranteed zero-cost/offline fallback. Current official 0.6B CustomVoice ignores `instruct`; current 1.7B is the admitted delivery-control benchmark target. No package/model auto-install or network model fetch is allowed, and preset-speaker/output publication rights remain an operator gate separate from Apache-2.0 metadata.

Fresh 2026-08-26 review still does not justify a default change. H100/H200 acceleration stacks remain operator benchmark infrastructure, while CosyVoice3 has recent correctness reports including TensorRT+FP16 non-finite audio and streaming device-mismatch failures. No neural-quality improvement claim exists until a provisioned 1.7B runtime is benchmarked on the same checked-in dialogue.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

A real identity-preservation claim still requires an operator-owned reference-conditioned runtime plus rights-safe benchmark assets. This environment does not contain a provisioned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V, WanGP or equivalent compliant GPU/model runtime.

Normal unattended Hottop must not auto-download multi-GB weights, provision GPU, consume credits or weaken the evidence boundary. A production identity claim still requires exact reference bytes, stable subject IDs, complete subject-bearing shot coverage, generated-video quality gates, generator/model/evaluator provenance and byte-bound generated artifacts.

## Current ecosystem radar

Targeted 2026-08-26 checks still do not justify changing a tested default:

- **LightX2V** recent visible maintenance does not show a measured benefit for Hottop's tested Wan2.2 subset; do not freshness-only repin.
- **MiniMax H3 through LightX2V** remains an operator benchmark candidate; weights/output-rights, hardware and local benchmark gates remain uncleared.
- **Qwen3-TTS CustomVoice** remains the preferred operator-local Mandarin role-aware candidate; acceleration stacks do not displace the reviewed local adapter without real A/B evidence.
- **CosyVoice3** remains a comparison candidate rather than a default because recent configuration-specific correctness failures reinforce finite-audio/device correctness gates.
- **SigLIP 2 Base 256** remains the preferred first local continuity evaluator experiment only when exact local weights/revision/hash are explicitly supplied.
- FramePack, FastVideo, LTX, SCAIL, LongCat, InfiniteTalk, DINOv3, DreamSim and newly discovered projects remain behind separate code-license, weights/data/output-rights, hidden-download/network, hardware, security, cost, benchmark-value and rollback gates.

Durable rule: popularity/freshness is not admission evidence; code license is not model/weights/data/output-rights clearance.

## Immediate next actions

1. Treat the 720×1280/24fps Odyssey delivery proof as the present deterministic zero-cost delivery baseline. Re-run it on relevant delivery-path changes, not every ordinary PR.
2. Continue direct inspection of the real 720p artifact and change deterministic visuals/audio only when a measurable failure appears; do not blindly retune camera, brightness, subtitles or mix after a passing sample.
3. Track delivery runtime as a practical budget: the current GitHub-hosted CPU proof rendered the real 720p24 execution stage in about 9m51s. Optimize only if later evidence shows this budget materially blocks use; do not lower resolution/fps and call it equivalent proof.
4. When an operator-provisioned Qwen3-TTS 1.7B runtime exists, run same-dialogue eSpeak-family vs Qwen A/B; no quality claim before real audio evidence.
5. When a compliant operator-owned reference-conditioned runtime plus rights-safe assets exists, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
6. Continue targeted ecosystem scans against measured gaps; integrate only candidates clearing source/license/weights/cost/hardware/security/reversibility/value gates.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain test fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
