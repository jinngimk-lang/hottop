# Safe Config-Driven Video Execution Plan

**Goal:** Extend the green `hottop.video-plan.v1` planning path into an opt-in execution layer so a repository video profile can drive Wan2.2 shot jobs, Motion Canvas composition, and FFmpeg final encoding without arbitrary shell execution, silent dependency installation, model downloads, or paid calls.

**Architecture:** Keep `video-plan` deterministic and side-effect free. Add structured command specs generated only by trusted Hottop code, environment readiness inspection, a `video-doctor` command, and an explicit `video-run --execute` path. Execution must use `subprocess.run([...], shell=False)` and fail closed when required local resources are missing.

## Task 1 — Structured execution contract + doctor

- Add `ExternalCommandSpec(program, args, cwd, stage)` to `video_production.py` while preserving existing human-readable command strings.
- Add structured generation, compositor and finalizer command specs to `VideoProductionPlan`.
- Add `src/hottop/video_execution.py` with readiness models and `inspect_video_environment()`.
- Check only local state: Wan2.2 repo/generate.py, configured model path, Node/npm, Motion Canvas project/package, FFmpeg binary.
- Never install/download anything.
- Add `hottop video-doctor --config ...`.
- TDD RED → GREEN.

## Task 2 — Motion Canvas project scaffold

- Commit a small `video/motion-canvas/` project pinned to Motion Canvas 3.17.2.
- The scaffold reads `hottop-video-plan.json` and creates one continuous timeline with placeholder/generated shot video inputs, captions and audio cues.
- Keep dependencies external; CI validates files/contracts but does not run npm install/render.
- Provide a deterministic render script entry used by the structured compositor command.

## Task 3 — Opt-in executor

- Add `hottop video-run <render-v2.json> --config ... --output-dir ...` dry-run by default.
- `--execute` is required before spawning external processes.
- Write plan/manifest to output directory.
- Execute only trusted structured specs in stage order; `shell=False`; explicit cwd; capture stdout/stderr summaries.
- Refuse execution when readiness is incomplete.
- Never auto-download Wan2.2 weights, install npm packages, provision GPU, call paid APIs, or enable Remotion.

## Task 4 — Representative Anti-Polish story fixture

- Add an original rough-3D cow/snake/mother InkClawAgent motion fixture and expected `hottop.video-plan.v1` archive.
- Preserve user-supplied product claims as user-provided: no deploy, low development barrier, Free Token entry wording; never imply unlimited/permanent free.
- Use original staging and broad low-budget 3D grammar only; no exact film frame/character/soundtrack.

## Task 5 — Full verification / PR sync

- Ruff + full pytest on exact head.
- Update STATUS and PR #1 body.
- Keep PR draft until remaining Foundation closure review is complete.
