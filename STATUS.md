# Hottop Status

Last updated: 2026-08-24 16:06 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1
PR: #1 — open, draft, mergeable

## Current foundation state

- Hottop is a cross-category hot-topic brand creative engine, not InkClawAgent-only, AI-only, static-only or four-panel-only. `PROJECT.md` and reusable skills are the durable doctrine.
- Core trend discovery/enrichment, dedupe/ranking, evidence-aware comparison, adaptive intake, project/platform/style routing, category reframing, bridge search, Creative Review/contextual review, orchestration, flexible `CreativeConcept` and provider-neutral `hottop.render.v2` are implemented.
- Social/hotspot creative is ad-light by default: no in-asset URL/QR/hard CTA for meme/brand-memory work unless conversion intent explicitly overrides it.
- Motion-native ideas preserve character/scene/action continuity instead of becoming slideshow-like still sequences. Product benefits appear first as dialogue, action or visible consequences.
- Provenance-first visual references remain grammar-only; protected film frames, soundtrack, character designs, proprietary UI and copied layouts are not default generation inputs.

## Anti-Polish / Controlled Badness video path

- **Anti-Polish / Controlled Badness** is a durable selectable Hottop strategy: `low production feel + high comedy control`. Rough/cheap 3D, simple materials, awkward motion, deadpan acting, crude Foley and cheap-sounding music may be intentional; character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety and rights safety remain hard requirements.
- Durable rule: **Do not polish the badness away; make the badness precise.** Product UI/benefits should remain native to the rough world instead of switching into generic glossy blue-purple AI-ad aesthetics.
- `config/video/anti-polish-direct.yml` is the unattended direct profile: Wan2.2 optional local generation → MoviePy deterministic headless composition → FFmpeg compatibility encoding. `config/video/anti-polish-short.yml` keeps Motion Canvas as an optional advanced compositor path.
- `src/hottop/video_production.py` defines `VideoProductionConfig`, `VideoProductionPlan`, ordered shots, continuity instructions, audio cues and trusted structured command specs (`program`, `args`, `cwd`, `stage`).
- `hottop video-plan <render-v2.json> --config ... [--output plan.json]` emits provider-neutral `hottop.video-plan.v1`. Planning is side-effect free with respect to external tools.
- `src/hottop/video_execution.py` provides fail-closed readiness inspection plus `hottop video-doctor`; it checks only operator-controlled local state and never installs packages, downloads models, provisions GPUs or calls paid services.
- `hottop video-run <render-v2.json> --config ... --output-dir ...` is implemented. It is dry-run by default and materializes the plan/workspace without spawning external processes. Only explicit `--execute` may run trusted stages after readiness passes, using structured argument arrays, `shell=False`, fixed stage order and explicit working directories.
- Execute mode now requires **fresh stage outputs**: before each generation/compositor/finalization command, any pre-existing expected output file is removed; a zero return code is accepted only if that stage then produces a new non-empty file. Stale files from a previous run cannot satisfy the success contract.
- Dry-run is now project-tree safe for the Motion Canvas path: it no longer writes `hottop-video-plan.json` into `video/motion-canvas/`; the optional compositor receives the output-workspace plan via an absolute `--plan` path only when the runtime command is executed.
- `video/motion-canvas/` remains a pinned Motion Canvas 3.17.2 scaffold for advanced vector-motion / interactive-preview treatment rather than a requirement for unattended execution.
- `examples/video/inkclaw-cow-snake.render.json` is the editable canonical Anti-Polish cow/snake/mother story source. `examples/video/inkclaw-cow-snake.video-plan.json` is a representative `hottop.video-plan.v1` derived archive; its execution notes explicitly require regeneration from the render + repository config when planner behavior changes rather than treating the archive as a second creative source of truth.
- The representative story keeps the user-provided wording `不用部署`, `开发零门槛`, and `Free Token 入门`, while avoiding unlimited/permanent-free implications, named-competitor defect claims, protected source footage, protected character designs and copyrighted soundtrack.
- Upstreams remain pinned in `integrations/versions.yml`: Wan2.2 optional Apache-2.0 local generation, MoviePy MIT headless composition, Motion Canvas MIT optional advanced composition, and FFmpeg external compatibility encoding with build-dependent licensing. Remotion remains disabled by default pending operator license review.
- Design/spec: `docs/superpowers/specs/2026-08-24-config-driven-video-production-design.md`.
- Planning implementation: `docs/superpowers/plans/2026-08-24-config-driven-video-production.md`.
- Safe execution follow-on: `docs/superpowers/plans/2026-08-24-video-execution-adapter.md`.

