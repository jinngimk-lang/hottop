# Adaptive Creative Orchestrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn Hottop's existing creative contracts into a smooth adaptive front door that resolves intent, asks only high-impact questions, applies platform/style/ambition/project-shape routing, ranks context-fit concepts, and packages the selected concept for render-v2.

**Architecture:** Keep the core deterministic and provider-neutral. Natural-language intent parsing uses transparent keyword/rule inference as a Foundation baseline, while accepting explicit structured overrides from conversational/LLM front ends. `CreativeIntent` and `InteractionState` live in a focused intake module; platform/style policies live in profiles; contextual review augments but never bypasses the existing hard creative gate; the orchestrator composes existing `CreativeConcept`, `CreativeReview`, `VisualReference`, Creative Package and render-v2 contracts.

**Tech Stack:** Python 3.11/3.12, Pydantic 2, Typer, pytest, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-21-adaptive-creative-orchestrator-design.md`

## Global Constraints

- Preserve arbitrary brand/product/service/feature/campaign/person/idea/keyword/tool semantics.
- Ask 0–3 questions by default; do not emit a static full questionnaire.
- Explicit user values always beat inference; inferred fields carry confidence/provenance.
- Platform/style/ambition must alter creative routing, not only renderer adjectives.
- Existing seven-part `CreativeReview` hard gate remains authoritative; contextual fit only ranks concepts that pass it.
- Never make unsupported factual competitor claims; downgrade to satire/metaphor/generic proxy when evidence is weak.
- No mandatory LLM provider, vector database, browser session, secret, paid API or GPU runtime in the core package.
- Preserve flexible expression forms and `hottop.render.v2`; do not regress to four-panel-only behavior.
- Update `PROJECT.md`, reusable skill doctrine, `STATUS.md` and the persistent loop when durable interaction doctrine changes.

---

### Task 1: CreativeIntent and provenance contract

**Files:**
- Create: `src/hottop/intake.py`
- Create: `tests/test_intake.py`

**Interfaces:**
- Produces: `CreativeIntent`, `IntentValue[T]`, `CreativeAmbition`, `ProductVisibility`, `CampaignGoal`, `Platform`, `CreativeStyle`, `resolve_intent(request: str, overrides: dict | None = None) -> CreativeIntent`.
- Consumes later: `QuestionRouter`, platform/style profiles and orchestrator.

- [ ] Write failing tests that prove explicit values override inferred values and that a natural request can infer platform/style/ambition/product visibility without requiring an LLM.
- [ ] Run `pytest tests/test_intake.py -v` and confirm RED because `hottop.intake` does not exist.
- [ ] Implement Pydantic contracts with per-field `value`, `source` (`explicit|inferred|defaulted`) and confidence; add conservative keyword inference for common Chinese/English platform/style/ambition phrases.
- [ ] Run `ruff check src/hottop/intake.py tests/test_intake.py` and `pytest tests/test_intake.py -v`; confirm GREEN.
- [ ] Commit.

### Task 2: High-impact QuestionRouter

**Files:**
- Modify: `src/hottop/intake.py`
- Modify: `tests/test_intake.py`

**Interfaces:**
- Produces: `GuidedQuestion`, `InteractionState`, `next_question(intent: CreativeIntent, *, asked_fields: list[str] | None = None, budget: int = 3) -> InteractionState`.

- [ ] Add failing tests for: no redundant question when request already provides platform/style/target; target ambiguity asked before style; audience is not asked for ordinary consumer requests; budget 0 returns ready/default behavior rather than a questionnaire.
- [ ] Run targeted tests and confirm RED.
- [ ] Implement impact-priority routing and compact 2–6 option questions with optional free-text fallback.
- [ ] Re-run Ruff + targeted tests and confirm GREEN.
- [ ] Commit.

### Task 3: Platform, style and project-shape profiles

**Files:**
- Create: `src/hottop/profiles.py`
- Create: `tests/test_profiles.py`

**Interfaces:**
- Produces: `PlatformProfile`, `StyleProfile`, `ProjectShapeProfile`, `get_platform_profile(platform)`, `get_style_profile(style)`, `infer_project_shape(category: str)`, `derive_routing_hints(intent, promotion_context) -> RoutingHints`.

- [ ] Write failing tests demonstrating Xiaohongshu biases carousel/cover-hook, Douyin biases short motion hooks, LinkedIn biases reframe/evidence, paid-social biases early product visibility; minimal-premium lowers text density; funny-meme raises reversal/punchline; food routes to sensory/product-led grammar while software routes to workflow/reframe grammar.
- [ ] Confirm RED because `hottop.profiles` does not exist.
- [ ] Implement small transparent profile tables and routing hints; do not create platform-specific renderers.
- [ ] Run Ruff + targeted tests and confirm GREEN.
- [ ] Commit.

### Task 4: Context-aware creative review

**Files:**
- Modify: `src/hottop/creative.py`
- Create: `tests/test_contextual_review.py`

**Interfaces:**
- Produces: `CreativeContextReview`, `ContextualCreativeReview`, `review_with_context(base: CreativeReview, context: CreativeContextReview) -> ContextualCreativeReview`, `select_best_contextual_review(...)`.

- [ ] Write failing tests proving: a concept failing base `CreativeReview` can never pass due to contextual scores; among passing concepts, platform/style/goal/ambition/project-shape/hotspot-native/humor scores alter ranking; humor is optional when style/goal does not require it.
- [ ] Confirm RED.
- [ ] Implement contextual weighted score as a secondary ranking layer while delegating pass/fail to `base.passes`.
- [ ] Run Ruff + targeted tests and full creative tests; confirm GREEN.
- [ ] Commit.

### Task 5: Adaptive orchestrator and Creative Package integration

**Files:**
- Create: `src/hottop/orchestrator.py`
- Modify: `src/hottop/creative_package.py`
- Create: `tests/test_orchestrator.py`

**Interfaces:**
- Produces: `OrchestrationInput`, `OrchestrationResult`, `orchestrate(input: OrchestrationInput) -> OrchestrationResult`.
- Reuses: `CreativeConcept`, `CreativeReview`, contextual reviews, `VisualReference`, `build_creative_render_request`.

- [ ] Write failing tests for three candidate concepts (pain contrast, bridge-led reveal, category reframe) where routing/context selects a platform-fit winner; test fallback when all candidates fail base gate; test alternate summaries retained for revision controls.
- [ ] Confirm RED.
- [ ] Implement orchestration that rejects all-fail packages, ranks passing candidates by contextual score, preserves selected render-v2 and concise selection rationale, and returns revision-ready alternates.
- [ ] Run Ruff + targeted tests and confirm GREEN.
- [ ] Commit.

### Task 6: Smooth CLI front door

**Files:**
- Modify: `src/hottop/cli.py`
- Create: `tests/test_adaptive_cli.py`
- Modify or create: `tests/test_creative_package_cli.py`

**Interfaces:**
- Produces commands:
  - `hottop intent "<natural request>" [--output PATH]`
  - `hottop next-question <intent.json> [--output PATH]`
  - `hottop package-concepts <package.json> [--output PATH]`
  - `hottop orchestrate <orchestration.json> [--output PATH]`

- [ ] Add failing CLI tests for all four commands, including the currently missing `package-concepts` command from the existing RED contract.
- [ ] Confirm RED and inspect exact failures.
- [ ] Implement loaders and commands using core modules only; all outputs are JSON and provider-neutral.
- [ ] Run Ruff + targeted CLI tests and confirm GREEN.
- [ ] Commit.

### Task 7: Representative project-shape fixtures

**Files:**
- Create: `examples/creative-packages/consumer-swipe-reveal.json`
- Create: `examples/creative-packages/software-category-reframe.json`
- Create: `examples/creative-packages/social-native-meme.json`
- Create: `tests/test_example_packages.py`

**Interfaces:**
- Examples must validate against current contracts and produce `hottop.render.v2` for the selected concept.

- [ ] Write failing contract test expecting all three fixture files.
- [ ] Confirm RED.
- [ ] Add fictional/original examples covering consumer sensory bridge + swipe reveal, software workflow constraint deletion + split-old-vs-new, and social-native humorous meme grammar; do not use protected assets or unsupported factual competitor claims.
- [ ] Run fixture tests and confirm GREEN.
- [ ] Commit.

### Task 8: Persist interaction doctrine and recovery rules

**Files:**
- Modify: `PROJECT.md`
- Modify: `skills/brand-metaphor-creative/SKILL.md`
- Modify: `STATUS.md`
- Modify: `tests/test_creative_skill_contract.py` or add `tests/test_interaction_doctrine_contract.py`

**Interfaces:**
- Durable doctrine includes adaptive guided intake, 0–3 question budget, creative ambition, platform-native routing, product visibility, project-shape adaptation, contextual review and conversational-front-end/CLI shared contracts.

- [ ] Write failing doctrine contract assertions first.
- [ ] Confirm RED.
- [ ] Update charter and skill with concise canonical rules; avoid duplicating the full design spec.
- [ ] Update `STATUS.md` with exact implemented contracts and next actions.
- [ ] Run contract tests + full suite and confirm GREEN.
- [ ] Commit.

### Task 9: Exact-head verification and PR synchronization

**Files:**
- No production file required unless verification reveals a defect.
- Update: PR #1 body only if implemented scope has materially moved beyond current text.

**Interfaces:**
- Exact branch head must pass Ruff + pytest on Python 3.11 and 3.12 in GitHub Actions.

- [ ] Fetch exact branch head and associated CI run.
- [ ] If failure: inspect logs, fix root cause with a targeted regression test, repeat until green.
- [ ] Confirm both Python jobs succeed.
- [ ] Refresh PR metadata and `STATUS.md` if the final exact-head CI fact is not yet persisted.
- [ ] Keep PR draft until remaining Foundation completion criteria in `STATUS.md` are actually satisfied.
