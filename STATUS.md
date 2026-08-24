# Hottop Status

Last updated: 2026-08-24 12:08 +08:00
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

- **Anti-Polish / Controlled Badness** is now a durable selectable Hottop strategy: `low production feel + high comedy control`. Rough/cheap 3D, simple materials, awkward motion, deadpan acting, crude Foley and cheap-sounding music may be intentional; character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety and rights safety remain hard requirements.
- Durable rule: **Do not polish the badness away; make the badness precise.** Product UI/benefits should remain native to the rough world instead of switching into generic glossy blue-purple AI-ad aesthetics.
- Config profile: `config/video/anti-polish-short.yml` — 720×1280, 24fps, 12s, `wan22-ti2v-5b` generation route, Motion Canvas compositor, FFmpeg final encoder, no URL/QR, explicit dialogue/Foley/BGM rules and continuity transitions.
- `src/hottop/video_production.py` defines `VideoProductionConfig`, `VideoProductionPlan`, ordered shots, continuity instructions, audio cues, Wan2.2 command plans, Motion Canvas manifest and FFmpeg H.264/AAC/yuv420p/fast-start finalization contract.
- `hottop.video-plan.v1` now preserves both the legacy human-readable command fields and trusted structured command specs (`program`, `args`, `cwd`, `stage`) for generation, compositor and finalization. A future executor therefore does not need to parse arbitrary shell strings.
- `hottop video-plan <render-v2.json> --config config/video/anti-polish-short.yml [--output plan.json]` emits provider-neutral `hottop.video-plan.v1`. It is planning-only and does not execute external tools.
- `src/hottop/video_execution.py` defines fail-closed local readiness inspection for Wan2.2 repository/model files, Node/npm + Motion Canvas project metadata, and FFmpeg. It never installs packages, downloads models, provisions GPU, or invokes paid services.
- `hottop video-doctor --config ... [--project-root ...] [--output ...]` exposes that readiness inspection without executing external commands.
- Upstreams are pinned in `integrations/versions.yml`: Wan2.2 as optional Apache-2.0 local shot generation; Motion Canvas as MIT deterministic compositor; FFmpeg as external compatibility encoder with build-dependent licensing; Remotion remains disabled-by-default and requires operator license review before use.
- Design/spec: `docs/superpowers/specs/2026-08-24-config-driven-video-production-design.md`.
- Planning implementation: `docs/superpowers/plans/2026-08-24-config-driven-video-production.md`.
- Safe execution follow-on: `docs/superpowers/plans/2026-08-24-video-execution-adapter.md`.

## Verification evidence

- Video-production contract was introduced RED-first: Ruff was corrected, then CI failed specifically because `hottop.video_production` did not exist.
- Implementation head `11b4ce86932558d810478abce2a115d25d141609` passed exact CI run 769 on Python 3.11 and 3.12.
- CLI contract then failed with exactly one missing `video-plan` command while 260 existing tests passed; implementation head `3dfdd25e795954f99a15d939eafced861211bccb` passed exact CI run 773.
- Durable-doctrine contract then failed with exactly two missing persistence/upstream-pin tests while 261 existing tests passed; doctrine/integration head `f6c5ed7a1699831a6ee2ab8e696e0811b2794986` passed exact CI run 781 on Python 3.11 and 3.12.
- Safe readiness inspection landed before CLI exposure; recovery baseline head `ce08fceadbfe2a0b14db22dd94bda64da97e78af` passed exact CI run 793.
- `video-doctor` was introduced RED-first at `70d5f7a03c11e4e617292c9c4a42d0bff8acda52`: Ruff passed and pytest failed exactly once because the command was missing (`1 failed / 265 passed`). Minimal CLI implementation head `fc90f46d3ba4f548bddecec1e4a7ba145d67e58c` passed exact CI run 797 on Python 3.11 and 3.12.
- Structured trusted command specs were introduced RED-first at `c2a5b81652e4b736bd340f04b7327b379bfd3af5`: Ruff passed and pytest failed exactly once because `VideoProductionPlan` lacked the new structured fields (`1 failed / 266 passed`). Implementation head `9bfece07230e4de636b42448832735ab7742f457` passed exact CI run 803 on Python 3.11 and 3.12.

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

- Foundation v0.1 closure review continues across the accumulated PR diff.
- Config-driven video planning, structured trusted command specs and fail-closed readiness inspection are implemented. Actual local GPU generation, Motion Canvas rendering and FFmpeg invocation remain intentionally operator/execution-environment concerns rather than CI requirements.
- The safe execution adapter is still incomplete: Motion Canvas scaffold and opt-in `video-run --execute` remain to be added. No external process should be spawned until those contracts are green.
- Continue fresh cross-category trend/evidence research when it materially improves creative coverage; do not collapse discovery into AI/tech only.
- RSSHub remains optional until an operator-controlled `RSSHUB_BASE_URL` is explicitly available.

## Next actions

1. Finish PR #1 accumulated diff/contract review; PR completion text is refreshed for the motion/video planning + doctor path, but keep the PR draft until closure criteria are reviewed against exact-head CI.
2. Add the small pinned Motion Canvas project scaffold that consumes `hottop-video-plan.json`; CI should validate files/contracts only, not install npm packages or render.
3. Add a representative `hottop.video-plan.v1` archive for the original InkClawAgent “cow / snake / mother” Anti-Polish story, with no protected source footage or soundtrack.
4. Add `video-run` dry-run by default, then explicit `--execute` process spawning with `shell=False`, fixed stage order, explicit cwd and fail-closed readiness. Never auto-install/download/provision anything.
5. Keep PR draft until Foundation closure criteria are reviewed against exact-head CI.
6. After Foundation v0.1, add the lightweight project-bootstrap template/command for charter/status/skill recovery.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
