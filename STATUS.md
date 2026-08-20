# Hottop Status

Last updated: 2026-08-21 01:00 +08:00
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
- Implemented `TrendCandidate.source_quality`, `Evidence.source_quality`, `Evidence.published_at`, source-quality scoring and evidence-freshness scoring.
- Collectors now propagate deterministic source-quality defaults and article timestamps into both `TrendCandidate` and `Evidence`: DailyHot defaults to 0.62, NewsNow to 0.68, RSS to configurable 0.75.
- `hottop doctor` now reports nonfatal readiness/configuration for Agent-Reach, Crawl4AI and Firecrawl without requiring optional services or credentials in CI.
- Confirmed CI green on implementation commit `312ed03e`: workflow run 71 succeeded after collector metadata and doctor changes.
- Archived live research batches through `examples/runs/2026-08-21-0100-briefs.json`.
- The 01:00 live batch adds three directions: Reuters Aug. 20 robot traffic officers → specialist-vs-orchestration metaphor; AP mid-August Odyssey visibility → public-domain cave-breakout metaphor; TechCrunch Gen-Z AI matchmaking → tool-swiping-vs-direct-team-assembly metaphor.

## In progress

- Expanding source diversity and evidence enrichment.
- Adding render-provider handoff and direct multi-collector fan-in.
- Turning source-quality defaults into explicit source presets so high-quality direct publishers can override aggregator defaults without hand-editing candidates.

## Next actions

1. Confirm CI on the latest archive/status head if a workflow is attached; repair immediately if red.
2. Add a renderer handoff schema so approved `MemeBrief` objects can be serialized for image-generation providers without coupling core logic to one vendor.
3. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
4. Add source presets for film/entertainment, AI/tech and Chinese internet/culture, including per-source quality values.
5. Add optional enrichment fallback ordering: Crawl4AI first for self-hosted browser/deep-page extraction, Firecrawl second when configured, plain HTTP/RSS when sufficient.
6. Continue hourly live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
7. Once remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **China robot traffic officers (fresh 2026-08-20, Reuters):** strong specialist-automation-versus-system-orchestration visual. Use completely original generic robots; never copy SUPCON hardware, police insignia or surveillance UI, and never imply InkClawAgent controls physical robots. Claim mode: workflow satire.
- **The Odyssey summer visibility (fresh through 2026-08-16/20, AP):** strong cave/giant/escape structure. Use only public-domain Homeric archetypes; never reproduce current actors, costumes, sets, posters or film frames. Claim mode: satire.
- **Gen-Z AI matchmaking / no-swiping trend (2026-08-06, TechCrunch):** useful for `stop endlessly choosing tools; assemble the workflow` framing. Never copy Tinder/Bumble/Ditto/Hinge UI or imply InkClawAgent is a dating product.
- **AI-agent safety/control:** useful for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail.
- **Gemini 3.7 Flash agent-workflow race:** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.
- **Niu Lai viral animation phenomenon:** useful for production-theater-versus-result-first execution; never copy its cow characters, title design, poster or frames. Claim mode: satire/workflow metaphor.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
