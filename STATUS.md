# Hottop Status

Last updated: 2026-08-26
Active workstream: **Production v0.2 — dual-DGX local multimodal generation fabric + real cinematic-motion proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot; re-fetch GitHub before exact head/CI claims.

## Current repository truth

PR #86 (`feat/dgx-spark-local-model-hub`) is the active workstream from `main@5f80ef0c1bd39c14499c1df8cded9f5ad8e0145a`.

TDD evidence:

- first test-only CI was blocked by a Ruff formatting issue and was not accepted as RED;
- corrected test-only head `a3086b69cee5e76f4ee00332db8f974ad21daa20` passed Ruff and failed pytest on Python 3.11/3.12 because `hottop.model_hub` did not exist;
- implementation is now adding the model hub, operator profile, probe, one-stop selector and durable local-fabric spec; exact-head GREEN remains required before merge.

## Declared local operator compute

The user has declared **two local NVIDIA DGX Spark systems**. Hottop must treat this self-owned pool as the preferred heavy-compute execution surface before paid SaaS.

Canonical profile: `config/operator/dgx-spark-dual.yml`.

Known platform capability recorded for routing/planning:

- NVIDIA GB10 Blackwell per node;
- 128 GB coherent unified memory per node;
- 273 GB/s memory bandwidth per node;
- ConnectX-7 200 Gbps capable networking;
- 256 GB aggregate physical unified-memory capacity across two systems.

Do **not** treat the two-node aggregate as one automatically shared GPU memory address space.

Actual operator runtime facts remain intentionally unverified until the machines are probed: hostname, DGX OS, driver, CUDA, PyTorch, free disk, local model paths and configured ConnectX/RDMA/network state. Run `python scripts/probe_dgx_spark.py` on each host. Current NVIDIA release versions are not proof of what is installed on the user's machines.

## Creative/production hierarchy remains above model routing

The local GPU pool changes the execution strategy, not Hottop's purpose. Every asset still follows:

`fresh/supplied hotspot evidence → promotion objective → hotspot mechanism → product role/outcome change → script/beat sheet → character/world bible + identity locks → keyframes/style frames → model selection → real image/video generation → continuity review → voice/BGM/SFX → post/final media verification → campaign-effect review`

Hard rules:

- maximize hotspot recognition + product relevance + promotional purpose before optimizing model quality;
- product must change the story outcome through a defensible product truth/metaphor;
- film/live-action hotspots require original cinematic/live-action grammar; crude 3D is only valid when that roughness is the hotspot-native grammar;
- cinematic video requires real character/environment/action motion; stills with pan/zoom/Ken-Burns movement are **not** accepted as video;
- script, character identity, costume/props, scene geography, action continuity, image/video style and audio grammar must remain coherent;
- paid SaaS is not a default fallback.

Durable operator spec: `docs/operations/dgx-spark-local-model-fabric.md`.

## One-stop multimodal model hub

Canonical registry: `integrations/model-hub.yml`.

Safe discovery surface: `hottop-models list`.

The registry unifies image generation/editing, I2V/T2V, character animation, speech-driven video, restoration, interpolation, TTS and workflow interoperability without vendoring third-party repositories or auto-downloading weights.

Current priority stack:

1. **LightX2V + Wan2.2 I2V A14B** — primary existing local cinematic reference-conditioned route.
2. **LightX2V Wan2.2 NVFP4 sparse Blackwell path** — high-priority dual-DGX benchmark; upstream speed claims are not Hottop evidence.
3. **Wan2.2 TI2V 5B** — 720p real-motion benchmark candidate.
4. **Wan2.2 Animate 14B** — character animation/replacement candidate; identity still requires output-side evidence.
5. **Wan2.2 S2V 14B** — speech-driven motion benchmark candidate.
6. **Qwen-Image 2.x** — keyframe/image/editing candidate for high-quality style/identity lock.
7. **Qwen3-TTS 1.7B CustomVoice** — local role/delivery Mandarin candidate behind existing rights gate.
8. **Real-ESRGAN** — restoration/SR only; cannot satisfy motion generation.
9. **RIFE** — interpolation only; cannot turn static-slide motion into cinematic action.
10. **ComfyUI** — isolated GPL interoperability/orchestration; do not vendor.

FramePack/LTX/LongCat/SCAIL/MiniMax H3/WanGP and future candidates remain registry/radar candidates until their exact code+weights rights, local runtime, quality and rollback gates clear. Newer LTX-2.x remains license-blocked for default commercial routing until its current commercial terms are cleared for the operator entity.

Paid video SaaS is represented only as an excluded class so default selection can prove it never leaks into zero-cost routing.

## Guaranteed deterministic baseline

The existing software3d → local audio → MoviePy → FFmpeg route remains valuable because it is reproducible, zero-GPU and evidence-rich. It remains a **style-appropriate deterministic baseline**, not the cinematic quality ceiling and not a fallback allowed to satisfy a photorealistic-film request.

The checked-in presentable deterministic delivery path remains 720×1280 / 24 fps and has real H.264/AAC evidence. Keep that proof for regression safety while the new local generative stack earns its own evidence.

## Immediate next actions

1. Finish PR #86 exact-head Ruff + full pytest on Python 3.11/3.12; review diff and merge only after GREEN.
2. Run `scripts/probe_dgx_spark.py` separately on both physical DGX Spark systems and record the actual runtime facts outside Git when local/private details should not be committed.
3. Provision/pin one reviewed local LightX2V/Wan2.2 route on the operator machines; Hottop itself must not silently install or download multi-GB models.
4. Use the Odyssey/Cyclops deployment-island concept as the first **true-motion** benchmark because the previous slideshow-like attempt clearly exposed the failure boundary.
5. Build a character/world bible + approved cinematic keyframes, then generate at least two subject-bearing real I2V shots with actual human/giant/environment motion.
6. Bind generator source revision, checkpoint provenance, reference bytes and shot hashes; run motion + cross-shot continuity evidence before composition.
7. Add role-aware Mandarin voice, original cinematic BGM and synchronized Foley/SFX, compose and verify the final H.264/AAC vertical short.
8. Visually inspect the real artifact. Reject slideshow motion, identity drift, broken geography, weak hotspot/product mapping or audio that undermines the scene.
9. Continue targeted ecosystem scans; integrate only candidates that materially improve a measured gap and clear license/cost/hardware/security/quality gates.
10. For every future creative request, continue live hotspot research when none is supplied; a supplied hotspot is analyzed first rather than replaced by a generic trending template.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. `docs/operations/dgx-spark-local-model-fabric.md`.
4. `config/operator/dgx-spark-dual.yml`.
5. `integrations/model-hub.yml`.
6. relevant reusable creative/video skills.
7. newest relevant benchmark/spec/decision/research record.
8. current `main`, open PRs and exact-head CI/production evidence.
9. targeted ecosystem scan for the measured gap.
10. fresh hotspot/mechanism analysis for new creative generation.
11. continue the highest-value safe action autonomously.
