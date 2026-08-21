# Hottop Status

Last updated: 2026-08-22 02:05 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Core trend pipeline is in place: DailyHotApi, NewsNow, RSS, dedupe/ranking, briefing, batch fan-in, source presets, enrichment fallback (Crawl4AI → Firecrawl → plain HTTP), doctor, renderer handoff and CLI commands.
- Promotion semantics are generalized beyond InkClawAgent/AI: brand, product, service, feature, campaign, person, idea, keyword or tool.
- Evidence-aware positioning/comparison handoff is implemented. `hottop position --comparisons` accepts internal `ComparisonCandidate` records or public `research_results`; unsupported `supported` claims are normalized back to satire and named competitor negatives require evidence.
- Adaptive interaction is implemented with `CreativeIntent`, provenance/confidence, 0–3 high-impact questions, platform/style/ambition/product-visibility routing and project-shape profiles.
- Structured creative contracts are implemented: `CreativeStrategy` preserves `category_default`, `deleted_constraint`, `new_competition_axis`, bridge type/bridge and expression form; `CreativeConcept` preserves flexible beats, medium, genre treatment, prompts, risks and claim status.
- Deterministic bridge scoring, expression-form selection, hotspot-medium routing, seven-part Creative Review, contextual review/ranking and orchestration are implemented. Contextual scores may rank passing work but never bypass the base creative gate.
- Provider-neutral flexible rendering is implemented via `hottop.render.v2`; legacy four-panel `hottop.render.v1` remains backward compatible. `hottop render-concept`, `hottop package-concepts`, `hottop orchestrate` and `hottop creative-batch` are wired.
- Enrichment is an explicit production handoff through `hottop enrich-creative`, preserving the selected candidate, source markdown/provider and fallback failures before creative work.
- Provenance-first `VisualReference` and `hottop reference-plan` are implemented for grammar-only reference research with Playwright CLI planning, analysis-only defaults and explicit `what_not_to_copy`.
- RSSHub external-feed pilot is implemented as an optional RSS adapter. It requires explicit `RSSHUB_BASE_URL`; `hottop doctor` reports configuration and core operation does not depend on RSSHub.
- Batch-config `preset` is now functional rather than descriptive: `_discover_configured()` passes the selected preset into DailyHot, NewsNow, RSS and RSSHub collectors, and source-quality resolution uses it. The RED contract in `tests/test_batch_preset_routing.py` exposed the dropped value; subsequent exact-head CI is green.
- Representative project-shape Creative Package fixtures exist for consumer swipe-reveal, software category reframe and social-native meme output, all validating through `hottop.render.v2`.
- A deterministic pre-generation `CreativeDirective` contract now converts resolved intent + promotion semantics into generation guidance: three direction lanes, preferred forms, bridge biases, humor/joke mechanics, product-visibility instruction, platform instructions, precision requirements and reject patterns. It is exposed as `hottop creative-directive <input.json>`. This codifies existing doctrine rather than replacing the Creative Review or inventing quality scores.
- `CreativeDirective` treats humor as an actual routing intent rather than a universal default: `funny-meme` requires humor, and explicit/inferred `witty` or `breakout` can require humor, while a defaulted `witty` value does not force jokes into an explicitly `minimal-premium` direction.
- Added `examples/runs/consumer-swipe-reveal-production.json`, a synthetic/non-factual representative production archive that exercises intent → enrichment handoff → grammar-only `VisualReference` → `CreativeDirective` → reviewed orchestration → three-frame `swipe-reveal` → `hottop.render.v2`. It preserves category default, deleted constraint, new competition axis, sensory bridge, exclusions, risks and claim posture.
- The consumer production archive contract was introduced RED-first (`FileNotFoundError` in run 481) and implemented afterward. Follow-on RED contracts exposed the missing `creative-directive` CLI and the default-witty humor leak; current implementation head `60a48668b75391161b52d8ce121dae6fc4a3d00d` passed CI run 499 on Python 3.11 and 3.12.
- Foundation closure review found and fixed a final evidence/safety gap in the flexible production contract: `CreativeConcept` can no longer declare `claim_status=supported` without attached `comparison_evidence`, and `hottop.render.v2` preserves that evidence provenance. RED run 507 produced the expected two failures; implementation head `899ca5b2d9c37298619616d4d4291398e11e6e85` passed CI run 511 on Python 3.11 and 3.12.
- Foundation closure review also found an integrity gap in external creative scoring: a high-scoring `CreativeReview` could be paired with a different option because package/orchestration contracts did not bind the review identity to the concept option. `CreativePackageOption` and `OrchestrationOption` now require a nonblank label and `review.name == option.label`, preventing cross-option review reuse. The first implementation run 521 correctly exposed a test-boundary mistake; corrected head `80ff4e464c7f8eefb42cf087b29e9beec9469988` passed CI run 523.
- A follow-on closure check found that the preceding “nonblank label” contract still accepted whitespace-only identities because Pydantic `min_length=1` counts spaces. RED run 527 reproduced the bypass with `label="   "` and matching review name. Package and orchestration option labels now strip whitespace and reject empty results before review binding; implementation head `151d004dd810c24374a88f8d8d43e47a5866eeb3` passed CI run 531 on Python 3.11 and 3.12.
- Closure review found another evidence/safety bypass in the flexible production boundary: a concept could name a competitor while remaining `claim_status=needs_evidence`, then still be packaged/orchestrated/rendered if an external review scored it highly. `CreativeConcept` now rejects unresolved named comparisons unless the claim is evidence-backed (`supported` with attached evidence) or explicitly `satire`. RED run 535 reproduced the bypass; implementation head `4ec220aeb15c1e5dba1e9d28c111d660ffebe017` passed CI run 537 on Python 3.11 and 3.12.
- Closure review found a cross-promotion integrity gap in orchestration: top-level `promotion_context` and candidate `CreativeConcept.promotion` could disagree, allowing a reviewed concept for a different product to be selected while the result advertised another canonical context. RED run 541 reproduced the issue as the only failure (1 failed, 167 passed). `OrchestrationInput` now requires every option concept's promotion context to exactly match the orchestration-level promotion context; implementation head `86e1e326345caebbc6079fda0e6ab3c3adc652e3` passed CI run 543 on Python 3.11 and 3.12.
- A follow-on orchestration integrity review found that `CreativeIntent.promotion_target` could still point at a different promoted subject than the canonical `promotion_context`, allowing one result to preserve user intent for Product A while selecting/rendering Product B. After correcting the RED fixture to isolate that edge, CI run 549 failed exactly because the mismatched intent target was not rejected (1 failed, 168 passed). `OrchestrationInput` now binds a resolved intent promotion target to `promotion_context.subject_name`; implementation head `52d22deb2cd1fd9725dfeb2be41eafc1d0b6ed59` passed CI run 551 on Python 3.11 and 3.12.
- Closure review then found that option labels were bound to review names but not required to be unique within a package/orchestration payload, leaving selection and alternate identities ambiguous. `CreativePackageInput` and `OrchestrationInput` now reject duplicate normalized labels. The initial implementation head `9f4077de95df32ec35ba9e0ed5bc005b96849d78` reached CI run 559 but Ruff stopped on an import-formatting error before pytest; formatting-only follow-up `1e67bbb841747aae17d71a6d25451dbcbca17ef7` passed run 561 on Python 3.11 and 3.12.
- Added live archive `examples/runs/2026-08-21-1257-briefs.json` with evidence-linked robotics, BirdTok and digital-popover creative directions while keeping factual/safety caveats explicit.
- Persistent project memory protocol is active: `PROJECT.md` is durable direction, `STATUS.md` is the execution snapshot, reusable skills carry operational doctrine, and repository truth is reread under context pressure.