## Verification evidence

- Earlier provider-neutral video planning, `video-doctor`, trusted structured command specs and Motion Canvas scaffold contracts were introduced RED-first and verified on Python 3.11 / 3.12.
- Recovery head `fc17af66dcc2e2dd040d9603dc0ee71ccf634a6b` exposed a Ruff-only import-order regression in `tests/test_anti_polish_doctrine_contract.py` (CI run 871). Minimal formatting fix `567f1231d0ee5d0d6b0c398d94865449b5d70c8d` restored exact-head CI in run 873.
- The representative video-plan archive was introduced RED-first at `47427420ff7f42fdcda397cf9828456a69158a1f`: run 875 passed Ruff and failed exactly once because `examples/video/inkclaw-cow-snake.video-plan.json` did not exist (`1 failed / 275 passed`). The representative derived archive plus contract head `fe418ee7aff38d3bf74c5ac4ce35ad284e8c7146` passed exact-head CI run 879.
- Motion Canvas dry-run project-tree safety was introduced RED-first at `d259f92dcb6e3a6834175ace19ca9f472b300dc8`: run 881 passed Ruff and failed exactly once because dry-run wrote a plan into the compositor project (`1 failed / 276 passed`). Minimal implementation head `645111dbcc9061a6bbdb09feb09ebe3a4702e3ae` now passes exact-head CI run 883 on Python 3.11 and 3.12.
- Basic execute-stage output verification was added at `7ca96c7d45fde4c8df9fe46bb2dcad76ba592e06`; exact-head CI run 889 passed after requiring generation/compositor/finalization to emit non-empty expected files.
- Fresh-output safety was introduced RED-first at `a484c8c8d1eec13a1cefd5848d391f2872274dab`: CI run 891 passed Ruff and failed exactly once because pre-existing non-empty MP4s could satisfy a no-op successful stage (`1 failed / 278 passed`). The implementation now removes each expected output before the trusted command and verifies a newly produced non-empty file. An initial GREEN wording change exposed only a backward-compatible error-message assertion in run 893; compatibility fix head `fce71de7539bf2078086a7a9f361b5ee4a7fd9eb` passes exact-head CI run 895 on Python 3.11 and 3.12.

## Current creative doctrine

- Reframe before optimize: identify `category_default`, test constraint deletion, derive `new_competition_axis`.
- Natural bridge before logo: search shape/material, action/motion, role, function, emotion/ritual and language/symbol.
- Format follows the idea; medium follows the hotspot; motion follows timing/action/dialogue/sound when those carry recognition.
- Anti-Polish is a valid competition axis when intentional roughness makes the work more native, memorable and less ad-like.
- Product benefits belong inside the joke as consequences; do not replace the joke with feature cards.
- Named competitor negatives require evidence or unmistakable satire; otherwise use a generic proxy or old category assumption.
- Creative Review remains the hard gate; contextual fit only ranks concepts that already pass.
- References teach grammar, not pixels.

## In progress

- Foundation v0.1 accumulated PR diff / production-contract closure review continues.
- The safe video execution adapter is implemented at the code-contract level: provider-neutral plan, readiness inspection, dry-run workspace, explicit opt-in execution, MoviePy headless composition, optional Motion Canvas path, FFmpeg finalization, stage output verification and stale-output rejection are present. Actual Wan2.2 model files, GPU execution, optional packages and external binaries remain operator-controlled environment concerns and are intentionally not CI requirements.
- Continue reviewing the explicit execution path only for concrete reproducible safety/integrity gaps; do not add infrastructure merely to create activity.
- Continue fresh cross-category trend/evidence research when it materially improves creative coverage; do not collapse discovery into AI/tech only.
- RSSHub remains optional until an operator-controlled `RSSHUB_BASE_URL` is explicitly available.

## Next actions

1. Finish PR #1 accumulated diff/contract closure review; keep the PR draft until closure criteria are reviewed against exact-head CI.
2. Review the explicit `video-run --execute` path for remaining concrete reproducible safety/integrity gaps; add RED → GREEN contracts only where a real gap exists.
3. Reconcile PR #1 completion text with the now-implemented fresh-output guarantee in addition to MoviePy/headless execution, representative video-plan archive and dry-run project-tree safety, then keep exact-head CI green.
4. Keep PR draft until Foundation closure criteria are reviewed; do not mark ready solely because the video adapter is green.
5. After Foundation v0.1, add the lightweight project-bootstrap template/command for charter/status/skill recovery.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
