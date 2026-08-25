# Autonomous Ecosystem Radar

This document is a durable operating policy for Hottop and is subordinate only to `PROJECT.md` when the two conflict. It exists to make the project's autonomy and ecosystem-maintenance rules recoverable across sessions.

## Autonomous decision rule

For normal, reversible work inside `jinngimk-lang/hottop`, the operator delegates routine engineering and creative decisions to the Hottop owner loop. Do not stop for ordinary approval when the repository, evidence, tests, and current project charter are sufficient to choose a safe path.

Continue useful work within the same run while the environment and permissions allow it. Pause only for destructive or irreversible actions, credentials or secrets, paid actions or credit consumption, new legal commitments or terms, KYC or identity steps, sensitive external publication, or other actions whose consequence cannot be safely inferred from the existing authorization.

Missing tools, skills, plugins, or MCP integrations may be discovered and installed/connected when they address a concrete Hottop gap, have a clear rollback path, do not require paid actions or new legal acceptance, do not broaden access unnecessarily, and pass a source/security/license check.

## Continuous ecosystem intelligence

Ecosystem maintenance is part of the product, not an occasional research task. Every autonomous run should perform a lightweight targeted check of upstream projects directly relevant to the current production gap. At least every few hours, or sooner when a material release/security/license/runtime event is likely, perform a broader scan of official GitHub repositories, releases, model cards, papers, official docs, and trustworthy technical news.

Priority areas include video T2V/I2V/S2V, identity and character consistency, animation/restylization, low-VRAM inference, temporal extension, frame interpolation, upscaling, TTS/voice, original music/audio generation, Foley, ComfyUI/workflow orchestration, deterministic editing/encoding, and quality evaluation.

The watchlist is open-ended. Current examples include Wan2.2, WanGP, FramePack, LTX/LTX-2, HunyuanVideo, FastVideo, ViMax, Toonflow, ComfyUI, Diffusers, RIFE, Real-ESRGAN, InfiniteTalk, SCAIL-2, and stronger candidates discovered later.

### Current material findings

- **SCAIL-2 (`zai-org/SCAIL-2`)** — official Apache-2.0 implementation for controlled character animation with end-to-end in-context conditioning. As of August 2026 it has multi-reference inference, ComfyUI integration, animal-driving/character-replacement support, and newly released training code. This is a strong fit for Hottop's identity-continuity gap, but the 14B-class checkpoint and preprocessing stack remain operator-owned; Hottop should integrate through an isolated adapter or Comfy workflow rather than downloading the model automatically.
- **WanGP (`DeepBeepMeep/Wan2GP`)** — remains a high-value low-VRAM operator backend. The August 2026 line has moved beyond the originally reviewed stack and now exposes newer LTX 2.5 / upsampling paths in addition to Wan/Hunyuan/LTX families. This reinforces the adapter-first policy: Hottop should track capability/profile metadata rather than bind its core plan schema to a specific WanGP model release.

These notes are not permission to execute a model. Code and model/weights licenses, model-card terms, hardware, and current runtime safety must still be checked at integration time.

## Integration gate

Do not integrate a project because it is popular. Before adoption, verify:

- exact upstream repository/source and maintenance freshness;
- code license separately from model/weights license;
- commercial, geographic, and redistribution restrictions;
- hardware/runtime requirements and actual zero-cost feasibility;
- install/runtime security and credential boundaries;
- headless/API maturity and failure behavior;
- measurable value against a current Hottop gap;
- isolation, rollback, and testability.

When a candidate is materially better, integrate the smallest compatible adapter, config, algorithm, or test. Do not vendor large third-party repositories by default. For incompatible licenses such as AGPL in a non-AGPL core, learn from architecture and behavior without copying code.

Every material integration should have a benchmark, acceptance test, or production-evidence criterion so later replacements are evidence-based.

## Charter synchronization

When this radar produces a durable new direction, architecture, safety boundary, integration strategy, style rule, or proven production pattern, update `PROJECT.md` and the relevant reusable skill/spec in the same workstream. `STATUS.md` records transient branch/CI/next-action state; the charter records durable doctrine.

If `PROJECT.md` is later edited, fold this policy into its Repository Operating Rules / Decision Log and keep this document as the detailed operating reference.