## Current creative doctrine

- **Reframe before optimize:** identify the category default, test deleting the constraint, then derive the new competition axis.
- **Natural bridge before logo:** search shape/material, action/motion, role, function, emotion/ritual and language/symbol links.
- **Product role is flexible:** the promoted subject may be hero, prop, material, gesture, route, transformation, environment or reveal.
- **Adaptive intake, not a static form:** infer known intent, ask only high-impact unresolved questions and let platform/style/ambition/product visibility/project shape change creative structure.
- **Format follows the idea:** single visual metaphor, swipe-reveal, four-panel, faux film still/poster, split old-vs-new or product-as-prop.
- **Medium follows the hotspot:** source-medium grammar and recognition cues matter; protected production assets do not become generation targets.
- **Competitor is optional; truth is mandatory:** use evidence-backed named comparisons, generic proxies, satire/metaphor or the old assumption itself as antagonist.
- **Creative quality gate stays hard:** instant comprehension, natural linkage, product centrality, surprise, ownability, evidence safety and original execution.
- **Reference research is grammar-only:** retain provenance, composition/reveal/medium lessons and `what_not_to_copy`; never use third-party pixels as a reproduction target.

## Latest live evidence notes

- Reuters, 2026-08-20: robotics leaders discussed a future “ChatGPT moment,” while broad practical capability is not yet here. Creative use: waiting for a universal breakthrough vs coordinating useful capability today. Do not imply control of robots or unsupported superiority over a robotics company.
- The Guardian, 2026-08-15: younger audiences showed renewed interest in birding/BirdTok amid a noisy online environment. Creative use: useful signal vs another noisy feed. Treat as cultural observation; do not copy TikTok UI or creators.
- The Guardian, 2026-08-18: humorous vocabulary for intrusive digital layers provides a constraint-deletion cue: question the need for the interface layer instead of designing a prettier obstruction. Use generic UI and never imply bypass of required permissions/authentication.

## In progress

- Foundation v0.1 closure review: continue inspecting the accumulated PR diff, tests and production-path contracts for contradictions, dead compatibility assumptions and missing evidence/safety/integrity edges after closing the render-v2 comparison-evidence, review-binding, whitespace-identity, unresolved named-comparison, cross-promotion concept/context, intent/promotion-context and duplicate-option-identity gaps.
- Continue fresh trend research across entertainment, animation, technology, internet culture, social phenomena and consumer culture without collapsing discovery into AI/tech only.
- RSSHub remains an optional pilot awaiting an explicitly configured operator-controlled instance; no credential or external-service setup is performed autonomously.

## Next actions

1. Continue PR #1 / Foundation v0.1 diff review for concrete regressions or contract gaps; use targeted RED → GREEN cycles only where the review finds a real issue.
2. Exercise the RSSHub pilot only when an operator-controlled `RSSHUB_BASE_URL` is explicitly available; otherwise keep the adapter optional and skip live-instance claims.
3. Refresh PR #1 completion text and mark ready only after the remaining Foundation review criteria are actually satisfied and exact-head CI stays green.
4. Keep producing fresh cross-category trend/evidence archives when they materially improve creative coverage.
5. After Foundation v0.1, add a lightweight project-bootstrap template/command so long-running projects can create charter/status/skill recovery files consistently.

## Constraints

- No secrets/cookies/browser profiles in Git or CI logs.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress or copied advertising layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
