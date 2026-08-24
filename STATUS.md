# Hottop Status

Last updated: 2026-08-24 17:38 +08:00
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
- **Roughness is not universal.** `VideoProductionConfig.roughness_score` now makes intentional surface polish explicit on a 0–100 scale. High values may embrace controlled low-budget artifacts; cinematic/film hotspots use lower values so faces, costumes, lighting and camera work stay presentable.
- `config/video/anti-polish-direct.yml`: unattended headless profile, `style_profile=anti-polish`, `roughness_score=78`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-meme-direct.yml`: presentable film-meme profile, `style_profile=cinematic`, `roughness_score=28`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/anti-polish-short.yml` keeps Motion Canvas as an optional advanced vector-motion / interactive-preview path.
- `hottop video-plan <render-v2.json> --config ...` remains planning-only. `hottop video-run <render-v2.json> --config ... --output-dir ...` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.
- Execute mode requires fresh non-empty stage outputs and removes partial output from a failed external stage before raising. Stale/corrupt half-files cannot satisfy success.

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

- Earlier provider-neutral video planning, `video-doctor`, structured command specs, MoviePy/headless execution, Motion Canvas project-tree safety, stage-output verification and fresh-output safety were introduced RED-first and verified on Python 3.11 / 3.12; prior exact-head run 895 was green before the audio/style increment.
- The new audio/style work was introduced RED-first through `tests/test_video_audio_pipeline.py`, `tests/test_video_style_profiles.py`, and `tests/test_odyssey_video_archive.py`.
- During RED, CI also exposed a concrete failed-stage cleanup gap; `src/hottop/video_execution.py` now removes a partial output before raising on a nonzero stage result.
- Exact branch head `3eb8055d5ddefb106b2a284e39d0613914613f4b` passed CI run **933** on both Python **3.11** and **3.12**; Ruff and pytest succeeded in both jobs.
- `PROJECT.md` and this STATUS were then synchronized with the style-routed/audio-first architecture. Re-verify exact head after remaining skill/PR synchronization before final Foundation closure claims.

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

- Persist `roughness_score` and first-class voice/music/SFX rules in the reusable creative skill and PR summary.
- Re-run exact-head CI after status/skill/PR synchronization.
- Next architecture increment: provider-neutral external/cloud generation adapter contract (for example a configured ComfyUI endpoint) that preserves the same `render.v2 → video-plan → video-run` semantics. It must remain fail-closed and must not silently upload assets, use credentials or incur paid usage.
- After the adapter contract exists, evaluate current video backends for style/continuity fit rather than hard-coding one model for every hotspot.
- Foundation v0.1 accumulated PR diff / production-contract closure review continues.

## Next actions

1. Update the reusable creative skill with style-routed roughness and first-class audio production rules.
2. Synchronize PR #1 body and verify the resulting exact head on Python 3.11/3.12.
3. Add an explicit external/cloud video adapter configuration + readiness contract; no real paid/cloud invocation without operator-controlled endpoint/credentials and an allowed cost boundary.
4. Add a higher-quality voice/music adapter interface while retaining the deterministic local audio fallback.
5. Continue Foundation closure review; keep PR draft until closure criteria are checked against exact-head CI.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
