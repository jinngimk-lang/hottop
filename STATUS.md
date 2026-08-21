# Hottop Status

Last updated: 2026-08-21 16:11 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Core trend pipeline is in place: DailyHotApi, NewsNow, RSS, dedupe/ranking, briefing, batch fan-in, source presets, enrichment fallback (Crawl4AI → Firecrawl → plain HTTP), doctor, renderer handoff and CLI commands.
- Promotion semantics are generalized beyond InkClawAgent/AI: brand, product, service, feature, campaign, person, idea, keyword or tool.
- `PromotionContext`, `ComparisonCandidate` and deterministic positioning/research-query planning are implemented; `hottop position` emits a structured research handoff.
- Comparison rules are evidence-aware: named competitors cannot be assigned invented defects; generic category/legacy/manual proxies are preferred when evidence is weak.
- `hottop position --comparisons <json>` ingests researched `ComparisonCandidate` records, normalizes unsupported `supported` posture back to `satire`, and emits `selected_comparison` using the deterministic selector. RED head `dc02ebd8bc86db56613e8cf2e1d000a33e363a60` failed CI run 305 because the option did not exist; implementation head `29f2093d8e39df39f37ef5acd7ae00a3f9bfbb8f` passed run 309 on Python 3.11/3.12.
- Public research handoff no longer requires callers to construct internal comparison records manually. `ComparisonResearchResult` + `adapt_comparison_research_results()` convert `research_results` entries into evidence-bearing `ComparisonCandidate` records with URL/source/timestamps/source quality/notes, and `hottop position --comparisons` accepts either `comparison_candidates` or `research_results`. Implementation head `ffe3b7d704cd49369e7b5c4304784bfc1bb0d448` passed CI run 337 on Python 3.11/3.12.
- Visual-medium routing is established for film/live action, animation, real-world/social, technology, food/consumer and internet-native formats.
- Creative doctrine is persisted in `PROJECT.md`, `skills/brand-metaphor-creative/SKILL.md`, `skills/creative-reference-research/SKILL.md`, and `skills/hottop-meme/SKILL.md`; context recovery must not collapse Hottop back into “four-panel AI memes.”
- Adaptive interaction doctrine is now persisted in both `PROJECT.md` and `skills/brand-metaphor-creative/SKILL.md`: resolve existing intent first, ask only high-impact questions within a 0–3 question budget, treat platform/style/creative ambition/product visibility/project shape as creative-routing inputs, and preserve the seven-part Creative Review as the hard gate. The stale-skill contract caused head `5873a31da80250a40f1e851850f79cbcfe9d20fa` / run 441 to fail; skill sync head `2fa733cbb39645354a24391cb3a28e251eb888aa` passed run 443 on Python 3.11/3.12.
- Structured creative contracts now exist in code: `CreativeStrategy` carries `category_default`, `deleted_constraint`, `new_competition_axis`, `bridge_type`, `bridge`, and `expression_form`; `CreativeConcept` carries flexible beats, medium, genre treatment, prompts, risks and claim status.
- Deterministic creative helpers are implemented: bridge scoring, expression-form selection, structured seven-part creative review, contextual review/ranking, best-review selection, and visual-medium routing.
- Provider-neutral flexible rendering is implemented via `CreativeRenderRequest` / schema `hottop.render.v2`; legacy `hottop.render.v1` four-panel handoff remains backward compatible.
- CLI command `hottop render-concept` validates a serialized `CreativeConcept` and emits `hottop.render.v2`; CI run 283 passed on Python 3.11/3.12 after the RED test exposed the missing command.
- `CreativePackageInput` / deterministic package selection existed but its CLI entrypoint was missing; run 327 exposed `test_package_concepts_selects_and_emits_render_v2` failing with exit code 2. `hottop package-concepts` is now wired to validate reviewed alternatives, choose a passing best concept and emit `hottop.creative-package.v1` with selected `hottop.render.v2`; repair head `83aecbaa3ae633fba5df1bd347a20beea03e14c9` passed run 329 on Python 3.11/3.12.
- Enrichment is now an explicit production handoff before creative strategy work. `hottop enrich-creative <trends.json> --index N` selects a normalized trend, runs the existing Crawl4AI → optional Firecrawl → plain-HTTP enrichment chain, and emits `hottop.creative-enrichment.v1` preserving the original candidate plus provider, source markdown and fallback failures. After the RED contract at `e4672fe360aaa222629ce8b1016317875fbac160` / run 447 exposed the missing enrichment entrypoint, implementation head `4db796ed896b76f6ed31aa65ae4f978742db700f` passed run 449 on Python 3.11/3.12.
- Flexible reviewed production is no longer single-item-only. `hottop creative-batch` accepts a non-empty set of existing `OrchestrationInput` records, reuses the established hard Creative Review + contextual ranking for each record, and emits `hottop.creative-batch.v1` with selected flexible `CreativeConcept` and `hottop.render.v2` results. Core does not invent creative-quality scores: reviewed candidate judgment remains upstream and the deterministic layer only validates/selects passing work. RED head `7828c5ab7e908260d3fe205bc3bc5f07a30bbae1` / run 451 failed only because the command did not exist; implementation head `db8332e7dbf3d98139a27288dfa55f4d7cf15e48` passed run 453 on Python 3.11/3.12.
- Provenance-first `VisualReference` and `hottop reference-plan` are implemented for grammar-only reference research using Playwright CLI planning without executing or persisting browser state.
- RSSHub external-feed pilot is implemented as an optional adapter that reuses the existing RSS parser. `BatchSourceConfig` and CLI discovery accept `rsshub`; operator must explicitly configure `RSSHUB_BASE_URL`; `hottop doctor` reports RSSHub configuration without making it a core dependency.
- RSSHub RED sequence verified expected failure modes (missing module / missing doctor state); exact-head CI run 301 passed on Python 3.11/3.12 after implementation.
- PR #1 metadata has been refreshed from the obsolete “four-panel meme brief pipeline” description to the current brand-creative-engine scope while remaining draft/mergeable.
- Added live archive `examples/runs/2026-08-21-1257-briefs.json` with three evidence-linked creative directions: robotics “ChatGPT moment” → do not wait for a universal breakthrough; BirdTok / craving for something real → signal over output volume; intrusive digital popovers → delete interface friction rather than design a prettier layer.
- Persistent project memory protocol is active: durable direction lives in the repository; context pressure triggers repository-based recovery; accepted direction changes update charter + relevant skill/spec + status.

