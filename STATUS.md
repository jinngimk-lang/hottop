# Hottop Status

Last updated: 2026-08-20
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Repository initialized and persistent project brief added.
- Upstream research completed for Agent-Reach and Crawl4AI.
- Additional discovery candidates selected: DailyHotApi, NewsNow, RSSHub, with TrendRadar as a reference/optional aggregate layer.
- Integration posture fixed: adapters + pinned upstream versions/services; do not vendor large upstream repositories.
- Hourly continuation task configured to resume from this repository and keep producing/reviewing work.
- Architecture spec, implementation plan, CI workflow and first RED tests committed.

## In progress

- Verifying the RED CI baseline.
- Core schemas, ranking and role mapping.
- Collectors and upstream adapters.
- First real trend batch and meme briefs.

## Next actions

1. Inspect CI failure to verify tests fail because production modules are absent.
2. Implement schemas/ranking/mapping and make CI green.
3. Add DailyHotApi + RSS/NewsNow collectors with fixture tests.
4. Add Agent-Reach adapter + installer/doctor scripts.
5. Add Crawl4AI Docker/MCP config + adapter.
6. Add CLI: `discover`, `rank`, `brief`, `doctor`.
7. Add reusable `skills/hottop-meme/SKILL.md`.
8. Run real hot-topic discovery and archive first briefs under `examples/runs/`.
9. Open PR, inspect CI/diff, fix, and merge when green.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, or copyrighted character designs in generated prompts.
