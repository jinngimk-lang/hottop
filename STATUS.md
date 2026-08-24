# Hottop Status

Last updated: 2026-08-24 19:08 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1
PR: #1 — open, draft, mergeable

## Current foundation state

- Hottop is a cross-category hot-topic brand creative engine, not InkClawAgent-only, AI-only, static-only or four-panel-only. `PROJECT.md` and reusable skills are the durable doctrine.
- Core trend discovery/enrichment, dedupe/ranking, evidence-aware comparison, adaptive intake, project/platform/style routing, category reframing, bridge search, Creative Review/contextual review, orchestration, flexible `CreativeConcept`, provider-neutral `hottop.render.v2`, config-driven `hottop.video-plan.v1`, and dry-run-first `video-run` are implemented.
- Social/hotspot creative is ad-light by default: no in-asset URL/QR/hard CTA for meme/brand-memory work unless conversion intent explicitly overrides it.
- Motion-native ideas preserve character/scene/action continuity instead of becoming slideshow-like still sequences. Product benefits appear first as dialogue, action or visible consequences.
- Provenance-first visual references remain grammar-only; protected film frames, actor likenesses, soundtrack, character designs, proprietary UI and copied layouts are not default generation inputs.

## Zero-cost video path

- **`ZERO_COST_MODE=true` is now the preferred unattended generation policy.** Hottop reserves free/shared or operator-owned GPU capacity for high-value generative shots while retaining deterministic MoviePy/FFmpeg/audio production for the rest.
- `generation_backend: zero-cost-router` is implemented with `ZeroCostConfig`: `allow_paid_fallback` is literally constrained to `false`, candidates require `cost_per_unit: 0`, attempts are bounded, and free-route exhaustion never consults a paid backend.
- `src/hottop/video_hf_zerogpu.py` implements Hugging Face ZeroGPU Gradio submit/poll/download with optional environment-only token lookup, SSE terminal handling, timeout/error classification and atomic `.part` output replacement.
- `src/hottop/video_quality.py` deterministically inspects generated MP4s with ffprobe/ffmpeg: video stream, terminal-frame decode, sampled grayscale frame delta and duplicate-frame ratio.
- **Quality-gated failover is now wired into the free router.** A bad/duplicate-heavy candidate output is deleted, converted to retryable `zero_cost_quality_rejected`, and the next configured free candidate may run. Only a quality-passing fresh artifact is accepted.
- `config/video/cinematic-zero-cost.yml` is the first production profile for this path: cinematic roughness 28, HF ZeroGPU candidate list, bounded quality gate, local `espeak` dialogue + synthetic music + procedural SFX, MoviePy composition and FFmpeg finalization. Public Space availability is not treated as guaranteed.
- `docs/integrations/zero-cost-video-radar.md` records the admission policy for mature projects. Code license and model/weights license are always reviewed separately; stars/demos alone do not qualify a backend.
- Current watchlist: Wan2.2 for operator-controlled local generation; FramePack for future low-VRAM/reference I2V isolation; FastVideo for future self-hosted acceleration; ViMax/Toonflow for planning/provider architecture ideas; OpenMontage architecture only because its code is AGPL; RIFE/Real-ESRGAN only after a measurable post-processing gap exists.

## Style-routed video path

- **Anti-Polish / Controlled Badness** remains a durable selectable strategy: `low production feel + high comedy control`. Rough/cheap 3D, simple materials, awkward motion, deadpan acting, crude Foley and cheap-sounding music may be intentional; character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety and rights safety remain hard requirements.
- **Roughness is not universal.** `VideoProductionConfig.roughness_score` makes intentional surface polish explicit on a 0–100 scale. High values may embrace controlled low-budget artifacts; cinematic/film hotspots use lower values so faces, costumes, lighting and camera work stay presentable.
- `config/video/anti-polish-direct.yml`: unattended headless profile, `style_profile=anti-polish`, `roughness_score=78`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-meme-direct.yml`: presentable film-meme profile, `style_profile=cinematic`, `roughness_score=28`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-zero-cost.yml`: presentable free-only profile, `style_profile=cinematic`, `roughness_score=28`, bounded HF ZeroGPU route → quality gate → MoviePy → FFmpeg.
- `config/video/anti-polish-short.yml` keeps Motion Canvas as an optional advanced vector-motion / interactive-preview path.
- `hottop video-plan <render-v2.json> --config ...` remains planning-only. `hottop video-run <render-v2.json> --config ... --output-dir ...` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.
- Execute mode requires fresh non-empty stage outputs and removes partial output from a failed external stage before raising. Stale/corrupt half-files cannot satisfy success.

