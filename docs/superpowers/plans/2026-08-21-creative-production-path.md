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
- Test: `tests/test_render_concept_cli.py`

**Interfaces:**
- Consumes: `CreativeConcept.model_validate(...)`, `build_creative_render_request(concept)`.
- Produces: `hottop render-concept <concept.json> [--output PATH]` returning `hottop.render.v2`.

- [x] Add a failing CLI test with a three-frame `swipe-reveal` concept and assert `schema_version`, `expression_form`, `visual_medium`, strategy fields, frame count and captions.
- [x] Run CI and confirm RED because `render-concept` does not exist (run 281).
- [x] Add `_load_concept()` and `render-concept` command using the existing `CreativeConcept` and `build_creative_render_request` contracts.
- [x] Re-run CI and confirm GREEN (implementation head `afac292c89bb742359cd4dc05da3c955271ef1cc`, run 283).

### Task 2: Optional RSSHub collector path

**Files:**
- Create: `src/hottop/collectors/rsshub.py`
- Modify: `src/hottop/batch_config.py`
- Modify: `src/hottop/cli.py`
- Test: `tests/test_rsshub.py`
- Test: `tests/test_doctor.py`

**Interfaces:**
- Produces: `RSSHubCollector(route: str, base_url: str | None = None, ...)` that delegates feed parsing to `RSSCollector`.
- CLI source spec: `rsshub:<route>`; `RSSHUB_BASE_URL` is mandatory unless constructor `base_url` is explicitly supplied.

- [x] Add failing tests for URL normalization, missing configuration, and delegation through CLI `_discover`.
- [x] Run CI and confirm RED (run 287 exposed the missing collector after lint ordering was fixed).
- [x] Implement the wrapper and extend source-type validation.
- [x] Add `hottop doctor` visibility for optional RSSHub configuration using another RED → GREEN cycle (run 299 RED, run 301 GREEN).
- [x] Re-run CI and confirm GREEN (`dca2c95a07c72a1a9941bcddcc49222e04bc0bf3` passed run 297; doctor implementation `fcfd004b6f54893a4bd0899c489ab367a0b0d09a` passed run 301).

### Task 3: Persist current implementation truth

**Files:**
- Modify: `STATUS.md`

**Interfaces:**
- Records the exact green implementation head and next actions; no transient claims are added to `PROJECT.md`.

- [x] Update Done/In progress/Next actions to include CreativeReview, visual-reference research, render v2, `render-concept`, RSSHub pilot and evidence-backed comparison ingestion.
- [x] Re-run exact-head CI after the status update.
- [x] Confirm current status head is green (`d84a9cce0872c20a0b198fcd441751fce78f9cd7`, run 311, Python 3.11/3.12).

## Follow-on completed during execution

- [x] Add `hottop position --comparisons <json>` so current public-web / front-end research can flow into deterministic comparison selection.
- [x] Normalize `claim_posture=supported` back to `satire` when the candidate has no evidence.
- [x] Verify RED at `dc02ebd8bc86db56613e8cf2e1d000a33e363a60` / run 305 and GREEN at `29f2093d8e39df39f37ef5acd7ae00a3f9bfbb8f` / run 309.
- [x] Refresh PR #1 title/body so repository coordination no longer describes Hottop as a four-panel-only pipeline; keep the PR draft until the remaining production-path contracts are stable.

## Next plan boundary

The next implementation slice should focus on **evidence acquisition + flexible production**, not additional doctrine: research-result → `ComparisonCandidate`, enrichment-before-creative, flexible `creative-batch`, representative consumer/swipe-reveal fixtures, then Foundation v0.1 review readiness.
