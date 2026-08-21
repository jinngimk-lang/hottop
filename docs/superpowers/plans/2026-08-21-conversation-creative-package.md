# Conversation Creative Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the agreed “conversation = creative front end, Hottop = durable backend” workflow a first-class repository contract. A chat/LLM can propose multiple fully structured creative options and reviews; Hottop deterministically rejects weak options, selects the best passing concept, preserves visual-reference provenance, and emits the selected `hottop.render.v2` handoff.

**Architecture:** Do not duplicate creative reasoning inside deterministic code. The front end supplies `CreativeConcept` + `CreativeReview` pairs. A new package layer validates the pairs, applies existing hard review gates and weighted totals, selects the best passing option, and serializes provenance + selected render request. This keeps direct conversational production fast while making repeated output auditable and recoverable.

**Tech Stack:** Python 3.11/3.12, Pydantic 2, Typer, pytest, GitHub Actions.

**Spec:** `PROJECT.md`, `skills/brand-metaphor-creative/SKILL.md`, `skills/creative-reference-research/SKILL.md`.

## Global Constraints

- Do not make deterministic code pretend to invent good metaphors; it validates and selects supplied options.
- Preserve all `CreativeConcept` doctrine fields and `VisualReference` provenance.
- Only concepts whose `CreativeReview.passes` is true are eligible for final selection.
- If every option fails the hard review gate, fail clearly instead of silently choosing the least-bad idea.
- Output must include the selected provider-neutral `hottop.render.v2` request.
- Third-party reference pixels remain analysis-only; package stores only structured `VisualReference` metadata/grammar.

### Task 1: Package contract and deterministic selector

**Files:**
- Create: `src/hottop/creative_package.py`
- Test: `tests/test_creative_package.py`

- [ ] Add RED tests for selecting the highest-scoring passing reviewed concept and rejecting a package where all concepts fail.
- [ ] Implement `ReviewedCreativeOption`, `CreativePackageInput`, `CreativePackageResult`, and `build_creative_package()`.
- [ ] Preserve rejected-option diagnostics, references, selected concept and `hottop.render.v2` output.
- [ ] Verify GREEN on Python 3.11/3.12.

### Task 2: CLI front-end handoff

**Files:**
- Modify: `src/hottop/cli.py`
- Test: `tests/test_creative_package_cli.py`

- [ ] Add RED CLI test for `hottop package-concepts <package.json>`.
- [ ] Load/validate `CreativePackageInput`, build package result and optionally write `--output`.
- [ ] Verify GREEN.

### Task 3: Representative consumer/swipe-reveal fixture

**Files:**
- Create: `examples/creative-packages/consumer-swipe-reveal.json`
- Modify: `STATUS.md`

- [ ] Add a rights-safe, fictional consumer-food example with three explored creative directions and one selected swipe-reveal/product-as-action concept.
- [ ] Include at least one abstract `VisualReference` manifest with `what_not_to_copy` and `analysis-only` rights mode.
- [ ] Update status with exact RED/GREEN evidence and next production-path work.
