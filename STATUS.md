# Hottop Status

Last updated: 2026-08-20 19:00 +08:00
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

## In progress

- Re-checking GitHub Actions after the CI lint adjustment and live-run commit.
- Expanding source diversity and evidence enrichment.
- Turning archived briefs into a repeatable batch command and render-provider handoff format.

## Next actions

1. Inspect the newest PR workflow run; fix any remaining test/lint failures until green.
2. Add a batch pipeline command that discovers, dedupes, ranks and writes multiple briefs in one invocation.
3. Add explicit source/evidence freshness metadata and source-quality weighting.
4. Add Firecrawl adapter as an optional enrichment fallback; keep Crawl4AI as the primary self-hostable browser/deep-page layer.
5. Add integration doctor checks for Agent-Reach/Crawl4AI/Firecrawl without making optional services CI requirements.
6. Add more live-source presets for film/entertainment, AI/tech and Chinese internet/culture signals.
7. Add a renderer handoff schema so approved briefs can be sent to an image-generation endpoint without coupling the core pipeline to one vendor.
8. When CI is green, mark PR #1 ready, inspect final diff/reviews, and merge Foundation v0.1 if no blockers remain.

## Latest live creative signals

- **The Odyssey**: strong China/IMAX momentum; use generic mythic-voyage/cyclops archetypes only. Best mapping: obstacle/maze = comparison target; clever strategist = InkClawAgent. Claim mode: satire.
- **Niu Lai viral phenomenon**: current conversation contrasts rough/earnest aesthetics with polished mainstream production. Use only the cultural contrast, never copy its characters. Best mapping: over-engineered workflow theater vs result-first multi-agent workflow. Claim mode: satire.
- **Humanoid robots / 'ChatGPT moment'**: strong visual metaphor for many capable units needing orchestration. Best mapping: manually prompted individual units vs InkClawAgent as coordination layer. Claim mode: metaphor; do not imply robotics benchmarks.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, or identifiable proprietary robot designs in generated prompts.
