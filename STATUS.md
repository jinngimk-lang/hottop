# Hottop Status

Last updated: 2026-08-24 18:05 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1
PR: #1 — open, draft, mergeable

## Current foundation state

- Hottop is a cross-category hot-topic brand creative engine, not InkClawAgent-only, AI-only, static-only or four-panel-only. `PROJECT.md` and reusable skills are the durable doctrine.
- Core trend discovery/enrichment, dedupe/ranking, evidence-aware comparison, adaptive intake, project/platform/style routing, category reframing, bridge search, Creative Review/contextual review, orchestration, flexible `CreativeConcept`, provider-neutral `hottop.render.v2`, config-driven `hottop.video-plan.v1`, and dry-run-first `video-run` are implemented.
- Social/hotspot creative is ad-light by default: no in-asset URL/QR/hard CTA for meme/brand-memory work unless conversion intent explicitly overrides it.
- Motion-native ideas preserve character/scene/action continuity instead of becoming slideshow-like still sequences. Product benefits appear first as dialogue, action or visible consequences.
- Provenance-first visual references remain grammar-only; protected film frames, actor likenesses, soundtrack, character designs, proprietary UI and copied layouts are not default generation inputs.

## Style-routed video path

- **Anti-Polish / Controlled Badness** remains a durable selectable strategy: `low production feel + high comedy control`. Rough/cheap 3D, simple materials, awkward motion, deadpan acting, crude Foley and cheap-sounding music may be intentional; character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety and rights safety remain hard requirements.
- **Roughness is not universal.** `VideoProductionConfig.roughness_score` makes intentional surface polish explicit on a 0–100 scale. High values may embrace controlled low-budget artifacts; cinematic/film hotspots use lower values so faces, costumes, lighting and camera work stay presentable.
- `config/video/anti-polish-direct.yml`: unattended headless profile, `style_profile=anti-polish`, `roughness_score=78`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-meme-direct.yml`: presentable film-meme profile, `style_profile=cinematic`, `roughness_score=28`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/anti-polish-short.yml` keeps Motion Canvas as an optional advanced vector-motion / interactive-preview path.
- `hottop video-plan <render-v2.json> --config ...` remains planning-only. `hottop video-run <render-v2.json> --config ... --output-dir ...` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.
- Execute mode requires fresh non-empty stage outputs and removes partial output from a failed external stage before raising. Stale/corrupt half-files cannot satisfy success.

## Provider-neutral generation adapters

- Wan2.2 remains the operator-controlled local/open-source generation route; Hottop never downloads weights or provisions GPU resources automatically.
- `comfy-api-v2` is now an explicit optional remote/self-hosted generation adapter behind the same `render.v2 → video-plan → video-run` contract.
- Comfy adapter configuration contains endpoint, workflow path, prompt node/input mapping, token **environment-variable name**, polling interval and timeout. Secrets themselves are never written into plans/runtime command arguments.
- `video-doctor`/`inspect_video_environment()` fail closed when the workflow JSON or configured token environment variable is missing.
- Dry-run emits structured `python -m hottop.video_comfy_api ...` generation commands using `shell=False`; actual HTTP submission happens only under explicit `video-run --execute` after readiness passes.
- The adapter sends configured workflow JSON plus generated prompt/job metadata; it does not silently upload arbitrary local assets, create credentials or authorize paid usage. Operator endpoint/cost policy remains external to Hottop.

## Audio is now first-class

- `CreativeRenderFrame` supports `speaker` and `delivery`, so character role and performance direction survive from creative source into production.
- `VideoProductionConfig.audio` carries explicit **voice**, **music**, and **SFX/Foley** backends/profiles, Mandarin rate/language settings, dialogue ducking, and `original_music_only`.
- `hottop.video-plan.v1` carries an `audio_profile`; dialogue cues preserve character, delivery and voice profile alongside BGM/Foley timing.
- Local executable baseline is deliberately dependency-light and free: `espeak` for Mandarin dialogue + Hottop-generated original synthetic music + deterministic procedural SFX/Foley. This baseline is a fallback/testable execution path, not the quality ceiling.
- `video-run` runtime order is generation → audio → compositor → finalization. Dry-run creates both `shots/` and `audio/` workspaces without spawning subprocesses.
- MoviePy headless composition now mixes shot audio, generated dialogue WAVs, original synthetic BGM and procedural SFX before FFmpeg H.264/AAC/yuv420p/fast-start finalization.
- External/cloud voice/music backends stay fail-closed until explicitly configured. No paid API, credential use, upload or commercial-license activation is automatic.

