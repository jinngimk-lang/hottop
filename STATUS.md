# Hottop Status

Last updated: 2026-08-23 10:56 +08:00
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
- Visual-reference exclusion safety is canonical: every `what_not_to_copy` item is stripped and blank/whitespace-only exclusions are rejected, so a manifest cannot satisfy the grammar-only safety boundary with empty durable instructions. Implementation head `d9a8255578f81b28e186cf5363b9074f70de59d3` passed exact-head CI run 671.
- RSSHub external-feed pilot is implemented as an optional RSS adapter. It requires explicit `RSSHUB_BASE_URL`; `hottop doctor` reports configuration and core operation does not depend on RSSHub.
- Batch-config `preset` is now functional rather than descriptive: `_discover_configured()` passes the selected preset into DailyHot, NewsNow, RSS and RSSHub collectors, and source-quality resolution uses it. The RED contract in `tests/test_batch_preset_routing.py` exposed the dropped value; subsequent exact-head CI is green.
- Representative project-shape Creative Package fixtures exist for consumer swipe-reveal, software category reframe and social-native meme output, all validating through `hottop.render.v2`.
- A deterministic pre-generation `CreativeDirective` contract now converts resolved intent + promotion semantics into generation guidance: three direction lanes, preferred forms, bridge biases, humor/joke mechanics, product-visibility instruction, platform instructions, precision requirements and reject patterns. It is exposed as `hottop creative-directive <input.json>`. This codifies existing doctrine rather than replacing the Creative Review or inventing quality scores.
- `CreativeDirective` treats humor as an actual routing intent rather than a universal default: `funny-meme` requires humor, and explicit/inferred `witty` or `breakout` can require humor, while a defaulted `witty` value does not force jokes into an explicitly `minimal-premium` direction.
- Added `examples/runs/consumer-swipe-reveal-production.json`, a synthetic/non-factual representative production archive that exercises intent → enrichment handoff → grammar-only `VisualReference` → `CreativeDirective` → reviewed orchestration → three-frame `swipe-reveal` → `hottop.render.v2`. It preserves category default, deleted constraint, new competition axis, sensory bridge, exclusions, risks and claim posture.
- Foundation closure review fixed the flexible production evidence boundary: `CreativeConcept` cannot declare `claim_status=supported` without attached `comparison_evidence`, `hottop.render.v2` preserves that evidence, and unresolved named comparisons are rejected unless evidence-backed or explicitly satire.
- Package/orchestration review identities are bound and canonical: option labels are nonblank, normalized, unique, and must match base/contextual review identities; contextual identities are canonicalized before durable results.
- Promotion identities are canonical and cross-bound: `PromotionContext.subject_name`/`category`, resolved `CreativeIntent.promotion_target`, package options and orchestration options cannot silently diverge across promoted subjects.
- Resolved promotion semantics are canonical when present: `PromotionContext.primary_job`, `primary_pain_point` and `primary_differentiator` strip surrounding whitespace and reject blank/whitespace-only values while preserving `None` for genuinely unresolved semantics. RED run 657 produced exactly the four targeted failures (4 failed / 207 passed); implementation head `435bb093b4bffacd1711d7cd39b2ae70c59e97c1` passed run 659 on Python 3.11/3.12.
- Bridge-candidate semantics are canonical before ranking: `BridgeCandidate.bridge` strips surrounding whitespace and rejects blank/whitespace-only bridge text, preventing empty bridge records from participating in deterministic scoring. Implementation head `4bd5a71387b89af530b9697badb1118c591c231e` passed exact-head CI run 655.
- Comparison identities are canonical: `ComparisonCandidate.name` and `CreativeConcept.comparison_target` strip surrounding whitespace and reject blank identities.
- Evidence provenance identity is canonical: `Evidence.source` strips surrounding whitespace and rejects blank/whitespace-only source identities. RED run 611 produced exactly the two targeted failures (2 failed / 181 passed); implementation head `ceb4c27ca23a476866dd4b79be47415008d5ddaf` passed exact-head CI run 613.
- Trend provenance identity is canonical: `TrendCandidate.source` strips surrounding whitespace and rejects blank/whitespace-only source identities, aligning raw trend records with downstream evidence/archive provenance. RED run 617 produced exactly the two targeted failures (2 failed / 183 passed); implementation head `288004a018a2f7b8888595162c387b9d452267fc` passed exact-head CI run 619.
- Creative strategy semantic text is canonical when present: `category_default`, `deleted_constraint`, `new_competition_axis` and `bridge` strip surrounding whitespace and reject blank/whitespace-only values while preserving `None` for genuinely absent reframing fields. RED run 647 produced exactly the targeted two failures (2 failed / 203 passed); implementation head `51f1e502b9b22e1a39cea5c3b9e03bc24c2b30fe` passed exact-head CI run 649 on Python 3.11/3.12.
- Optional `CreativeBeat.caption` text is canonical when present: captions strip surrounding whitespace and reject blank/whitespace-only values while preserving `None` for deliberately captionless beats. RED run 663 produced exactly the two targeted failures (2 failed / 211 passed); implementation head `647be99f90ead8ae1aa6964a5881438777ac4860` passed run 665 on Python 3.11/3.12.
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

- Foundation v0.1 closure review: continue inspecting the accumulated PR diff, tests and production-path contracts for contradictions, dead compatibility assumptions and missing evidence/safety/integrity edges after closing the render-v2 comparison-evidence, review-binding, identity canonicalization, unresolved named-comparison, cross-promotion, strategy-semantic-text, optional beat-caption and visual-reference-exclusion gaps.
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