## Provider-neutral generation adapters

- Wan2.2 remains the operator-controlled local/open-source generation route; Hottop never downloads weights or provisions GPU resources automatically.
- `comfy-api-v2` remains an explicit optional remote/self-hosted generation adapter behind the same `render.v2 → video-plan → video-run` contract.
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
- The Comfy API v2 adapter began with RED contract `40c9df0d18da80e22a7edaeb6f2ea55cd287a79c`; exact head `f174e24a0d9b960fc3c0df70941527530cbaf89c` passed CI run 951 on Python 3.11 / 3.12.
- Zero-cost quality integration began with RED `46f93c45b9baf92e6d506a3ec2f24c6fdcc69fc3`; CI run **1000** passed Ruff and produced exactly **1 failed / 305 passed**, proving the first bad free candidate was still accepted. GREEN `0dd18b546b608c5a34a2b5c0c41728a0f5d53e7e` wired `inspect_video_quality` into failover; CI run **1002** passed Ruff + full pytest on Python 3.11 / 3.12.
- Zero-cost production profile/radar/doctrine began with normalized RED `c4906602b9fc143950bdd215b7f910998593c8b2`; CI run **1006** passed Ruff and produced exactly **2 failed / 306 passed**, both missing-artifact contracts (`cinematic-zero-cost.yml` and `zero-cost-video-radar.md`). After adding the profile, radar, `PROJECT.md` decision and skill rule, exact head `dd55e31b9b6cf3b6e3700745734d2afe6886c86d` passed CI run **1014** on Python 3.11 / 3.12.

## Current creative doctrine

- Reframe before optimize: identify `category_default`, test constraint deletion, derive `new_competition_axis`.
- Natural bridge before logo: search shape/material, action/motion, role, function, emotion/ritual and language/symbol.
- Format follows the idea; medium follows the hotspot; motion follows timing/action/dialogue/sound when those carry recognition.
- Roughness follows the idea too: Anti-Polish is differentiated, not universal. A cinematic meme may be weird without looking broken.
- Product benefits belong inside the joke as consequences; do not replace the joke with feature cards.
- Named competitor negatives require evidence or unmistakable satire; otherwise use a generic proxy or old category assumption.
- Creative Review remains the hard gate; contextual fit only ranks concepts that already pass.
- References teach grammar, not pixels.
- Zero-cost generation is hybrid, not magical unlimited compute: use free capacity selectively, reject bad artifacts, keep deterministic production alive, and never pay silently.

## In progress

- Foundation v0.1 accumulated PR diff / production-contract closure review continues.
- Next zero-cost capability gap: **reference-first I2V consistency**. The current HF adapter is text-to-video only even though the preferred architecture fixes a character/product keyframe before motion generation. Add this only through a rights-safe reference contract and isolated adapter path.
- After reference I2V, evaluate a clearly labeled deterministic degradation path for free-route exhaustion; never publish a mock placeholder as successful generative footage.
- Higher-quality voice/music adapters remain useful but must not displace the stricter zero-cost video consistency/runtime work or introduce hidden cloud cost.

## Next actions

1. Add a TDD-first reference-image contract for zero-cost/high-value I2V so a rights-cleared fixed character/product keyframe can survive into eligible free/local generation; preserve env-only credentials and no paid fallback.
2. Add a deterministic, explicitly labeled degradation strategy for all-free-routes-unavailable cases only after defining how the final artifact records that it is non-generative fallback footage.
3. Benchmark FramePack only when operator-controlled GPU/runtime is available; never invoke its automatic >30GB model download from unattended Hottop/CI. Keep FastVideo as a future acceleration candidate until a measurable self-hosted performance gap exists.
4. Continue Foundation closure review and keep PR draft until exact-head CI and accumulated contract review are complete.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls, automatic overage or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.