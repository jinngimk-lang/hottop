# Hottop Status

Last updated: 2026-08-21 03:00 +08:00
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
- Added provider-neutral renderer handoff contract in `src/hottop/rendering.py`: `RenderRequest` / `RenderPanel` plus `build_render_request(MemeBrief)`. The schema keeps four panels, captions, prompts, risk flags and claim status while deliberately excluding API keys and vendor/model settings.
- Renderer handoff was developed RED→GREEN: CI run 81 failed on the missing `hottop.rendering` module as expected; implementation commit `dd9d1153` then passed CI run 83.
- Current pre-archive renderer head is green on Python CI.
- Archived live research batches through `examples/runs/2026-08-21-0300-briefs.json`.
- The 03:00 batch adds: Reuters Niu Lai cultural phenomenon → rough-but-finished versus polished-tool-theater metaphor; Slack Code launch → coding-agent-room versus whole-project-workflow metaphor; Reuters robot “ChatGPT moment” → specialist-capability versus orchestration metaphor.

## In progress

- Expanding source diversity and evidence enrichment.
- Direct multi-collector fan-in for `hottop batch`.
- Turning source-quality defaults into explicit source presets so high-quality direct publishers can override aggregator defaults without hand-editing candidates.
- Connecting approved `RenderRequest` JSON to future image-generation providers without coupling the core package to any single vendor.

## Next actions

1. Confirm CI on the newest archive/status head; repair immediately if red.
2. Extend `hottop batch` so it can fan-in multiple configured collectors directly instead of requiring a prebuilt candidate JSON file.
3. Add a CLI/export path for provider-neutral `RenderRequest` handoffs generated from approved briefs.
4. Add source presets for film/entertainment, AI/tech and Chinese internet/culture, including per-source quality values.
5. Add optional enrichment fallback ordering: Crawl4AI first for self-hosted browser/deep-page extraction, Firecrawl second when configured, plain HTTP/RSS when sufficient.
6. Continue live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
7. Once remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **Niu Lai viral animation phenomenon (Reuters 2026-08-20):** useful for rough-but-finished versus polished-production-theater framing. Never use the film's calf/mother/leopard characters, title treatment, poster, frames or identifiable low-poly character design. Claim mode: satire/workflow metaphor.
- **Slack Code / coding agents in project channels (The Verge + Slack docs 2026-08-20):** useful for coding-specialists-versus-whole-project-team framing. Never copy Slack UI/logos or imply InkClawAgent integrates with Slack unless separately evidenced. Claim mode: workflow satire.
- **Robotics “ChatGPT moment” (Reuters 2026-08-20):** useful for many capable specialists needing an orchestration layer. Never copy Unitree hardware or imply InkClawAgent controls physical robots. Claim mode: workflow metaphor.
- **AI sovereignty / competing AI camps (Reuters 2026-08-19):** useful for `tool camps argue; user wants delivery` framing. Because the source context is geopolitical, generated art must avoid flags, politicians and endorsement framing; keep the punchline about workflow fragmentation only. Claim mode: satire.
- **The Odyssey summer visibility (AP 2026-08-16):** strong cave/giant/escape structure. Use only public-domain Homeric archetypes; never reproduce current actors, costumes, sets, posters or film frames. Claim mode: satire.
- **Robotics investment excitement (Reuters 2026-08-19):** useful for specialist-tools-versus-orchestration. Use original generic robots; never copy identifiable hardware and never imply InkClawAgent controls physical robots. Claim mode: workflow satire.
- **China robot traffic officers (Reuters 2026-08-20):** strong specialist-automation-versus-system-orchestration visual. Use completely original generic robots; never copy SUPCON hardware, police insignia or surveillance UI, and never imply InkClawAgent controls physical robots. Claim mode: workflow satire.
- **Gen-Z AI matchmaking / no-swiping trend (TechCrunch 2026-08-06):** useful for `stop endlessly choosing tools; assemble the workflow` framing. Never copy Tinder/Bumble/Ditto/Hinge UI or imply InkClawAgent is a dating product.
- **AI-agent safety/control:** useful for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail.
- **Gemini 3.7 Flash agent-workflow race:** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
