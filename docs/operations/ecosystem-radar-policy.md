# Hottop Ecosystem Radar Policy

This document is intentionally small. `PROJECT.md` remains the canonical charter; this file records the operational mechanics for continuous upstream discovery.

## Purpose

Hottop must continuously improve rather than freeze around whatever model, renderer, TTS, compositor, retrieval stack, or workflow happened to be available when a milestone started.

## Operating rule

When the active implementation can safely continue in the current run, continue it. Do not stop merely because a sub-step, CI run, design checkpoint, or intermediate milestone completed. Pause only for a real boundary that requires user involvement: destructive or irreversible action, credentials/secrets, paid spend or credit enrollment, legal acceptance/commitment, sensitive external publication, or an unavailable capability that cannot be replaced safely.

## Upstream radar

At least once per autonomous hourly run, inspect the current project gap first, then check fresh upstream evidence only for technologies plausibly able to close that gap. Sources should favor official repositories, release notes, model cards, licenses, papers, documentation, and security advisories.

Candidate classes include video/image generation, character/reference consistency, motion control, low-VRAM inference, frame interpolation, restoration/upscaling, TTS, music/audio generation, orchestration, browser/research acquisition, quality evaluation, media tooling, and safe local/cloud execution.

For each candidate, distinguish code license from model/weights/data license; record maintenance/freshness, hardware and runtime needs, zero-cost practicality, commercial/geographic restrictions, security/install behavior, interface maturity, and measurable project value.

## Integration rule

Do not integrate a project merely because it is newer or popular. Integrate only when it closes a measured Hottop gap and the change is source-verifiable, rights/license-compatible for the intended use, zero-cost-compatible by default, testable, isolated behind a stable adapter or internal contract, and safely reversible.

Prefer extracting a small capability or adapter over vendoring a large upstream repository. Do not copy incompatible-license code into Hottop. Do not auto-download large model weights, auto-install opaque custom nodes, or enable paid endpoints in unattended execution.

When a better direction survives review, update `PROJECT.md`, the relevant reusable skill/spec, and `STATUS.md` in the same workstream so future runs recover the new canonical direction rather than stale assumptions.

## Current production bias

Production v0.2 prioritizes repeatable config-to-MP4 evidence and presentable real motion over additional abstraction. The deterministic software-3D path is a zero-cost baseline/fallback, not a quality ceiling. Free shared GPU and operator-owned open model backends should be measured against that baseline for identity, motion, visual quality, audio, reproducibility, license safety, and failure recovery.
