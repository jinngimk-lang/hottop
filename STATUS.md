# Hottop Status

Last updated: 2026-08-21 13:05 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Core trend pipeline is in place: DailyHotApi, NewsNow, RSS, dedupe/ranking, briefing, batch fan-in, source presets, enrichment fallback (Crawl4AI → Firecrawl → plain HTTP), doctor, renderer handoff and CLI commands.
- Promotion semantics are generalized beyond InkClawAgent/AI: brand, product, service, feature, campaign, person, idea, keyword or tool.
- `PromotionContext`, `ComparisonCandidate` and deterministic positioning/research-query planning are implemented; `hottop position` emits a structured research handoff.
- Comparison rules are evidence-aware: named competitors cannot be assigned invented defects; generic category/legacy/manual proxies are preferred when evidence is weak.
- Visual-medium routing is established for film/live action, animation, real-world/social, technology, food/consumer and internet-native formats.
- **Creative direction audit completed from the working conversation and supplied visual-ad examples.** `PROJECT.md` persists the broader doctrine so context recovery does not collapse the project back into “four-panel AI memes.”
- Added `skills/brand-metaphor-creative/SKILL.md`, covering category defaults, constraint deletion, bridge search, format selection, competitor truthfulness and a creative review gate.
- Refactored `skills/hottop-meme/SKILL.md` to be hotspot/evidence/four-panel specific and to route creative strategy through `brand-metaphor-creative`.
- Added `tests/test_creative_skill_contract.py`. RED run 195 failed on the missing doctrine/skill as intended; implementation head `97a81e161768633b2c209ab215e58627ea460247` passed CI run 201 on Python 3.11/3.12.
- Documentation/status head `fcf96d05d839a482113eae053f7f6dbf4b72b1d6` passed CI run 203.
- Added live archive `examples/runs/2026-08-21-1257-briefs.json` with three evidence-linked creative directions: robotics “ChatGPT moment” → do not wait for a universal breakthrough; BirdTok / craving for something real → signal over output volume; intrusive digital popovers → delete interface friction rather than design a prettier layer.
- Added a **persistent project memory protocol** to `PROJECT.md` and `skills/brand-metaphor-creative/SKILL.md`: new multi-session projects create a living project charter; context pressure triggers repository-based recovery; durable direction changes update the charter + skill/spec + status; a compact decision log preserves rationale without turning the charter into a transcript.
- Extended the creative skill to explore pain-point contrast, bridge-led metaphor and constraint-deletion directions before locking the first obvious idea.
- Persistence contract commit `0b5de6cb9f1612573e105570a4dfe904ba006925` failed CI run 209 as expected before the new protocol existed. Implementation head `bd2aca2d086ad4bb6d12d15b43d9c9046811ff53` passed CI run 213 on Python 3.11/3.12.

## Current creative doctrine

- **Reframe before optimize:** find the category default, then ask whether the constraint should disappear instead of making a marginally better version of it.
- **Natural bridge before logo:** connect hotspot and product through shape/material, action, role, function, emotion/ritual or language/symbol.
- **Product role is flexible:** the promoted subject may be hero, prop, material, gesture, route, transformation, environment or final reveal.
- **Format follows the idea:** single visual metaphor, swipe-reveal, four-panel, faux film still/poster, split old-vs-new or product-as-prop. Four panels are no longer the default requirement.
- **Medium follows the hotspot:** movie feels cinematic, animation feels animation-native, real/social feels documentary-native, consumer product can feel like polished commercial photography.
- **Competitor is optional; truth is mandatory:** the strongest antagonist may be a named rival, incumbent habit, manual workaround or the old category assumption itself.
- **Creative quality gate:** instant comprehension, natural linkage, product centrality, surprise, ownability, evidence safety and original execution.
- **Project memory is part of product quality:** durable doctrine lives in the repository; context recovery reads it before continuing; new durable learning is audited and written back instead of living only in chat.

## Latest live evidence notes

- Reuters, 2026-08-20: robotics leaders are discussing a future “ChatGPT moment,” while broad practical capability is not yet here. Creative use: contrast waiting for a universal breakthrough with coordinating useful capabilities available today. Risk: never imply InkClawAgent controls robots or outperforms a named robotics company.
- The Guardian, 2026-08-15: younger audiences are showing renewed interest in birding/BirdTok amid a noisy online environment. Creative use: “one useful signal vs another noisy content source.” Risk: cultural observation only; do not turn it into a universal behavioral claim or copy TikTok UI/creators.
- The Guardian, 2026-08-18: humorous new vocabulary describes common digital irritants such as modal/popover layers obscuring desired content. Creative use: constraint deletion — do not build a prettier popover, question the need for the interface layer. Risk: use generic UI and do not imply bypass of required authentication/permissions.

## In progress

- Turning `hottop position` search plans into evidence-backed `ComparisonCandidate` records from public web / Agent-Reach results.
- Extending structured schemas/renderer handoff for the new creative doctrine instead of leaving it only in documentation.
- Continuing live trend research while Foundation v0.1 closes.

## Next actions

1. Confirm CI on the newest status head; repair immediately if red.
2. Add structured creative fields: `category_default`, `deleted_constraint`, `new_competition_axis`, `bridge_type`, `bridge`, and `expression_form`.
3. Add an expression-form selector that can choose `single-visual-metaphor`, `swipe-reveal`, `four-panel`, `faux-film-still`, `split-old-vs-new`, or `product-as-prop` instead of hard-coding four panels.
4. Add a bridge generator/scorer for shape/material, action, role, function, emotion/ritual and language/symbol links.
5. Connect researched comparison evidence to deterministic target selection and briefing.
6. Make batch-config `preset` affect collector/source-quality resolution.
7. Add enrichment-before-brief CLI path and promote `visual_medium` / `genre_treatment` into first-class renderer fields.
8. Add representative archives for consumer products and swipe-reveal advertising, not only software/four-panel cases.
9. After Foundation v0.1, add a lightweight project-bootstrap template/command so new long-running projects can create charter/status/skill recovery files consistently instead of relying on memory.
10. Inspect Foundation v0.1 diff/reviews and mark PR #1 ready once remaining contracts are green.

## Constraints

- No secrets/cookies/browser profiles in Git.
- No unsupported factual superiority claims.
- No invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI or distinctive competitor trade dress.
- Preserve broad cultural/medium recognition while building original staging and assets.
