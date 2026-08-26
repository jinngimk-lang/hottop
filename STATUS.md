# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — repeatable presentable zero-cost delivery; operator-local generated/TTS quality when provisioned**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

Current `main`: `45ecfeb7d34ed32408839d780a96682c9ced1e95` (`prod: bind delivery evidence to canonical source bytes`, squash merge of PR #83).

- PR #83 exact GREEN head: `c22f5a240302351f6f746a6d7d7739535085d084`.
- Exact-head CI **1660** passed Ruff + full pytest on Python 3.11/3.12.
- Post-merge `main` CI **1661** passed.
- No paid service, credential, provider-routing or media-generation behavior changed in #83.

PR #83 closes a durable provenance gap in the checked-in 720p Odyssey delivery proof. `examples/runs/odyssey-cinematic-software3d-delivery.evidence.json` now binds the canonical render and delivery config by both path **and SHA-256 bytes**, so later fixture/profile edits cannot silently make old evidence appear to prove current source files. The manifest already binds workflow/artifact/final-media/shot bytes; source bytes are now part of the same evidence chain.

## Guaranteed zero-cost software3d baseline

The lightweight repeatedly exercised smoke profiles remain intentionally small:

- `anti-polish-software3d.yml`: 360×640, 12 fps;
- `cinematic-software3d.yml`: 360×640, 12 fps.

They exist to keep full config→media→provenance evidence cheap and repeatable in CI. They are **not** a cinematic delivery ceiling.

The guaranteed route has real production evidence for checked-in render/config → actual moving 3D shots → Mandarin eSpeak-NG/eSpeak dialogue with preserved `speaker + delivery` semantics → original synthetic music/procedural Foley → dialogue-aware MoviePy composition → FFmpeg H.264/AAC/yuv420p/fast-start finalization. It carries final AAC activity/duration checks, byte-bound per-shot provenance + immediate pre-composition re-verification, perceptible-motion/mobile-framing/subtitle contracts, and zero GPU/model-download/credential/paid-service requirements.

## Presentable cinematic software3d delivery evidence — PROVEN

`config/video/cinematic-software3d-delivery.yml` remains the deterministic presentable-delivery profile: **720×1280, 24 fps**, `software3d → MoviePy → FFmpeg`, cinematic/lower-roughness semantics, Mandarin guaranteed local voice fallback, original synthetic score/Foley, and no URL/QR/GPU/model/credential/paid API requirement.

The scoped `cinematic-delivery-smoke` proof produced a real 15.0-second MP4. Durable checked-in evidence records:

- workflow head/run and GitHub artifact digest;
- final MP4 SHA-256 and H.264/yuv420p/AAC media contract;
- five byte-bound software3d shot records;
- canonical render SHA-256 and delivery-config SHA-256;
- measured motion/audio/luminance inspection and deterministic-only claim scope.

Large media remains out of Git. This proof does **not** upgrade deterministic software3d into a generated/reference-conditioned identity claim.

## Operator-local Mandarin TTS

Qwen3-TTS CustomVoice remains the preferred non-default role-aware Mandarin benchmark candidate behind fail-closed local preflight. eSpeak-NG/eSpeak remains the guaranteed zero-cost/offline fallback. Current official 0.6B CustomVoice ignores `instruct`; current 1.7B is the admitted delivery-control benchmark target. No package/model auto-install or network model fetch is allowed, and preset-speaker/output publication rights remain an operator gate separate from Apache-2.0 metadata.

Fresh 2026-08-26 review still does not justify a default change. H100/H200 acceleration stacks remain operator benchmark infrastructure. CosyVoice3 still has recent correctness reports including TensorRT+FP16 non-finite audio and streaming device-mismatch failures, so it remains a comparison candidate rather than a default.

Research record: `docs/research/2026-08-26-qwen3-customvoice-routing.md`.

## Generated/reference-conditioned identity gap

A real identity-preservation claim still requires an operator-owned reference-conditioned runtime plus rights-safe benchmark assets. This environment does not contain a provisioned LightX2V/Wan2.2, MiniMax-H3-through-LightX2V, WanGP or equivalent compliant GPU/model runtime.

Normal unattended Hottop must not auto-download multi-GB weights, provision GPU, consume credits or weaken the evidence boundary. A production identity claim still requires exact reference bytes, stable subject IDs, complete subject-bearing shot coverage, generated-video quality gates, generator/model/evaluator provenance and byte-bound generated artifacts.

## Current ecosystem radar

Targeted 2026-08-26 freshness check:

- **LightX2V:** upstream `main` moved from the previously observed `5dc5d637…` to `aa1b7b5921d73fb42a605a3f4f3519b0554bb7e6` on 2026-08-26. The new commit adds SwiftVR single-image super-resolution support, larger-input RoPE handling and related MP4/checkpoint-conversion work. This is material upstream maintenance, but Hottop currently has no measured delivery failure that requires an SR stage and no operator benchmark proving gain on the tested Wan2.2 route. **Do not freshness-only repin or add a post-process dependency.**
- **Qwen3-TTS:** official repository `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; community H100/H200 and MLX serving work does not replace the reviewed operator-local adapter without same-dialogue A/B evidence.
- **CosyVoice3:** recent TensorRT+FP16 NaN and streaming STFT device mismatch reports reinforce finite-audio/device correctness gates.
- **MiniMax H3 / FramePack / FastVideo / LTX / SCAIL / LongCat / InfiniteTalk / RIFE / Real-ESRGAN:** remain behind separate code-license, weights/data/output-rights, hidden-download/network, hardware, security, cost, benchmark-value and rollback gates.

Durable rule remains unchanged: popularity/freshness is not admission evidence; code license is not model/weights/data/output-rights clearance.

## Immediate next actions

1. Treat the 720×1280/24fps Odyssey delivery proof, including canonical source-byte hashes, as the present deterministic zero-cost delivery baseline. Re-run the scoped workflow on relevant delivery-path changes, not every ordinary PR.
2. Continue direct inspection of real delivery artifacts and change deterministic visuals/audio only when a measurable failure appears; do not blindly retune camera, brightness, subtitles, mix or add SR/interpolation/upscale stages after a passing sample.
3. When an operator-provisioned Qwen3-TTS 1.7B runtime exists, run same-dialogue eSpeak-family vs Qwen A/B; no quality claim before real audio evidence.
4. When a compliant operator-owned reference-conditioned runtime plus rights-safe assets exists, execute a real multi-shot identity/style benchmark before changing defaults or claiming identity preservation.
5. Continue targeted ecosystem scans against measured gaps; integrate only candidates clearing source/license/weights/cost/hardware/security/reversibility/value gates.
6. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain test fixtures, not creative defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
