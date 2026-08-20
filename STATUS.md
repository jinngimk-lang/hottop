# Hottop Status

Last updated: 2026-08-21 05:00 +08:00
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
- Added `build_batch(...)` pipeline and `hottop batch` JSON output.
- Added optional Firecrawl v2 enrichment adapter; Crawl4AI remains the preferred self-hostable browser/deep-page layer.
- Implemented candidate/evidence source-quality and evidence-freshness scoring.
- Collectors propagate deterministic source-quality defaults and article timestamps.
- `hottop doctor` reports nonfatal readiness for Agent-Reach, Crawl4AI and Firecrawl.
- Added provider-neutral renderer handoff (`RenderRequest` / `RenderPanel`) and `hottop render` CLI.
- Added asynchronous multi-collector fan-in via `collect_and_build_batch(...)` and repeatable live `--source TYPE:KEY` options.
- CI run 105 on head `dddd0ae5` completed successfully before the 05:00 archive update.
- Archived live research batches through `examples/runs/2026-08-21-0500-briefs.json`.
- The 05:00 batch adds: Niu Lai → shipped-first-draft versus planning-theater; Chinamaxxing/China-Cool → AI-tool-collecting versus coherent workflow; China technology-tour sequence → impressive specialist demos versus end-to-end orchestration.

## In progress

- Expanding source diversity and evidence enrichment.
- Turning source-quality defaults into explicit source presets so high-quality direct publishers can override aggregator defaults without hand-editing candidates.
- Connecting approved `RenderRequest` JSON to future image-generation providers without coupling the core package to any single vendor.
- Designing optional enrichment fallback ordering: Crawl4AI first, Firecrawl second, plain HTTP/RSS when sufficient.

## Next actions

1. Confirm CI on the newest archive/status head; repair immediately if red.
2. Add source presets for film/entertainment, AI/tech and Chinese internet/culture, including per-source quality values and a small resolver API that collectors can consume.
3. Add optional enrichment fallback ordering: Crawl4AI first for self-hosted browser/deep-page extraction, Firecrawl second when configured, plain HTTP/RSS when sufficient.
4. Add a batch config file contract so repeatable collector specs can be stored as YAML rather than only CLI flags.
5. Continue live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
6. Once remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **Niu Lai viral animation phenomenon (FT 2026-08-20):** useful for shipped-first-draft versus planning-theater framing. Never use the film's characters, title treatment, poster, frames or identifiable character design. Claim mode: satire/workflow metaphor.
- **Chinamaxxing / China-Cool social trend (China Daily 2026-08-19):** useful for `AI-tool-maxxing` satire: collecting fashionable single-purpose assistants versus orchestrating a coherent workflow. Avoid flags, politics, copied creator imagery and real social-platform UI. Claim mode: satire.
- **China technology tourism (2026-08-19 reporting):** robots, autonomous rides, brain-computer demos and rocket launches provide a visual sequence for specialist-demo-versus-end-to-end-journey framing. Use only original generic hardware and never imply InkClawAgent controls physical machines. Claim mode: workflow metaphor.
- **Hot Spot release-day AI-ruler premise (AP release guide; release 2026-08-21):** useful for monolithic do-everything AI versus coordinated specialist workflow framing. Never reproduce actor likenesses, film sets, costumes, posters, title treatment or frames. Claim mode: satire.
- **World Robot Conference exhibitor density (Reuters 2026-08-20):** useful for `many specialists, who orchestrates them?` framing. Never copy identifiable robot hardware, booth branding or imply InkClawAgent controls physical robots. Claim mode: workflow metaphor.
- **Slack Code / coding agents in project channels (The Verge + Slack docs 2026-08-20):** useful for coding-specialists-versus-whole-project-team framing. Never copy Slack UI/logos or imply InkClawAgent integrates with Slack unless separately evidenced. Claim mode: workflow satire.
- **The Odyssey summer visibility (AP 2026-08-16):** strong cave/giant/escape structure. Use only public-domain Homeric archetypes; never reproduce current actors, costumes, sets, posters or film frames. Claim mode: satire.
- **AI-agent safety/control:** useful for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail.
- **Gemini 3.7 Flash agent-workflow race:** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