## Representative video sources

- `examples/video/inkclaw-cow-snake.render.json` — high-roughness original Anti-Polish story source; its derived `hottop.video-plan.v1` archive remains a snapshot rather than a second creative source of truth.
- `examples/video/inkclaw-odyssey-witch-pigs.render.json` — lower-roughness cinematic mythic meme source: sailors code/eat in one original witch banquet hall, an unmistakably satirical magical obstruction turns them into pigs, an original returning-sailor hero uses InkClawAgent to break the curse, and `不用部署 / 开发零门槛 / Free Token 入门` appear as story consequences rather than glossy feature cards.
- The Odyssey source explicitly excludes copied film frames, actor likenesses, official character designs, source footage and commercial soundtrack. The `某包 / Work巴迪?` prop is framed only as magical satire/metaphor, not as a factual defect claim.

## Verification evidence

- Earlier provider-neutral video planning, `video-doctor`, structured command specs, MoviePy/headless execution, Motion Canvas project-tree safety, stage-output verification and fresh-output safety were introduced RED-first and verified on Python 3.11 / 3.12.
- Audio/style work was introduced RED-first through `tests/test_video_audio_pipeline.py`, `tests/test_video_style_profiles.py`, and `tests/test_odyssey_video_archive.py`; exact head `3eb8055d5ddefb106b2a284e39d0613914613f4b` passed CI run 933 on both Python versions before doctrine synchronization.
- The Comfy API v2 adapter began with RED contract `40c9df0d18da80e22a7edaeb6f2ea55cd287a79c`. CI run 941 first exposed only a Ruff import-order issue before pytest could execute; after implementation and normalization, exact head `f174e24a0d9b960fc3c0df70941527530cbaf89c` passed CI run **951** on Python **3.11** and **3.12**, with Ruff and full pytest successful in both jobs.
- The Comfy tests verify environment-only credential reference, fail-closed missing-token readiness, workflow prompt injection, job polling and successful video download without embedding the secret in dry-run commands.

## Current creative doctrine

- Reframe before optimize: identify `category_default`, test constraint deletion, derive `new_competition_axis`.
- Natural bridge before logo: search shape/material, action/motion, role, function, emotion/ritual and language/symbol.
- Format follows the idea; medium follows the hotspot; motion follows timing/action/dialogue/sound when those carry recognition.
- Roughness follows the idea too: Anti-Polish is differentiated, not universal. A cinematic meme may be weird without looking broken.
- Product benefits belong inside the joke as consequences; do not replace the joke with feature cards.
- Named competitor negatives require evidence or unmistakable satire; otherwise use a generic proxy or old category assumption.
- Creative Review remains the hard gate; contextual fit only ranks concepts that already pass.
- References teach grammar, not pixels.

## In progress

- Synchronize PR #1 summary with the now-green optional Comfy API v2 adapter.
- Next architecture increment: a higher-quality provider-neutral voice/music adapter interface while retaining the deterministic local audio fallback and the same explicit credential/cost boundaries.
- Evaluate current video backends for style/continuity fit rather than hard-coding one model for every hotspot; keep Wan2.2 and Comfy adapters selectable rather than universal.
- Foundation v0.1 accumulated PR diff / production-contract closure review continues.

## Next actions

1. Synchronize PR #1 body with the green Comfy API v2 optional generation adapter and exact-head CI 951 evidence.
2. Add a higher-quality voice/music adapter interface while retaining `espeak` + synthetic/procedural local fallback and fail-closed credential/cost behavior.
3. Add targeted contracts for adapter output/metadata integrity only when a concrete gap is reproducible; do not add generic cloud infrastructure for its own sake.
4. Continue Foundation closure review; keep PR draft until closure criteria are checked against exact-head CI.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
