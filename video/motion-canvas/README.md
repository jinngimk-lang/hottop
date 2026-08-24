# Hottop Motion Canvas scaffold

This project is the pinned Motion Canvas compositor scaffold for `hottop.video-plan.v1`.

- Motion Canvas packages are pinned to `3.17.2`.
- `npm run render -- --plan <path>` validates the plan and writes `src/generated-plan.ts`.
- The scene consumes the ordered shot timeline, captions and audio-cue timing in one continuous Motion Canvas scene.
- Generated shot inputs use the deterministic convention `/shots/shot-001.mp4`, `/shots/shot-002.mp4`, and so on; until those assets exist, the scaffold renders plan-aware placeholders rather than inventing footage.
- The script deliberately does **not** install dependencies, start a renderer, download models, provision a GPU or invoke FFmpeg. External process spawning belongs to the explicit `video-run --execute` adapter after readiness checks.

CI validates repository files/contracts only. Operators may run `npm install` in this directory when they intentionally prepare a local compositor environment.
