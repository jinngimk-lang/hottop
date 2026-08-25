# Config-Driven Video Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Hottop generate a deterministic `hottop.video-plan.v1` from `hottop.render.v2` plus repository YAML configuration, with Anti-Polish doctrine, shot continuity, dialogue/SFX/BGM, generation/compositor/encoder routing and safe external-backend commands.

**Architecture:** Keep `hottop.render.v2` as the creative contract. Add a downstream `video_production.py` model/planner that loads a `VideoProductionConfig` and emits a provider-neutral `VideoProductionPlan`; external adapters are represented as validated command specs rather than runtime dependencies. Persist Anti-Polish doctrine and pin Wan2.2 / Motion Canvas / FFmpeg / optional Remotion metadata.

**Tech Stack:** Python 3.11+, Pydantic v2, PyYAML, Typer; external optional Wan2.2, Motion Canvas and FFmpeg.

**Spec:** `docs/superpowers/specs/2026-08-24-config-driven-video-production-design.md`

## Global Constraints

- `hottop.render.v2` remains backward compatible and provider-neutral.
- CI must not require Node.js, GPU models, model downloads, or FFmpeg binaries.
- Anti-Polish means low production feel + high comedy control; continuity, subtitles, dialogue, timing, product semantics and rights safety remain precise.
- No URL/QR/hard CTA for meme/hotspot/brand-memory output unless the render request explicitly allows it.
- No copyrighted soundtrack or film footage auto-fetching.
- Remotion must remain optional because its current commercial license conditions are entity-dependent.

---

### Task 1: Video production configuration and plan contract

**Files:**
- Create: `src/hottop/video_production.py`
- Create: `tests/test_video_production.py`
- Create: `config/video/anti-polish-short.yml`

**Interfaces:**
- Consumes: `hottop.rendering.CreativeRenderRequest`
- Produces: `VideoProductionConfig`, `VideoProductionPlan`, `load_video_production_config(path: Path)`, `build_video_production_plan(render_request, config)`

- [ ] **Step 1: Write failing contract tests**

Tests must validate: YAML profile loading; 9:16 defaults; Anti-Polish style; ordered shots whose total does not exceed configured duration; continuity instructions for motion; explicit audio cues; no in-asset destination by default; Wan2.2 generation routing; Motion Canvas compositor routing; FFmpeg H.264/yuv420p/fast-start finalization.

- [ ] **Step 2: Verify RED**

Run: `pytest tests/test_video_production.py -q`
Expected: import / missing-contract failures.

- [ ] **Step 3: Implement minimal Pydantic models and deterministic planner**

Use strict enums/literals for backends and audio cue kinds. Derive shot duration from render frames deterministically, preserve frame order, carry master/negative prompts into shot prompts, and emit execution notes rather than running tools.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/test_video_production.py -q`
Expected: PASS.

---

### Task 2: CLI `video-plan`

**Files:**
- Modify: `src/hottop/cli.py`
- Create: `tests/test_video_plan_cli.py`

**Interfaces:**
- Consumes: render-v2 JSON path and video profile YAML path.
- Produces: JSON `hottop.video-plan.v1` to stdout or `--output`.

- [ ] **Step 1: Write failing CLI test**

Use Typer CliRunner with a representative motion render-v2 request and the committed Anti-Polish profile. Assert successful JSON output, schema version, configured backends and audio/continuity fields.

- [ ] **Step 2: Verify RED**

Run: `pytest tests/test_video_plan_cli.py -q`
Expected: command missing.

- [ ] **Step 3: Implement command**

Add `hottop video-plan <render-v2.json> --config <yaml> [--output]`. Do not execute external tools.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/test_video_plan_cli.py -q`
Expected: PASS.

---

### Task 3: Persist Anti-Polish doctrine and upstream pins

**Files:**
- Modify: `PROJECT.md`
- Modify: `skills/brand-metaphor-creative/SKILL.md`
- Modify: `integrations/versions.yml`
- Modify: `STATUS.md`
- Create: `tests/test_anti_polish_doctrine_contract.py`

**Interfaces:**
- Produces durable project recovery rules and reproducible upstream integration metadata.

- [ ] **Step 1: Write doctrine contract test**

Assert the durable documents include: `Anti-Polish`, `Controlled Badness`, `low production feel`, `high comedy control`, `Wan2.2`, `Motion Canvas`, and the principle that rough aesthetics must not weaken continuity/timing/subtitle correctness.

- [ ] **Step 2: Verify RED**

Run: `pytest tests/test_anti_polish_doctrine_contract.py -q`
Expected: missing doctrine / integration entries.

- [ ] **Step 3: Update documents and integration pins**

Pin:
- `Wan-Video/Wan2.2` as Apache-2.0 external local generation backend;
- `motion-canvas/motion-canvas` commit `7b91435c301d530351dcf5ebb91dd139c002e405`, MIT, external compositor;
- `FFmpeg/FFmpeg` commit `1019f8f036602a8464185baa4857654337eeca14`, external encoder;
- `remotion-dev/remotion` commit `05075f384a0a28e193876c1fd43ab9fba5ef10f9`, optional adapter candidate with license-review requirement.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/test_anti_polish_doctrine_contract.py -q`
Expected: PASS.

---

### Task 4: Full exact-head verification

**Files:**
- Modify only if failures reveal concrete regressions.

- [ ] **Step 1: Run Ruff**

Run: `ruff check .`
Expected: all checks passed.

- [ ] **Step 2: Run full pytest**

Run: `pytest`
Expected: all tests passed.

- [ ] **Step 3: Verify PR exact-head CI**

Fetch PR #1 head SHA and its GitHub Actions run. Repair only reproducible failures; do not claim green from an older head.

- [ ] **Step 4: Refresh `STATUS.md` and PR body**

Record the new video-production path accurately. Keep PR draft unless all Foundation closure criteria are actually satisfied.
