# Fresh Hotspot Generation Preflight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every Hottop image/video generation path start from freshly researched hotspot evidence, a newly resolved promoted subject, and a per-request style decision instead of inherited fixed examples.

**Architecture:** Add a small provider-neutral runtime gate that validates a generation preflight record before asset generation. The gate consumes existing `ProductProfile`, `TrendCandidate`, and `Evidence` models, requires fresh observation/publication timestamps, and requires explicit per-request style/format rationale. Expose it through a CLI command and bind the rule into `PROJECT.md` plus the existing creative skills used by Chat.

**Tech Stack:** Python 3.11+, Pydantic 2, Typer, pytest, GitHub Actions.

**Spec:** User instruction in the active Hottop project session: every image/video request must re-explore current hotspot/news context; product, hotspot, and style are dynamic rather than fixed.

## Global Constraints

- Reuse existing Hottop skills and collectors; do not add a duplicate skill or dependency.
- The runtime gate must be provider-neutral and must not fetch the network itself.
- Chat/live orchestration is responsible for fresh web/news discovery; the gate validates the resulting evidence record.
- Default research observation age is at most 6 hours; default hotspot publication age is at most 7 days when a publication timestamp exists.
- A missing publication timestamp may pass only when fresh observation evidence exists; unknown timing must never be silently presented as a newly published news fact.
- Product, hotspot, visual medium/style, and output format have no historical hard-coded defaults in this gate.
- Existing archived creative examples remain readable; the gate applies to new image/video generation entrypoints rather than retroactively invalidating archives.

---

### Task 1: Runtime freshness gate

**Files:**
- Create: `tests/test_generation_preflight.py`
- Create: `src/hottop/generation_preflight.py`

**Interfaces:**
- Consumes: `ProductProfile`, `TrendCandidate`, `Evidence`.
- Produces: `GenerationPreflightInput`, `GenerationPreflightResult`, `validate_generation_preflight(...)`.

- [ ] **Step 1: Write failing tests** for fresh evidence acceptance, stale observation rejection, stale publication rejection, missing evidence rejection, and required dynamic style/output fields.
- [ ] **Step 2: Run CI and verify RED** because `hottop.generation_preflight` does not exist.
- [ ] **Step 3: Implement minimal provider-neutral validation** with timezone-aware UTC age calculations and fail-closed blockers.
- [ ] **Step 4: Run CI and verify GREEN** on Python 3.11 and 3.12.

### Task 2: CLI gate usable by operators and Chat tooling

**Files:**
- Modify: `src/hottop/cli.py`
- Create: `tests/test_generation_preflight_cli.py`

**Interfaces:**
- Consumes: a JSON preflight record.
- Produces: `hottop.generation-preflight.v1` JSON and a non-zero Typer error when blocked.

- [ ] **Step 1: Write failing CLI tests** for accepted and rejected records.
- [ ] **Step 2: Verify RED** because the command is absent.
- [ ] **Step 3: Add `hottop generation-preflight <json>`** that validates and emits the result.
- [ ] **Step 4: Verify GREEN** for command tests and full CI.

### Task 3: Bind the gate into durable project/chat doctrine

**Files:**
- Modify: `PROJECT.md`
- Modify: `skills/brand-metaphor-creative/SKILL.md`
- Modify: `skills/hottop-meme/SKILL.md`
- Create: `tests/test_fresh_hotspot_generation_contract.py`
- Modify: `STATUS.md`

**Interfaces:**
- Produces: a recovery-safe instruction that future sessions read before generating assets.

- [ ] **Step 1: Write contract tests** requiring: GitHub doctrine re-read, fresh hotspot/news exploration on every new image/video request, explicit non-fixed product/hotspot/style selection, and runtime preflight before generation.
- [ ] **Step 2: Verify RED** against the current doctrine.
- [ ] **Step 3: Update doctrine and existing skills** without creating another skill.
- [ ] **Step 4: Update `STATUS.md`** with the shipped gate and recovery instruction.
- [ ] **Step 5: Verify GREEN** across the full test suite.

### Task 4: Live conversation smoke test

**Files:**
- No repository code required.

**Interfaces:**
- Uses: current web/news search plus the repository doctrine.
- Produces: one real current-hotspot preflight record that satisfies the new gate without generating an asset unless explicitly requested.

- [ ] **Step 1: Re-read current `PROJECT.md`, `STATUS.md`, and creative skill from the branch.**
- [ ] **Step 2: Search current news/hotspot sources with current timestamps.**
- [ ] **Step 3: Build one preflight example with a dynamically selected promoted subject/hotspot/style and confirm it meets the gate semantics.**
- [ ] **Step 4: Only after repository CI is green, merge the PR and re-fetch `main` to verify the deployed doctrine/code exists.**
