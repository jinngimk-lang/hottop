# Creative Production Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Connect the conversational creative front end to Hottop's flexible `CreativeConcept` / `hottop.render.v2` contract and add a low-risk RSSHub feed path without regressing the creative doctrine.

**Architecture:** Keep generation provider-neutral. Hottop validates and serializes structured concepts produced by a human/LLM front end, then emits renderer-neutral v2 frames. RSSHub is treated as an optional external feed router that reuses `RSSCollector`; it is never vendored and requires explicit configuration.

**Tech Stack:** Python 3.11/3.12, Pydantic 2, Typer, httpx, pytest, GitHub Actions.

**Spec:** `PROJECT.md`

## Global Constraints

- Preserve arbitrary brand/product/service/feature/keyword semantics; no permanent InkClawAgent assumption.
- Preserve `category_default`, `deleted_constraint`, `new_competition_axis`, bridge, expression form, visual medium and genre treatment through renderer handoff.
- Do not reintroduce a four-panel-only path.
- No secrets/cookies/browser profiles in Git or CI.
- RSSHub remains optional and externally hosted/self-hosted; do not vendor its AGPL source.
- Named competitor negatives still require evidence or clear satire/metaphor.

---

### Task 1: Creative concept file → render v2 CLI

**Files:**
- Modify: `src/hottop/cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `CreativeConcept.model_validate(...)`, `build_creative_render_request(concept)`.
- Produces: `hottop render-concept <concept.json> [--output PATH]` returning `hottop.render.v2`.

- [ ] Add a failing CLI test with a three-frame `swipe-reveal` concept and assert `schema_version`, `expression_form`, `visual_medium`, strategy fields, frame count and captions.
- [ ] Run CI and confirm RED because `render-concept` does not exist.
- [ ] Add `_load_concept()` and `render-concept` command using the existing `CreativeConcept` and `build_creative_render_request` contracts.
- [ ] Re-run CI and confirm GREEN.

### Task 2: Optional RSSHub collector path

**Files:**
- Create: `src/hottop/collectors/rsshub.py`
- Modify: `src/hottop/batch_config.py`
- Modify: `src/hottop/cli.py`
- Test: `tests/test_rsshub.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces: `RSSHubCollector(route: str, base_url: str | None = None, ...)` that delegates feed parsing to `RSSCollector`.
- CLI source spec: `rsshub:<route>`; `RSSHUB_BASE_URL` is mandatory unless constructor `base_url` is explicitly supplied.

- [ ] Add failing tests for URL normalization, missing configuration, and delegation through CLI `_discover`.
- [ ] Run CI and confirm RED.
- [ ] Implement the wrapper and extend source-type validation.
- [ ] Re-run CI and confirm GREEN.

### Task 3: Persist current implementation truth

**Files:**
- Modify: `STATUS.md`

**Interfaces:**
- Records the exact green implementation head and next actions; no transient claims are added to `PROJECT.md`.

- [ ] Update Done/In progress/Next actions to include CreativeReview, visual-reference research, render v2, `render-concept`, and RSSHub pilot.
- [ ] Re-run exact-head CI after the status update.
- [ ] If green, record that exact run in the next recovery cycle; if red, repair before new feature work.