## Current creative doctrine

- **Reframe before optimize:** find the category default, then ask whether the constraint should disappear instead of making a marginally better version of it.
- **Natural bridge before logo:** connect hotspot and product through shape/material, action, role, function, emotion/ritual or language/symbol.
- **Product role is flexible:** the promoted subject may be hero, prop, material, gesture, route, transformation, environment or final reveal.
- **Adaptive intake, not a static form:** infer what is already known and ask only unresolved high-impact questions; platform/style/ambition/product visibility/project shape change creative structure rather than only output formatting.
- **Format follows the idea:** single visual metaphor, swipe-reveal, four-panel, faux film still/poster, split old-vs-new or product-as-prop. Four panels are no longer the default requirement.
- **Medium follows the hotspot:** movie feels cinematic, animation feels animation-native, real/social feels documentary-native, consumer product can feel like polished commercial photography.
- **Competitor is optional; truth is mandatory:** the strongest antagonist may be a named rival, incumbent habit, manual workaround or the old category assumption itself.
- **Creative quality gate:** instant comprehension, natural linkage, product centrality, surprise, ownability, evidence safety and original execution; contextual fit ranks only concepts that already pass this gate.
- **Reference research is grammar-only:** preserve provenance, composition/reveal/medium lessons and `what_not_to_copy`; never turn third-party pixels into a generation target.
- **Project memory is part of product quality:** durable doctrine lives in the repository; context recovery reads it before continuing; new durable learning is audited and written back instead of living only in chat.

## Latest live evidence notes

- Reuters, 2026-08-20: robotics leaders are discussing a future “ChatGPT moment,” while broad practical capability is not yet here. Creative use: contrast waiting for a universal breakthrough with coordinating useful capabilities available today. Risk: never imply InkClawAgent controls robots or outperforms a named robotics company.
- The Guardian, 2026-08-15: younger audiences are showing renewed interest in birding/BirdTok amid a noisy online environment. Creative use: “one useful signal vs another noisy content source.” Risk: cultural observation only; do not turn it into a universal behavioral claim or copy TikTok UI/creators.
- The Guardian, 2026-08-18: humorous new vocabulary describes common digital irritants such as modal/popover layers obscuring desired content. Creative use: constraint deletion — do not build a prettier popover, question the need for the interface layer. Risk: use generic UI and do not imply bypass of required authentication/permissions.

## In progress

- Making batch-config `preset` affect collector/source-quality resolution rather than remaining descriptive configuration.
- Adding representative consumer-product / swipe-reveal production archives that exercise adaptive intent, enrichment, flexible orchestration, `CreativeConcept` and `hottop.render.v2` together.
- Continuing live trend research across entertainment, animation, technology, internet culture, social phenomena and consumer culture while Foundation v0.1 closes.

## Next actions

1. Make batch-config `preset` affect collector/source-quality resolution.
2. Add representative consumer-product and swipe-reveal archives that exercise `CreativeConcept` + `hottop.render.v2`, including category-default/deleted-constraint/new-axis fields and reference manifests where useful.
3. Exercise the RSSHub pilot against an explicitly configured operator-controlled instance; keep it optional and do not vendor RSSHub.
4. Inspect Foundation v0.1 diff/reviews and mark PR #1 ready once remaining production-path contracts are green.
5. After Foundation v0.1, add a lightweight project-bootstrap template/command so new long-running projects can create charter/status/skill recovery files consistently instead of relying on memory.

## Constraints

- No secrets/cookies/browser profiles in Git.
- No unsupported factual superiority claims.
- No invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI or distinctive competitor trade dress.
- Preserve broad cultural/medium recognition while building original staging and assets.
