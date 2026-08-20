# Hottop Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested hot-topic acquisition, ranking, semantic-mapping and four-panel meme-brief pipeline with optional Agent-Reach and Crawl4AI integrations.

**Architecture:** Keep core logic dependency-light and deterministic. All heterogeneous data sources normalize into Pydantic models; collectors/adapters live behind small interfaces; the creative layer emits structured briefs and risk flags. Large upstream tools run outside the repository and are integrated through CLI/HTTP/MCP boundaries.

**Tech Stack:** Python 3.11+, Pydantic 2, httpx, feedparser, PyYAML, Typer, pytest, GitHub Actions, optional Docker/Crawl4AI and Agent-Reach.

**Spec:** `docs/superpowers/specs/2026-08-20-hottop-foundation-design.md`

## Global Constraints

- No secrets, cookies or browser profiles in Git.
- Optional authenticated channels are not CI requirements.
- Unsupported objective comparison claims must be marked `needs_evidence` or rewritten as satire/metaphor.
- Image prompts must avoid actor likenesses, exact frames, official posters and protected character-design replication.
- Agent-Reach and Crawl4AI are adapters/services, not vendored source trees.

---

### Task 1: Core models and scorer

**Files:**
- Create: `src/hottop/models.py`
- Create: `src/hottop/scoring.py`
- Test: `tests/test_models.py`
- Test: `tests/test_scoring.py`

**Interfaces:**
- Produces: `Evidence`, `TrendCandidate`, `TrendScore`, `ProductProfile`, `RoleMap`, `Panel`, `MemeBrief`, `score_candidate(candidate, now=None)`.

- [ ] Write model/scoring tests first.
- [ ] Run CI/test and verify RED because `hottop` production modules are missing.
- [ ] Implement minimal models and deterministic scoring.
- [ ] Run tests and verify GREEN.

### Task 2: Role mapping and claim guardrail

**Files:**
- Create: `src/hottop/mapping.py`
- Create: `src/hottop/guardrails.py`
- Test: `tests/test_mapping.py`
- Test: `tests/test_guardrails.py`

**Interfaces:**
- Consumes: `TrendCandidate`, `ProductProfile`.
- Produces: `infer_archetype(candidate) -> str`, `build_role_map(candidate, product, comparison_target=None) -> RoleMap`, `classify_claim(text, evidence_count) -> ClaimStatus`.

- [ ] Write failing mapping/guardrail tests.
- [ ] Verify RED.
- [ ] Implement minimal deterministic rules.
- [ ] Verify GREEN.

### Task 3: Zero-auth discovery collectors

**Files:**
- Create: `src/hottop/collectors/base.py`
- Create: `src/hottop/collectors/dailyhot.py`
- Create: `src/hottop/collectors/rss.py`
- Create: `src/hottop/collectors/newsnow.py`
- Create fixtures under `tests/fixtures/`
- Test: `tests/test_collectors.py`

**Interfaces:**
- Produces: async `collect(limit: int) -> list[TrendCandidate]`.

- [ ] Add fixture tests for JSON/RSS normalization and malformed records.
- [ ] Verify RED.
- [ ] Implement collectors with timeouts and typed source errors.
- [ ] Verify GREEN.

### Task 4: Deduplication and cross-source boost

**Files:**
- Create: `src/hottop/dedupe.py`
- Test: `tests/test_dedupe.py`

**Interfaces:**
- Produces: `merge_candidates(items) -> list[TrendCandidate]`.

- [ ] Test canonical URL and normalized-title merging.
- [ ] Verify RED, implement, verify GREEN.

### Task 5: Agent-Reach integration

**Files:**
- Create: `integrations/versions.yml`
- Create: `scripts/install_agent_reach.sh`
- Create: `src/hottop/integrations/agent_reach.py`
- Test: `tests/test_agent_reach.py`

**Interfaces:**
- Produces: `AgentReachAdapter.doctor()` and command builders/readers for supported public channels.

- [ ] Pin upstream tested commit.
- [ ] Test command construction and parser fixtures without credentials.
- [ ] Add safe installer that defaults to Agent-Reach check-only behavior.
- [ ] Verify tests.

### Task 6: Crawl4AI HTTP/MCP integration

**Files:**
- Create: `docker-compose.integrations.yml`
- Create: `mcp/crawl4ai.json`
- Create: `src/hottop/integrations/crawl4ai.py`
- Test: `tests/test_crawl4ai.py`

**Interfaces:**
- Produces: `Crawl4AIAdapter.markdown(url)`, `.screenshot(url)`, `.doctor()`.

- [ ] Add fake-transport tests for request/response parsing.
- [ ] Add pinned Docker service + MCP endpoint config.
- [ ] Implement adapter and verify tests.

### Task 7: Meme brief builder

**Files:**
- Create: `src/hottop/briefing.py`
- Test: `tests/test_briefing.py`

**Interfaces:**
- Produces: `build_brief(candidate, product, comparison_target=None) -> MemeBrief`.

- [ ] Test four-panel structure, punchline and copyright exclusions.
- [ ] Verify RED.
- [ ] Implement setup→escalation→reversal→punchline builder.
- [ ] Verify GREEN.

### Task 8: CLI and doctor

**Files:**
- Create: `src/hottop/cli.py`
- Create: `src/hottop/doctor.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces CLI commands `discover`, `rank`, `brief`, `doctor`.

- [ ] Write CLI smoke tests.
- [ ] Verify RED, implement, verify GREEN.

### Task 9: Reusable skill and source configuration

**Files:**
- Create: `skills/hottop-meme/SKILL.md`
- Create: `config/sources.yml`
- Create: `config/products/inkclawagent.yml`
- Update: `README.md`

- [ ] Encode the durable creative workflow and product profile.
- [ ] Add DailyHotApi, NewsNow and RSSHub source presets.
- [ ] Document optional Agent-Reach/Crawl4AI setup.

### Task 10: CI, first real run, PR and merge

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `examples/runs/YYYY-MM-DD/*.json|md`
- Update: `STATUS.md`

- [ ] Run CI on Python 3.11/3.12.
- [ ] Discover fresh topics from at least two public sources.
- [ ] Rank and generate at least three meme briefs.
- [ ] Archive sources/evidence/risk flags.
- [ ] Open PR; inspect diff and CI; fix findings.
- [ ] Merge when green and update `STATUS.md` with next milestone.
