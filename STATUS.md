# Hottop Status

Last updated: 2026-08-24 11:15 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1
PR: #1 — open, draft, mergeable

## Current foundation state

- Hottop is a cross-category brand creative engine, not InkClawAgent-only, AI-only or four-panel-only. `PROJECT.md` and the reusable skills are canonical for doctrine.
- Core trend discovery, enrichment, dedupe/ranking, source presets, optional RSSHub, evidence-aware comparison handoff, adaptive intake, project/platform routing, category reframing, bridge scoring, expression-form routing, Creative Review/contextual review, orchestration and provider-neutral rendering are implemented.
- Flexible `CreativeConcept` + `hottop.render.v2` is the primary production contract; legacy four-panel `hottop.render.v1` remains backward compatible.
- Provenance-first `VisualReference` + `reference-plan` are implemented with grammar-only research, analysis-only defaults, explicit `what_not_to_copy`, and no pixel-level reproduction target.
- Representative archives include a consumer swipe-reveal production path and cross-category live evidence runs.
- Foundation closure review has hardened durable identities, comparison/evidence safety, review binding, cross-promotion integrity, render text, strategy text, trend/product/comparison semantics, visual-reference provenance/exclusions, risk metadata, and distribution metadata through targeted RED → GREEN contracts.

## Distribution doctrine closure

- Durable doctrine is now **ad-light and motion-aware** for hotspot/meme/brand-memory work: omit in-asset URL/QR/hard CTA by default; conversion briefs may explicitly retain a destination; use motion when timing/action/dialogue/sound carries the idea; preserve scene/character/action continuity rather than slideshow-like hard cuts; show benefits first as consequences of the scene.
- This rule is persisted in `PROJECT.md` and `skills/brand-metaphor-creative/SKILL.md` and supersedes the older habit of automatically adding a URL CTA or forcing a dynamic hotspot into a static poster.
- `examples/runs/2026-08-24-inkclaw-aura-farming.json` was corrected from a static 4:5 URL-CTA poster into a 9:16 continuous-motion social-short treatment with dialogue, sound design, action continuity and no in-asset destination.
- Guided intake preserves static-vs-motion intent without adding a routine question: `CreativeIntent.distribution_mode` is `auto | static | motion`.
- `CreativeDirective` serializes `distribution_mode`, `in_asset_cta_policy`, and `motion_continuity_required`, adding anti-slideshow, continuity, no-URL/QR and benefits-as-consequences instructions where appropriate.
- RED head `5512d946a0bc5df7f1e901846f2c111bf6fe668a` failed CI run 733 with exactly the two missing distribution-intent/directive tests; GREEN directive head `0f0d4311e14efbfb8f16b673f5eae7824d0b5503` passed run 737. Status head `0832c330fd6cc1750ce73fd244f4c67d47b7883d` passed run 739.
- `CreativeConcept` and `CreativeRenderRequest` carry the same three distribution fields with backward-compatible defaults, and `build_creative_render_request()` preserves them into `hottop.render.v2`.
- RED head `5cd4fb0828e8fd449e0bf6a271176a61cc8ec995` failed exact-head CI run 741 with exactly two targeted render-handoff failures (`2 failed / 254 passed`, Ruff green). GREEN implementation head `79d787660cfd93b1d2617c7aec3145d46f0417db` passed exact-head CI run 745. Status head `b578ec372ce6ddb7ca5c13d158d5c2ddd4f6bb8b` passed run 747.
- Orchestration now applies the resolved distribution directive to the selected concept before building `hottop.render.v2`, closing the gap where options created before/without directive metadata defaulted back to `auto` / no-destination. Explicit concept motion metadata is retained when intent remains `auto`; resolved intent wins when it specifies static or motion, and CTA policy is derived from the same deterministic directive.
- RED head `e19ef41ae9477d9df61af03b3d321b6ff6be4220` failed exact-head CI run 749 with exactly two targeted orchestration propagation failures (`2 failed / 256 passed`, Ruff green). GREEN orchestration head `deb4675f0425dcf6c60c360a2bcf50d3bdc134d2` passed exact-head CI run 751.

## Current creative doctrine

- Reframe before optimize: identify `category_default`, test constraint deletion, derive `new_competition_axis`.
- Natural bridge before logo: search shape/material, action/motion, role, function, emotion/ritual and language/symbol.
- Product role is flexible: hero, prop, material, gesture, route, transformation, environment or reveal.
- Adaptive intake, not a static questionnaire: ask only high-impact unresolved questions.
- Format follows the idea; medium follows the hotspot.
- Distribution stays native: motion-native jokes stay motion-native; hotspot/meme/brand-memory assets remain ad-light unless conversion intent overrides.
- Named competitor negatives require evidence or unmistakable satire; otherwise use a generic proxy or the old assumption itself.
- Creative Review remains a hard gate: instant comprehension, natural linkage, product centrality, surprise, ownability, evidence safety, original execution.
- Visual-reference research is grammar-only with provenance and explicit exclusions.

## In progress

- Foundation v0.1 accumulated PR diff / production-contract closure review continues. Distribution now survives intent → directive → orchestration-selected concept → `hottop.render.v2`; do not create a parallel video renderer unless a concrete backend gap appears later.
- Continue checking for concrete regressions, dead compatibility assumptions, evidence/safety/integrity edges and missing deterministic handoffs. Use targeted RED → GREEN only for reproducible gaps.
- Continue fresh cross-category trend/evidence research when it materially improves creative coverage; do not collapse discovery into AI/tech only.
- RSSHub remains an optional pilot until an operator-controlled `RSSHUB_BASE_URL` is explicitly available.

## Next actions

1. Continue PR #1 / Foundation v0.1 accumulated diff and production-contract closure review from exact-head CI run 751; repair CI first if a future head fails.
2. Inspect package-only paths and revision flows for any remaining way to bypass or silently discard the selected distribution policy; only add a contract if a reproducible drop exists.
3. Refresh PR #1 completion text and mark ready only after remaining Foundation review criteria are satisfied and exact-head CI remains green.
4. Exercise the RSSHub pilot only with an explicitly configured operator-controlled instance.
5. Keep producing fresh cross-category evidence/creative archives when useful.
6. After Foundation v0.1, add a lightweight project-bootstrap template/command for charter/status/skill recovery files.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
