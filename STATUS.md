# Hottop Status

Last updated: 2026-08-20 20:05 +08:00
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
- CI is green on the batch-pipeline implementation commit (`6e7e7eac`, workflow run 29).
- Added `build_batch(...)` pipeline to dedupe, rank and generate multiple briefs in one reusable call.
- Added CLI `hottop batch` command with JSON file output support.
- Archived a second fresh research batch at `examples/runs/2026-08-20-night-briefs.json`, covering the Niu Lai viral wave, China rocket-launch tourism, and the current multi-agent coding-agent category conversation around Meta Muse Code.

## In progress

- Watching the latest data/status commits for CI completion; the last code-bearing commit is green.
- Expanding source diversity and evidence enrichment.
- Adding source freshness/quality metadata and render-provider handoff.

## Next actions

1. Add explicit source/evidence freshness metadata and source-quality weighting.
2. Add Firecrawl adapter as an optional enrichment fallback; keep Crawl4AI as the primary self-hostable browser/deep-page layer.
3. Add integration doctor checks for Agent-Reach/Crawl4AI/Firecrawl without making optional services CI requirements.
4. Add more live-source presets for film/entertainment, AI/tech and Chinese internet/culture signals.
5. Add a renderer handoff schema so approved briefs can be sent to an image-generation endpoint without coupling the core pipeline to one vendor.
6. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
7. Once the remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **Niu Lai viral animation phenomenon (fresh 2026-08-20):** strongest current China culture/meme signal. Use the contrast between elaborate production theater and result-first execution, but never copy its cow characters, title design, poster or frames. Claim mode: satire.
- **China rocket-launch tourism (fresh 2026-08-19/20):** visually strong launch/control-room metaphor. Best mapping: old workflow = endlessly preparing on the ground; InkClawAgent = coordinating tasks into an actual launch. Use generic spacecraft and no agency marks. Claim mode: satire.
- **Multi-agent coding-agent wave / Meta Muse Code:** timely category signal for specialist coding agents versus a broader multi-agent workbench. Do not claim benchmark superiority; frame as breadth/orchestration positioning only. Claim mode: satire/category metaphor.
- **The Odyssey:** still usable as a film-language meme shell, but keep to generic mythic-voyage/cyclops archetypes and original visual treatment rather than movie-specific assets.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, or identifiable proprietary robot designs in generated prompts.
