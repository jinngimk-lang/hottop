# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — fresh-generation gate + operator-owned cinematic quality proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Hottop now has three complementary production layers:

1. a **mandatory fresh-generation entry gate** for every new image/video request;
2. a guaranteed **zero-cost deterministic software3d → audio → MoviePy → FFmpeg → verified MP4** baseline; and
3. isolated operator-owned/open generation routes that can be benchmarked without changing the provider-neutral creative/runtime contract.

Closed production evidence:

- PR #12 established the reproducible software3d config-to-MP4 loop with byte-bound provenance manifests and final media verification.
- PR #15 generalized software3d story routing beyond the cow/snake flagship and added the Odyssey witch/pigs cinematic profile; it was squash-merged as `01e54432978f9694ea79a645e8b53308c474f3d5`.
- PR #13 added the benchmark-ready offline local Qwen3-TTS 0.6B CustomVoice adapter and was merged as `b9743763316f240d5c095c84bc5f2f071ee32716`.
- PR #14 added the first-class operator-managed LightX2V/Wan2.2 T2V/I2V backend and was merged as `e32a0632d1245752baa0b60cd464a18af110a8df`.
- `8410458fd9cbc416f0cb98fa39001f685f6feb7c` added the reusable checked-in LightX2V/Wan2.2 I2V operator profile and registry boundary.
- `859f2c382119facf96b3c6147e0b85fff979f514` bound accepted LightX2V shot bytes to artifact provenance and re-verification before composition.

## Fresh-generation preflight deployment

PR #23 (`feat/fresh-hotspot-generation-preflight`) implements the user's hard requirement that **every new image/video generation request starts from newly researched current hotspot evidence and a new product/hotspot/style/format decision** rather than inheriting an old example.

Runtime/API:

- `src/hottop/generation_preflight.py` defines `GenerationPreflightInput`, `GenerationPreflightResult`, and `evaluate_generation_preflight(...)`.
- schema: `hottop.generation-preflight.v1`;
- required dynamic fields: promoted `product`, selected `hotspot`, `visual_style`, `style_rationale`, `output_format`, `output_kind`, and timezone-aware `researched_at`;
- default freshness gate: research observation <= **6 hours**; known hotspot publication <= **7 days**;
- fail-closed blockers include missing/stale evidence, stale research observation, and stale known publication time;
- unknown publication time may pass only with fresh observed evidence and remains unknown rather than being invented.

Operator/Chat entrypoint:

- `hottop generation-preflight <json> [--now ...]` runs the same gate; blocked inputs exit non-zero.
- `PROJECT.md`, `skills/brand-metaphor-creative/SKILL.md`, and `skills/hottop-meme/SKILL.md` require Chat generation to reread repository truth, perform a new live hotspot/news/culture/internet scan for each asset request, select product/hotspot/style/format dynamically, and pass the preflight before final image/video generation.
- Historical cow/snake/Odyssey/four-panel/Anti-Polish/low-poly/cinematic examples remain reusable grammar only and are not implicit defaults.
- No new skill, MCP, plugin, package, or external dependency was added; existing Hottop/GitHub/TDD capabilities were sufficient.

Strict TDD evidence for PR #23:

- runtime RED: Ruff passed; the existing **409 tests passed** and exactly **6 new tests failed** because `hottop.generation_preflight` did not yet exist;
- CLI RED: **415 tests passed** and exactly **2 new tests failed** because `generation-preflight` did not yet exist;
- durable-doctrine RED: **417 tests passed** and exactly **3 contract tests failed** because `PROJECT.md` and the two existing creative skills did not yet contain the mandatory rule;
- GREEN after implementation/doctrine: Python 3.11 and 3.12 passed Ruff + **420 tests**;
- live-current-news smoke was then added using a Reuters story observed on 2026-08-25, with publication timestamp intentionally left unknown because the exact time was not evidenced;
- PR merge-ref CI run `32831989190` passed on Python 3.11 and 3.12; Python 3.12 explicitly reports **421 passed** after the live fixture was added.

Archived live smoke input:

- `examples/preflight/live-smoke-2026-08-25.json`;
- promoted subject for this smoke: Hottop;
- selected hotspot: Reuters, `Waiting on Nvidia for next leg of AI rally`;
- selected treatment: financial-news/social-native editorial realism;
- selected format: single visual metaphor;
- this fixture proves a real live-research result can flow through the same runtime preflight used by synthetic unit cases without fabricating an unknown publication timestamp.

## Durable governance state

`PROJECT.md` is canonical and requires:

- repository-backed context recovery whenever a session is new, long, stale, or handed off;
- every new Hottop image/video generation request in Chat to re-read current repository doctrine/status/relevant skills/configs, then separately perform fresh public hotspot research;
- product, hotspot, visual style/medium, and output format to be per-request choices rather than historical defaults;
- mandatory `hottop.generation-preflight.v1` readiness before final asset generation;
- **existing-skill first** capability routing: reuse a suitable installed skill/MCP/plugin rather than duplicating it; add capabilities only for a concrete uncovered gap after permission/license/security/cost/reversibility review;
- targeted ecosystem freshness scans against measured project gaps, followed by real integration when a candidate clears the admission gate.

## Current ecosystem priorities

1. **Fresh creative truth before generation:** keep the generation preflight provider-neutral while improving live source diversity, evidence quality, hotspot ranking, and archive provenance.
2. **Cinematic generated-video proof:** benchmark the merged LightX2V/Wan2.2 operator route when local assets exist, comparing motion quality, identity continuity, reference adherence, artifact rejection and runtime cost against the deterministic baseline.
3. **Cross-shot identity / continuation:** prioritize measurable reference/continuation capability rather than generic single-shot demo quality.
4. **Mandarin dialogue quality:** benchmark Qwen3 CustomVoice and CosyVoice3 only when operator-provisioned local models are available. eSpeak remains the guaranteed fallback; voice cloning remains rights-gated.
5. **Production evidence over abstraction:** promoted routes must end in reproducible evidence, not merely another provider interface.
6. **License separation:** code repositories and model/weights licenses remain separate gates.

## Immediate next actions

1. Finish PR #23 exact-head/merge-ref verification and merge it once all repository gates remain green.
2. Re-fetch `main` after merge and verify the runtime gate, CLI, charter, skills, live smoke fixture, and status are actually deployed.
3. Continue the Production v0.2 reference-conditioned identity/continuation benchmark work without weakening the new fresh-generation gate.
4. When operator-owned GPU/model assets are available, run a real LightX2V/Wan2.2 cinematic benchmark through normal quality/provenance/composition gates; do not auto-download or trigger paid compute.
5. Continue targeted upstream scans and integrate only changes that materially improve a measured Hottop gap and clear source/license/cost/hardware/security/rollback gates.

## Durable motion contract

`fresh hotspot research → hottop.generation-preflight.v1 → hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg → final media verification`

Default unattended target remains zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never become paid credits or a hidden paid provider. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity remain hard gates.
