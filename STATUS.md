# Hottop Status

Last updated: 2026-08-20 23:59 +08:00
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
- Archived live research batches through `examples/runs/2026-08-20-2359-briefs.json` covering film, AI/tech, Chinese internet/culture and workflow-metaphor creative directions.
- Confirmed CI green on PR head `e12e4ae7` before this run: workflow run 49 succeeded.
- Added RED-first scoring coverage for explicit source quality and evidence freshness. The test-only commit `439f0b8e` produced the expected failing CI run 51.
- Implemented `TrendCandidate.source_quality`, `Evidence.source_quality`, `Evidence.published_at`, source-quality scoring and evidence-freshness scoring. Implementation commit `93a5c5e8` passed CI run 55.
- Added a 23:59 live batch with three fresh creative directions: AI-agent safety/control-tower metaphor (Reuters Aug. 18), Gemini 3.7 Flash single-leg-speed-vs-full-workflow metaphor (Reuters Aug. 13), and a public-domain Odyssey cave-escape concept. The Reuters Connect/Cover Media Odyssey signal is explicitly downgraded in source quality because Reuters Connect says it was not Reuters-verified.

## In progress

- Expanding source diversity and evidence enrichment.
- Propagating source-quality/freshness metadata automatically from collectors instead of relying on manually enriched live batches.
- Adding render-provider handoff and direct multi-collector fan-in.

## Next actions

1. Confirm CI on the latest 23:59 archive/status head; repair immediately if red.
2. Teach collectors/presets to assign deterministic default `source_quality` values and preserve article `published_at` evidence metadata automatically.
3. Extend `hottop doctor` to report Agent-Reach/Crawl4AI/Firecrawl readiness without making optional services CI requirements.
4. Add more live-source presets for film/entertainment, AI/tech and Chinese internet/culture signals.
5. Add a renderer handoff schema so approved briefs can be sent to an image-generation endpoint without coupling the core pipeline to one vendor.
6. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
7. Once the remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **AI-agent safety/control (fresh 2026-08-18/20, Reuters):** strong visual metaphor for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail. Claim mode: workflow satire.
- **Gemini 3.7 Flash agent-workflow race (fresh 2026-08-13/20, Reuters):** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.
- **The Odyssey billion-dollar visibility (fresh through 2026-08-10/20):** still highly recognizable, but the current Reuters Connect item is Cover Media material and explicitly not Reuters-verified, so evidence quality is lower. Use only public-domain Homeric archetypes; never reproduce actors, costumes, sets or film frames.
- **Niu Lai viral animation phenomenon:** useful for production-theater-versus-result-first execution; never copy its cow characters, title design, poster or frames. Claim mode: satire/workflow metaphor.
- **China humanoid-robot / AI leaderboard conversations:** useful secondary signals for specialist-tools-versus-orchestration and benchmark-chatter-versus-delivery metaphors; do not reproduce proprietary designs/UI or claim benchmark superiority.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
