# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — real mechanism-driven generation smoke + image/video quality benchmark**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current main state

Current deployed creative/runtime chain:

`fresh/supplied hotspot analysis → hotspot mechanism mapping → product role/outcome change → hottop.generation-preflight.v1 → dynamic format/style selection → render route → voice/music/SFX → final quality/media verification`

The repository now enforces four complementary layers:

1. **Fresh-generation gate** — every new image/video request re-resolves product, hotspot, style and format; when no hotspot is supplied, run fresh live discovery; when the user supplies one, analyze that source first and freshly verify current/factual context as needed.
2. **Mechanism-first creative mapping** — extract recognition hook, causal/relationship mechanism, native visual grammar, native dialogue/language rhythm and native audio grammar; the product must take a functional role that changes the story outcome.
3. **No-template runtime** — the old keyword → fixed archetype → product-as-hero → automatic four-panel path is removed. Legacy four-panel briefing now requires explicit `ProductMechanismMapping`; batch discovery without mechanism analysis returns `mechanism_required_ids` instead of inventing a generic brief.
4. **Video quality routing** — direct video remains preferred when it meets the selected quality bar; when it does not, approved rights-safe keyframes may feed the existing reference-conditioned I2V path. Image-first is a recovery route, not a universal template, and the output must still contain meaningful motion, continuity and hotspot-native timing/audio.

## Deployed milestones

- PR #23 — mandatory fresh-hotspot generation preflight, merged as `ee801cb289f99baecd932a32b520e89fd0155aec`.
- PR #24 — canonical mechanism-first creative doctrine + optional image-first/reference-conditioned video quality recovery, merged as `8f1e24e2e8b89c0aa8a0608739e754fcf30b74f4`.
- PR #25 — runtime removal of the legacy keyword/archetype/template briefing behavior, merged as `39f601f5a4c5b22d73f9542d4b3f45a149f9386f`.

Supporting production baseline remains deployed:

- deterministic zero-cost software3d → audio → MoviePy → FFmpeg → verified MP4 path;
- software3d multi-story routing including cow/snake and Odyssey production cases;
- operator-managed LightX2V/Wan2.2 T2V/I2V route and reusable I2V profile;
- byte-bound shot provenance before composition;
- Qwen3-TTS benchmark-ready offline local adapter;
- role/subject/identity-lock reference continuity contract.

## Verification evidence

### PR #24

- RED contract head `47062886b4a0f4df2541d85bc4fa54844c49a16d` failed because the mechanism doctrine did not yet exist.
- Exact implementation head `4f806c412afd96784ef88ae2e26c438a7ccecc06` passed Ruff + full pytest on Python 3.11 and 3.12.
- Post-merge main CI run `32834370593` passed Python 3.11 and 3.12.

### PR #25

- RED head `66b114c3ff0b7662d8939a7dd824829ece563d89` failed pytest on Python 3.11 and 3.12 before the mechanism runtime existed.
- The first implementation run exposed four migration/test-fixture failures; workflow logs showed two were legitimate dedupe of identical test titles and two were stale render-v1 tests still calling `build_brief()` without a mechanism mapping. Those test contracts were corrected rather than weakening the runtime guard.
- Exact PR head `228cce83a1660ca6f5c9263ce394a1ec8801d47b` passed Ruff + full pytest on Python 3.11 and 3.12 in CI run `32835317473`.
- Post-merge main head `39f601f5a4c5b22d73f9542d4b3f45a149f9386f` passed Ruff + full pytest on Python 3.11 and 3.12 in CI run `32835457340`.

No new skill, MCP, plugin, package, paid service or duplicate video backend was introduced for PR #24/#25 because the existing Hottop creative skills, GitHub/TDD/debugging capabilities and reference-conditioned I2V architecture already covered the required surface.

## Current creative contract

For every new Hottop image/video task in Chat or production:

- recover current `PROJECT.md`, `STATUS.md` and relevant checked-in skills/configs;
- if the user supplies a hotspot, analyze its actual recognition mechanism and native visual/dialogue/audio grammar first;
- if no hotspot is supplied, perform a fresh live hotspot/news/culture/internet discovery pass;
- never inherit a previous product, cow/Odyssey character, four-panel format, 3D treatment, cinematic treatment or other historical example as an implicit default;
- make the product perform a real job inside the hotspot mechanism and change the outcome;
- reject `hot character + logo`, decorative hotspot skins and concepts that could advertise any brand unchanged;
- require fresh evidence and `hottop.generation-preflight.v1` readiness before final asset generation;
- for video, treat BGM, voice delivery, SFX/Foley, timing, subject continuity and meaningful motion as first-class quality gates;
- use image-first/reference-conditioned I2V only when it measurably improves a weak direct-video route; never downgrade the result into a slideshow.

## Current ecosystem priorities

1. **Real creative smoke:** exercise the mechanism runtime with a genuinely current hotspot and a real promoted product, not only synthetic test data.
2. **Hotspot-source quality:** improve freshness/source diversity/evidence quality only where it raises concept quality or reduces false trend selection.
3. **Video benchmark:** compare direct video with image-first reference-conditioned I2V on the same accepted creative when direct generation misses identity/style quality.
4. **Audio benchmark:** improve Mandarin voice quality and match BGM/SFX/voice delivery to the selected hotspot's native audio grammar; eSpeak remains a deterministic fallback, not the quality ceiling.
5. **Cross-shot identity/continuation:** promote routes only when they preserve subject identity and action/geography across shots with measurable evidence.
6. **Ecosystem radar:** continue targeted GitHub/open-source/news scans against measured gaps; integrate only candidates that clear source/license/weights-license/cost/hardware/security/reversibility/value gates.

## Immediate next actions

1. Run a **real fresh-hotspot + product mechanism creative smoke** through the newly deployed runtime and generation preflight.
2. Archive the selected hotspot evidence, mechanism mapping, product role/outcome change, style/format rationale and creative review result.
3. If motion is selected, compare direct video quality with the existing image-first reference-conditioned I2V route only when direct output misses the chosen quality bar; preserve voice/BGM/SFX and continuity gates.
4. Turn successful real production cases into reusable evidence/examples without making their product, hotspot, character, format or style the next request's default.
5. Continue targeted upstream scans and integrate only changes that materially improve a measured Hottop gap.

## Recovery order

When resuming after context pressure/new conversation:

1. Read `PROJECT.md`.
2. Read this `STATUS.md`.
3. Read the relevant checked-in skill(s), especially `brand-metaphor-creative` and `hottop-meme` for generation work.
4. Read the newest relevant config/spec/example/decision record.
5. Inspect current `main`, open PRs and exact-head CI.
6. Perform the targeted ecosystem scan relevant to the active production gap.
7. For a new image/video request, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously rather than asking for routine project decisions.
