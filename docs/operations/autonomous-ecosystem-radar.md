# Autonomous Ecosystem Radar

This document is the detailed operating policy for Hottop's autonomous maintenance and is subordinate only to `PROJECT.md` when the two conflict. It exists so ecosystem research becomes production improvement rather than a pile of links.

## Autonomous decision rule

For normal, reversible work inside `jinngimk-lang/hottop`, routine engineering, creative and integration decisions are delegated to the Hottop owner loop. Do not stop for ordinary approval when repository truth, current evidence, tests and the charter are sufficient to choose a safe path.

Continue useful work within the same interactive run while environment and permissions allow it; a scheduled-loop boundary is not a stopping condition. The hourly loop is a recovery/persistence mechanism, not the only time work may advance.

Pause only for destructive or irreversible actions, credentials/secrets, paid actions or credit consumption, new legal commitments/terms, KYC/identity steps, sensitive external publication, or another action whose consequences cannot be safely contained by existing authorization.

Missing tools, skills, plugins or MCP integrations may be discovered and installed/connected when they solve a concrete Hottop gap, have a clear rollback path, do not require paid actions/new legal acceptance, do not unnecessarily broaden access, and pass source/security/license review. Never install something merely because it is available.

## Continuous ecosystem intelligence

Ecosystem maintenance is part of the product. Every autonomous production cycle should perform a **targeted freshness check** of upstreams relevant to the current bottleneck. A broader scan is useful when a material release, security issue, license change or architecture shift is likely; do not mechanically rescan the same ecosystem when nothing changed.

Priority areas:

- T2V/I2V/S2V and multi-reference character/identity consistency;
- animation/restylization and temporal extension;
- low-VRAM, CPU or operator-owned local inference;
- verified free shared-GPU execution;
- keyframe/reference image generation;
- interpolation, temporal restoration and upscaling;
- Mandarin/multilingual expressive TTS and safe voice design;
- original music/audio generation and Foley;
- ComfyUI/workflow/headless orchestration;
- deterministic editing/encoding and media QA;
- security, licenses, breaking APIs and runtime changes.

The watchlist is open-ended. Current examples include Wan2.2/WanGP, FramePack, FastVideo, LTX, MiniMax H3, SCAIL-2, LongCat, HunyuanVideo, ComfyUI/Diffusers, RIFE, Real-ESRGAN, InfiniteTalk, Fun-CosyVoice/CosyVoice3, Qwen3-TTS and stronger candidates discovered later.

## Admission gate

Popularity is not an admission criterion. Before adoption, verify:

1. exact upstream repository/source and tested revision;
2. code license separately from model/checkpoint/weights license;
3. commercial, geographic, redistribution and usage restrictions;
4. true zero-cost or operator-owned feasibility and absence of hidden paid fallback;
5. hardware/runtime requirements for a defined production profile;
6. install/runtime/network behavior, credential handling and security isolation;
7. headless/API maturity and bounded failure behavior;
8. a concrete measured Hottop gap it improves;
9. reversible adapter/config/test boundaries and a rollback path;
10. a benchmark, acceptance test or production case capable of proving the improvement.

A permissive repository license does not automatically authorize its weights or hosted endpoint. Use of a model whose terms themselves create a new legal acceptance is operator-controlled even when technically free.

For incompatible code licenses such as AGPL in a non-AGPL core, learn from architecture and behavior but do not copy implementation into Hottop. Reimplement the useful behavior cleanly if it is worth keeping.

## Integration rule: research must close the loop

When a candidate materially clears the admission gate, **do not stop at a research note**. Integrate the smallest useful unit:

- a machine-readable registry entry with exact provenance/license/runtime status;
- a provider/CLI/API adapter;
- a production profile or workflow contract;
- a selectively ported permissive algorithm/file when narrow reuse is cleaner than an adapter;
- acceptance/benchmark tests;
- representative production evidence.

Prefer narrow interfaces to vendoring entire upstream repositories. Never auto-install unreviewed code or silently download multi-gigabyte models in CI or normal `video-run`. Operator-owned model stacks remain explicit dependencies outside the core repository unless later evidence justifies a different packaging strategy.

If the candidate does **not** clear the gate, record the reason precisely (`weights_license_review`, `hardware_blocked`, `gui_only`, `no_measured_gain`, etc.) so the loop does not repeatedly rediscover the same blocker without new evidence.

## Current material findings

- **SCAIL-2 (`zai-org/SCAIL-2`)** — Apache-2.0 code implementation for controlled character animation with multi-reference/in-context conditioning and relevant character-replacement/animal-animation capabilities. It is a strong identity-continuity benchmark candidate; checkpoint/runtime size and exact weights terms remain execution gates. Prefer an isolated adapter or reviewed Comfy workflow rather than automatic provisioning.
- **WanGP (`DeepBeepMeep/Wan2GP`)** — high-value low-VRAM operator backend whose supported model set evolves quickly. Keep Hottop bound to its stable headless/API/Settings boundary and capability metadata, not a specific model release. WanGP's own distribution/commercial terms remain separate from every model it runs.
- **MiniMax H3 (`MiniMaxAI/MiniMax-H3`)** — technically attractive for reference-conditioned and synchronized audio/video generation, but the weights/usage terms are not a permissive drop-in OSS default. Keep it `license-gated/operator-approved`; never auto-download or silently route unattended production to it.
- **LongCat Video / Avatar** — relevant to character/avatar consistency and synchronized performance; keep exact checkpoint/license/runtime status in the candidate registry before production enablement.
- **Fun-CosyVoice / CosyVoice3** — strong local Mandarin/multilingual TTS family. Hottop already has a rights-gated local CosyVoice3 adapter. Reference voice audio is treated like image references: local file, explicit rights provenance, no arbitrary URL scraping and no silent voice cloning/model download.
- **Qwen3-TTS 0.6B Base** — high-priority permissive local TTS benchmark recorded in the registry. Open voice-cloning capability does not relax voice rights; unattended use should favor designed/preset/otherwise rights-safe voices or explicit rights-cleared reference audio.
- **software3d** — Hottop's own deterministic low-poly 3D renderer is now the guaranteed zero-cost motion baseline. External candidates should beat it on a defined visual/identity/production metric rather than merely exist.

These notes are not permission to execute a model. Re-check exact current repository/model-card/license/runtime facts at integration time because upstream state can change.

## Benchmark discipline

Compare candidates against the **current working route**, not an imagined ideal. Depending on the gap, measure:

- identity/reference retention across shots;
- actual frame motion vs duplicate/static output;
- prompt/action adherence;
- scene/action continuity;
- readable product semantics;
- visual quality at the selected `roughness_score`;
- Mandarin dialogue intelligibility/prosody;
- synchronized audio/video quality;
- VRAM/RAM/runtime and setup burden;
- output decodability/codec compliance;
- license/rights operational burden.

A model that is prettier but destroys identity, requires paid credits, silently downloads large checkpoints, or has incompatible rights is not an upgrade for the unattended route.

## Charter synchronization

When the radar yields a durable direction, architecture, safety boundary, integration strategy, style rule or proven production pattern, update `PROJECT.md` and the relevant reusable skill/spec **in the same workstream**. `STATUS.md` records transient branch/CI/next action; the charter records durable doctrine.

Periodically audit `PROJECT.md` for stale milestones, duplicated doctrine or old assumptions that conflict with newly accepted evidence. Supersede them explicitly rather than stacking contradictory text.
