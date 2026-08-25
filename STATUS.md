# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — mechanism-first hotspot creative + reference-conditioned video quality proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Hottop now has four complementary production layers:

1. a **mandatory fresh-generation entry gate** for every new image/video request;
2. a **mechanism-first hotspot creative doctrine** that analyzes the hotspot's causal/relationship, visual, language and audio grammar before product insertion;
3. a guaranteed **zero-cost deterministic software3d → audio → MoviePy → FFmpeg → verified MP4** baseline; and
4. isolated operator-owned/open reference-conditioned generation routes that can be benchmarked without changing the provider-neutral creative/runtime contract.

Closed production evidence:

- PR #12 established the reproducible software3d config-to-MP4 loop with byte-bound provenance manifests and final media verification.
- PR #15 generalized software3d story routing beyond the cow/snake flagship and added the Odyssey witch/pigs cinematic profile; it was squash-merged as `01e54432978f9694ea79a645e8b53308c474f3d5`.
- PR #13 added the benchmark-ready offline local Qwen3-TTS 0.6B CustomVoice adapter and was merged as `b9743763316f240d5c095c84bc5f2f071ee32716`.
- PR #14 added the first-class operator-managed LightX2V/Wan2.2 T2V/I2V backend and was merged as `e32a0632d1245752baa0b60cd464a18af110a8df`.
- `8410458fd9cbc416f0cb98fa39001f685f6feb7c` added the reusable checked-in LightX2V/Wan2.2 I2V operator profile and registry boundary.
- `859f2c382119facf96b3c6147e0b85fff979f514` bound accepted LightX2V shot bytes to artifact provenance and re-verification before composition.
- PR #23 deployed the mandatory fresh-hotspot generation preflight to `main` as `ee801cb289f99baecd932a32b520e89fd0155aec`.

## Fresh-generation preflight deployment

PR #23 (`feat/fresh-hotspot-generation-preflight`) is merged and implements the hard requirement that **every new image/video generation request starts from newly researched current hotspot evidence and a new product/hotspot/style/format decision** rather than inheriting an old example.

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

Closed TDD/CI evidence for PR #23:

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

## Active PR #24 — mechanism-first creative + image-first quality recovery

Branch: `feat/hotspot-mechanism-image-first-quality`

This work deliberately **extends existing capabilities instead of duplicating them**:

- user-supplied hotspot → analyze that source first, then verify current/factual context as needed;
- no supplied hotspot → perform fresh discovery for the current request;
- extract recognition hook, **causal/relationship mechanism**, native visual grammar, native dialogue/language rhythm, and native audio grammar;
- place the product in a functional role inside the mechanism and require it to **change the story outcome** rather than decorate the hotspot skin;
- require retained hotspot elements to have jobs in the causal chain;
- prefer audience decoding `hotspot recognition → mapping → product consequence → punchline`;
- use **Image-first quality recovery** only when direct video misses the selected visual/identity/style bar: approve rights-safe keyframes first, then reuse the repository's existing reference-conditioned I2V path;
- image-first is not a new backend and not a universal template; successful video still requires meaningful motion, continuity, native timing, BGM/voice/SFX quality, artifact integrity and final media verification;
- no new skill/MCP/plugin/package/backend is being introduced because existing `brand-metaphor-creative`, `hottop-meme`, TDD and reference-conditioned I2V infrastructure already cover the required execution surface.

Strict TDD evidence so far:

- RED contract commit: `47062886b4a0f4df2541d85bc4fa54844c49a16d`;
- PR #24 was opened as draft with only the new contract test;
- CI run `32833835372` showed Ruff success and Python **3.11 pytest failure** on the RED test-only head, confirming the new doctrine was genuinely absent before implementation; Python 3.12 was also running the same pytest contract at that checkpoint;
- implementation commits then updated the canonical `PROJECT.md`, `skills/brand-metaphor-creative/SKILL.md`, and `skills/hottop-meme/SKILL.md` rather than adding a parallel skill or duplicate video route;
- exact-head GREEN verification is the next gate before merge.

## Durable governance state

`PROJECT.md` is canonical and requires:

- repository-backed context recovery whenever a session is new, long, stale, or handed off;
- every new Hottop image/video generation request in Chat to re-read current repository doctrine/status/relevant skills/configs;
- if the user supplies the hotspot, analyze its mechanism first; if not, discover fresh current candidates first;
- product, hotspot, visual style/medium, output format, dialogue/audio grammar and mechanism mapping to be per-request choices rather than historical defaults;
- the product to take a functional role that changes the hotspot story outcome;
- mandatory `hottop.generation-preflight.v1` readiness before final asset generation;
- **existing-skill first** capability routing: reuse a suitable installed skill/MCP/plugin rather than duplicating it; add capabilities only for a concrete uncovered gap after permission/license/security/cost/reversibility review;
- targeted ecosystem freshness scans against measured project gaps, followed by real integration when a candidate clears the admission gate.

## Current ecosystem priorities

1. **Fresh creative truth + mechanism quality:** improve live source diversity/evidence quality while measuring whether the selected hotspot mechanism creates a natural, product-specific joke rather than a surface reference.
2. **Cinematic generated-video proof:** benchmark the merged LightX2V/Wan2.2 operator route when local assets exist, comparing direct video with approved image-first reference-conditioned recovery when appropriate.
3. **Cross-shot identity / continuation:** prioritize measurable reference/continuation capability rather than generic single-shot demo quality.
4. **Mandarin dialogue/audio quality:** benchmark Qwen3 CustomVoice and CosyVoice3 only when operator-provisioned local models are available; match voice/BGM/SFX to hotspot-native grammar. eSpeak remains the guaranteed fallback, not the quality ceiling.
5. **Production evidence over abstraction:** promoted routes must end in reproducible evidence, not merely another provider interface.
6. **License separation:** code repositories and model/weights licenses remain separate gates.

## Immediate next actions

1. Finish PR #24 exact-head Python 3.11/3.12 CI verification and keep the contract GREEN.
2. Review the PR diff for accidental doctrine loss/duplication, then merge when gates are satisfied.
3. Re-fetch `main` after merge and verify `PROJECT.md`, both creative skills, contract tests and status are actually deployed.
4. Continue Production v0.2 with a real hotspot/product generation smoke that exercises mechanism mapping; for motion, compare direct video against image-first reference-conditioned I2V only when direct output misses the quality bar.
5. Continue targeted upstream scans and integrate only changes that materially improve a measured Hottop gap and clear source/license/cost/hardware/security/rollback gates.

## Durable motion contract

`fresh/supplied hotspot analysis → mechanism mapping → product role/outcome change → hottop.generation-preflight.v1 → hottop.render.v2 → route(direct video | image-first reference-conditioned I2V when justified) → hottop.video-plan.v1 → generation → voice/music/SFX → MoviePy → FFmpeg → final media verification`

Default unattended target remains zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never become paid credits or a hidden paid provider. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity remain hard gates.
