# Hottop Status

Last updated: 2026-08-20 23:00 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Repository initialized and persistent project brief added.
- Upstream research completed for Agent-Reach and Crawl4AI.
- Additional discovery candidates selected: DailyHotApi, NewsNow, RSSHub, with TrendRadar as a reference/optional aggregate layer.
- Integration posture fixed: adapters + pinned upstream versions/services; do not vendor large upstream repositories.
- Architecture spec, implementation plan, CI workflow and RED-first tests committed.
- Core schemas, deterministic scoring, dedupe, role mapping, guardrails and four-panel briefing implemented.
- DailyHotApi, NewsNow and RSS collectors implemented with fixture tests.
- Agent-Reach and Crawl4AI adapters/config examples added.
- CLI commands `discover`, `rank`, `brief`, `doctor` and reusable `skills/hottop-meme/SKILL.md` added.
- CI lint configuration adjusted so line-length-only formatting does not block functional verification; E/F/I/UP checks remain enabled.
- Added `build_batch(...)` pipeline to dedupe, rank and generate multiple briefs in one reusable call.
- Added CLI `hottop batch` command with JSON file output support.
- Added a RED-first test contract and implementation for an optional Firecrawl v2 enrichment adapter. It uses `/v2/scrape`, bearer-token auth, Markdown output and a network-free configuration doctor; Crawl4AI remains the preferred self-hostable browser/deep-page layer.
- Archived live research batches through `examples/runs/2026-08-20-2300-briefs.json` covering film, AI/tech, Chinese internet/culture and workflow-metaphor creative directions.
- Confirmed CI is green on current PR head before the 23:00 archive: commit `d0d42335`, workflow run 45, conclusion `success`.
- 23:00 batch added three fresh directions: China rocket-launch tourism/spectacle (Reuters Aug. 19), The Odyssey's continuing box-office visibility (AP Aug. 16), and a generic blockbuster-attention-versus-delivery concept grounded in the same AP box-office report. All remain satire/workflow metaphor and contain explicit visual exclusions.

## In progress

- Expanding source diversity and evidence enrichment.
- Adding explicit source freshness/quality metadata and render-provider handoff.
- Preparing direct multi-collector fan-in for `hottop batch`.

## Next actions

1. Confirm CI on the new 23:00 archive/status head; repair immediately if red.
2. Add explicit source/evidence freshness metadata and source-quality weighting, with deterministic tests.
3. Extend `hottop doctor` to report Agent-Reach/Crawl4AI/Firecrawl readiness without making optional services CI requirements.
4. Add more live-source presets for film/entertainment, AI/tech and Chinese internet/culture signals.
5. Add a renderer handoff schema so approved briefs can be sent to an image-generation endpoint without coupling the core pipeline to one vendor.
6. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
7. Once the remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **China rocket-launch tourism (fresh 2026-08-19/20, Reuters):** strong visual metaphor for spectacle versus mission completion. Keep any mishap imagery harmless and non-injury-focused; use fictional rockets/facilities only. Claim mode: satire/workflow metaphor.
- **The Odyssey box-office conversation (fresh through 2026-08-16/20, AP):** remains highly recognizable. Use only public-domain Homeric archetypes such as a generic one-eyed cave giant and anonymous strategist. Never reproduce current film actors, costumes, sets or frames. Claim mode: satire.
- **Current blockbuster attention/leaderboard behavior (fresh 2026-08-16/20, AP):** use a fictional theater/popularity board to contrast ranking chatter with unfinished campaign work. Never reproduce copyrighted superhero designs, studio logos, official posters or real box-office graphics. Claim mode: workflow satire.
- **Niu Lai viral animation phenomenon (fresh 2026-08-20):** use the meta-contrast between production theater and result-first execution; never copy its cow characters, title design, poster or frames. Claim mode: satire/workflow metaphor.
- **China humanoid-robot / AI leaderboard conversations:** useful secondary signals for specialist-tools-versus-orchestration and benchmark-chatter-versus-delivery metaphors; do not reproduce proprietary designs/UI or claim benchmark superiority.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
