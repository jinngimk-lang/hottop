# Hottop Status

Last updated: 2026-08-24 11:38 +08:00
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
- New config profile: `config/video/anti-polish-short.yml` — 720×1280, 24fps, 12s, `wan22-ti2v-5b` generation route, Motion Canvas compositor, FFmpeg final encoder, no URL/QR, explicit dialogue/Foley/BGM rules and continuity transitions.
- New module: `src/hottop/video_production.py` defines `VideoProductionConfig`, `VideoProductionPlan`, ordered shots, continuity instructions, audio cues, Wan2.2 command plans, Motion Canvas manifest and FFmpeg H.264/AAC/yuv420p/fast-start finalization contract.
- New CLI: `hottop video-plan <render-v2.json> --config config/video/anti-polish-short.yml [--output plan.json]` emits `hottop.video-plan.v1`. It is planning-only: it does not download models, require GPU/Node/FFmpeg in CI, invoke paid APIs or execute external commands silently.
- Upstreams are pinned in `integrations/versions.yml`: Wan2.2 as optional Apache-2.0 local shot generation; Motion Canvas as MIT deterministic compositor; FFmpeg as external compatibility encoder with build-dependent licensing; Remotion remains disabled-by-default and requires operator license review before use.
- Design/spec: `docs/superpowers/specs/2026-08-24-config-driven-video-production-design.md`.
- Implementation plan: `docs/superpowers/plans/2026-08-24-config-driven-video-production.md`.

## Verification evidence

- Video-production contract was introduced RED-first: Ruff was corrected, then CI failed specifically because `hottop.video_production` did not exist.
- Implementation head `11b4ce86932558d810478abce2a115d25d141609` passed exact CI run 769 on Python 3.11 and 3.12.
- CLI contract then failed with exactly one missing `video-plan` command while 260 existing tests passed; implementation head `3dfdd25e795954f99a15d939eafced861211bccb` passed exact CI run 773.
- Durable-doctrine contract then failed with exactly two missing persistence/upstream-pin tests while 261 existing tests passed; doctrine/integration head `f6c5ed7a1699831a6ee2ab8e696e0811b2794986` passed exact CI run 781 on Python 3.11 and 3.12.

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

- Foundation v0.1 closure review continues across the accumulated PR diff. The config-driven video **planning** path is implemented; actual local GPU model execution, Motion Canvas project scaffolding and FFmpeg invocation remain intentionally operator/execution-environment concerns rather than CI requirements.
- The next useful video layer is an execution adapter that consumes `hottop.video-plan.v1` without weakening provider neutrality or silently installing/downloading heavy dependencies. It should be added only with deterministic dry-run/availability checks first.
- Continue fresh cross-category trend/evidence research when it materially improves creative coverage; do not collapse discovery into AI/tech only.
- RSSHub remains optional until an operator-controlled `RSSHUB_BASE_URL` is explicitly available.

## Next actions

1. Finish PR #1 accumulated diff/contract review and refresh the PR completion text for the now-implemented motion/video planning path.
2. Add a dry-run/doctor layer for video execution availability (Wan2.2 model path, Motion Canvas project/runtime, FFmpeg binary) before any command is allowed to execute external tools.
3. Add a representative `hottop.video-plan.v1` archive for the InkClawAgent “cow / snake / mother” Anti-Polish story using original staging and no protected source footage.
4. Only after the dry-run contract is green, implement an opt-in executor that can generate shot jobs, compose timeline/audio and encode MP4/GIF in an operator-controlled environment.
5. Keep PR draft until Foundation closure criteria are reviewed against exact-head CI.
6. After Foundation v0.1, add the lightweight project-bootstrap template/command for charter/status/skill recovery.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
