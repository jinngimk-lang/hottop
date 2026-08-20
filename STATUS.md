# Hottop Status

Last updated: 2026-08-20 22:00 +08:00
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
- First live public-web research batch archived at `examples/runs/2026-08-20-evening-briefs.json` covering The Odyssey, the Niu Lai viral animation phenomenon, and the current humanoid-robot 'ChatGPT moment' discussion.
- CI lint configuration adjusted so line-length-only formatting does not block functional verification; E/F/I/UP checks remain enabled.
- Added `build_batch(...)` pipeline to dedupe, rank and generate multiple briefs in one reusable call.
- Added CLI `hottop batch` command with JSON file output support.
- Archived a second fresh research batch at `examples/runs/2026-08-20-night-briefs.json`, covering the Niu Lai viral wave, China rocket-launch tourism, and the current multi-agent coding-agent category conversation around Meta Muse Code.
- Added a RED-first test contract and implementation for an optional Firecrawl v2 enrichment adapter. It uses `/v2/scrape`, bearer-token auth, Markdown output and a network-free configuration doctor; Crawl4AI remains the preferred self-hostable browser/deep-page layer.
- Archived a third fresh research batch at `examples/runs/2026-08-20-2100-briefs.json` covering China humanoid-robot market mania, the crowded AI model leaderboard conversation, and AI-assisted film production. All three concepts remain satire/workflow metaphor rather than unsupported benchmark claims.
- Confirmed CI is green on commit `87366a32` (workflow run 40), which includes the Firecrawl adapter and 21:00 data archive.
- Archived a fourth live batch at `examples/runs/2026-08-20-2200-briefs.json` using fresh Aug. 20/18 signals: Reuters + FT coverage of the Niu Lai meme wave, AP box-office coverage keeping The Odyssey culturally current, and Axios reporting on cross-platform video-view metric confusion. The briefs deliberately map only broad conflict/archetype language, not protected film characters/UI assets.

## In progress

- Expanding source diversity and evidence enrichment.
- Adding explicit source freshness/quality metadata and render-provider handoff.
- Preparing direct multi-collector fan-in for `hottop batch`.

## Next actions

1. Add explicit source/evidence freshness metadata and source-quality weighting, with deterministic tests.
2. Extend `hottop doctor` to report Agent-Reach/Crawl4AI/Firecrawl readiness without making optional services CI requirements.
3. Add more live-source presets for film/entertainment, AI/tech and Chinese internet/culture signals.
4. Add a renderer handoff schema so approved briefs can be sent to an image-generation endpoint without coupling the core pipeline to one vendor.
5. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
6. Confirm CI after the 22:00 archive/status commits. If green, continue Foundation v0.1 contracts; if red, repair before feature expansion.
7. Once the remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **Niu Lai viral animation phenomenon (fresh 2026-08-20, Reuters + FT):** the strongest current China culture signal. Use the meta-contrast between production theater and result-first execution; never copy its cow characters, title design, poster or frames. Claim mode: satire/workflow metaphor.
- **The Odyssey box-office conversation (fresh through 2026-08-17/20):** still highly recognizable. Use only public-domain Homeric archetypes such as a generic one-eyed cave giant and anonymous strategist. Never reproduce Nolan film actors, costumes, sets or frames. Claim mode: satire.
- **Video-view metric debate (fresh 2026-08-18/20):** use a fictional giant VIEW COUNTER versus an unfinished campaign board. Never reproduce YouTube/TikTok UI or imply InkClawAgent increases engagement. Claim mode: workflow satire.
- **China humanoid-robot market mania (fresh 2026-08-19/20):** use a fictional robotics expo to contrast many specialist tools with an orchestration layer. Never reproduce Unitree/Tesla/proprietary robot designs. Claim mode: satire/workflow metaphor.
- **AI model leaderboard conversation (fresh 2026-08-17/20):** use a fictional race scoreboard where spectators debate tiny ranking gaps while the user still needs an end-to-end job completed. Do not reproduce real leaderboards, logos, scores or claim InkClawAgent wins model benchmarks. Claim mode: satire.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
