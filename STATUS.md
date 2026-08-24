# Hottop Status

Last updated: 2026-08-25 00:58 +08:00
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

- **`ZERO_COST_MODE=true` is the preferred unattended generation policy.** Hottop reserves free/shared or operator-owned GPU capacity for high-value generative shots while retaining deterministic MoviePy/FFmpeg/audio production for the rest.
- `generation_backend: zero-cost-router` is implemented with `ZeroCostConfig`: `allow_paid_fallback` is literally constrained to `false`, candidates require `cost_per_unit: 0`, attempts are bounded, and free-route exhaustion never consults a paid backend.
- `src/hottop/video_hf_zerogpu.py` implements Hugging Face ZeroGPU Gradio submit/poll/download with optional environment-only token lookup, SSE terminal handling, timeout/error classification and atomic `.part` output replacement.
- **Rights-safe reference I2V is end-to-end on the normal zero-cost runtime for the validated LTX 2.3 profile.** `VideoReference` carries a local reference locator plus explicit rights mode (`generated-original` or `user-provided-rights-cleared`) from `CreativeRenderFrame` → `hottop.video-plan.v1` → structured `video-run` command → `hottop.video_zero_cost` → `HfZeroGpuRequest`. Missing rights metadata, remote/data locators and unsupported profiles fail locally before upload.
- `video-run` preflights every zero-cost reference locator before any external stage is spawned. Missing local reference files make dry-run readiness false and make explicit `--execute` fail closed before consuming free GPU capacity or uploading anything.
- `src/hottop/video_quality.py` deterministically inspects generated MP4s with ffprobe/ffmpeg: video stream, terminal-frame decode, sampled grayscale frame delta and duplicate-frame ratio.
- **Quality-gated failover is wired into the free router.** A bad/duplicate-heavy candidate output is deleted, converted to retryable `zero_cost_quality_rejected`, and the next configured free candidate may run. Only a quality-passing fresh artifact is accepted.
- **All-free-routes exhaustion has an explicit non-generative degradation contract.** Deterministic reference-motion fallback is disabled by default, may run only when explicitly enabled and a rights-safe local reference exists, and is recorded as `artifact_kind=deterministic-non-generative`, `backend=deterministic-reference-motion`, `degraded_from=zero-cost-router`, `degradation_reason=zero_cost_routes_exhausted`. It is never reported as AI-generated footage.
- **Zero-cost artifact provenance is verified before composition and bound to exact bytes.** The manifest must declare `planned_generation_backend=zero-cost-router`; AI-generated shot backends must be IDs from the currently configured cost-zero candidate set; deterministic fallback is accepted only when explicitly enabled and only with the canonical reference-motion backend/degradation metadata. Each accepted shot manifest also records SHA-256 + byte size, and validation recomputes both from the MP4 instead of trusting a pathname alone.
- **MoviePy re-verifies generated shot bytes immediately before consuming them.** `verify_moviepy_shot_artifacts()` re-opens each `shot-XXX.artifact.json`, binds shot index + path, and recomputes SHA-256 + size so a generated file replaced after the earlier execution-stage check fails closed before composition.
- `config/video/cinematic-zero-cost.yml` is the first production profile for this path: cinematic roughness 28, HF ZeroGPU candidate list, bounded quality gate, local `espeak` dialogue + synthetic music + procedural SFX, MoviePy composition and FFmpeg finalization. Public Space availability is not treated as guaranteed.
- `docs/integrations/zero-cost-video-radar.md` records the admission policy for mature projects. Code license and model/weights license are always reviewed separately; stars/demos alone do not qualify a backend.
- Current watchlist: Wan2.2 for operator-controlled local generation; FramePack for future low-VRAM/reference I2V isolation; FastVideo for future self-hosted acceleration; ViMax/Toonflow for planning/provider architecture ideas; OpenMontage architecture only because its code is AGPL; RIFE/Real-ESRGAN only after a measurable post-processing gap exists.

## Style-routed video path

- **Anti-Polish / Controlled Badness** remains a durable selectable strategy: `low production feel + high comedy control`. Rough/cheap 3D, simple materials, awkward motion, deadpan acting, crude Foley and cheap-sounding music may be intentional; character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety and rights safety remain hard requirements.
- **Roughness is not universal.** `VideoProductionConfig.roughness_score` makes intentional surface polish explicit on a 0–100 scale. High values may embrace controlled low-budget artifacts; cinematic/film hotspots use lower values so faces, costumes, lighting and camera work stay presentable.
- `config/video/anti-polish-direct.yml`: unattended headless profile, `style_profile=anti-polish`, `roughness_score=78`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-meme-direct.yml`: presentable film-meme profile, `style_profile=cinematic`, `roughness_score=28`, Wan2.2 optional generation → MoviePy → FFmpeg.
- `config/video/cinematic-zero-cost.yml`: presentable free-only profile, `style_profile=cinematic`, `roughness_score=28`, bounded HF ZeroGPU route → quality gate → MoviePy → FFmpeg.
- **The bundled `video/motion-canvas` project is planning/interactive-preview only.** Its `render` script prepares `src/generated-plan.ts` and explicitly does not spawn a renderer. `config/video/anti-polish-short.yml` therefore points explicit execution at a separate operator-provided `video/motion-canvas-executor` project. If that executor is absent, `video-doctor`/`video-run --execute` fail readiness before spawning npm. MoviePy remains the unattended compositor default.
- `hottop video-plan <render-v2.json> --config ...` remains planning-only. `hottop video-run <render-v2.json> --config ... --output-dir ...` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.
- Execute mode requires fresh non-empty stage outputs and removes residual output both when an external stage returns failure and when a nominally successful stage leaves an empty/invalid expected artifact. Stale/corrupt/zero-byte half-files cannot satisfy success or remain behind as misleading workspace artifacts.
- **Final delivery is media-verified, not merely file-verified.** After configured FFmpeg finalization returns success, `video-run --execute` runs ffprobe against the fresh output and requires positive duration plus the configured video codec, pixel format and audio codec (for the default MP4 path: H.264 / yuv420p / AAC). A non-media or incompatible final artifact is deleted and execution fails closed instead of reporting `executed=True`.

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
- MoviePy headless composition mixes shot audio, generated dialogue WAVs, original synthetic BGM and procedural SFX before FFmpeg H.264/AAC/yuv420p/fast-start finalization.
- External/cloud voice/music backends stay fail-closed until explicitly configured. No paid API, credential use, upload or commercial-license activation is automatic.

## Representative video sources

- `examples/video/inkclaw-cow-snake.render.json` — high-roughness original Anti-Polish story source; its derived `hottop.video-plan.v1` archive remains a snapshot rather than a second creative source of truth.
- `examples/video/inkclaw-odyssey-witch-pigs.render.json` — lower-roughness cinematic mythic meme source: sailors code/eat in one original witch banquet hall, an unmistakably satirical magical obstruction turns them into pigs, an original returning-sailor hero uses InkClawAgent to break the curse, and `不用部署 / 开发零门槛 / Free Token 入门` appear as story consequences rather than glossy feature cards.
- The Odyssey source explicitly excludes copied film frames, actor likenesses, official character designs, source footage and commercial soundtrack. The `某包 / Work巴迪?` prop is framed only as magical satire/metaphor, not as a factual defect claim.
- `examples/video/hottop-zero-cost-reference-i2v.render.json` — representative rights-safe free-I2V source using the repository-generated `assets/generated-original/hottop-signal-orb.ppm` reference in every shot. The PPM is original text-authored pixel data with no third-party pixels; each frame carries `rights=generated-original`, motion continuity is required, destination CTA is disabled, and the source plans through `config/video/cinematic-zero-cost.yml` to `zero-cost-router`.

## Verification evidence

- Earlier provider-neutral video planning, `video-doctor`, structured command specs, MoviePy/headless execution, Motion Canvas project-tree safety, stage-output verification and fresh-output safety were introduced RED-first and verified on Python 3.11 / 3.12.
- Audio/style work was introduced RED-first through `tests/test_video_audio_pipeline.py`, `tests/test_video_style_profiles.py`, and `tests/test_odyssey_video_archive.py`; exact head `3eb8055d5ddefb106b2a284e39d0613914613f4b` passed CI run 933 on both Python versions before doctrine synchronization.
- The Comfy API v2 adapter began with RED contract `40c9df0d18da80e22a7edaeb6f2ea55cd287a79c`; exact head `f174e24a0d9b960fc3c0df70941527530cbaf89c` passed CI run 951 on Python 3.11 / 3.12.
- Zero-cost quality integration began with RED `46f93c45b9baf92e6d506a3ec2f24c6fdcc69fc3`; CI run **1000** passed Ruff and produced exactly **1 failed / 305 passed**, proving the first bad free candidate was still accepted. GREEN `0dd18b546b608c5a34a2b5c0c41728a0f5d53e7e` wired `inspect_video_quality` into failover; CI run **1002** passed Ruff + full pytest on Python 3.11 / 3.12.
- Zero-cost production profile/radar/doctrine began with normalized RED `c4906602b9fc143950bdd215b7f910998593c8b2`; CI run **1006** passed Ruff and produced exactly **2 failed / 306 passed**, both missing-artifact contracts. After adding the profile, radar, `PROJECT.md` decision and skill rule, exact head `dd55e31b9b6cf3b6e3700745734d2afe6886c86d` passed CI run **1014** on Python 3.11 / 3.12.
- Reference-I2V provider safety began with RED `0ca588fb028ac0e929aa6d1c1bf1d360b966135c`; CI run **1018** passed Ruff and produced exactly **2 failed / 308 passed**, proving missing reference-rights validation and missing Gradio upload. GREEN `30e0d716251825475def8d335fcf7afc02fdd809` added explicit rights modes plus LTX 2.3 upload/FileData handling; CI run **1020** passed Ruff + full pytest on Python 3.11 / 3.12.
- Provider-neutral reference propagation is covered by `tests/test_video_reference_runtime.py`: local rights-safe references survive `render.v2 → video-plan → compositor manifest → zero-cost runtime args → HfZeroGpuRequest`; baseline exact head `2cf101b5e1314d1900635f7620b1e00530a55607` passed CI run **1040**.
- Full-plan reference preflight began with RED `0d4c5644ea715c4f1d79208a1c421fcbe15376c8`; CI run **1042** passed Ruff and produced exactly **1 failed / 316 passed**, proving a missing reference still allowed the first external generation command to spawn. GREEN `31a819cf815bb12deb7f747d9c5c8bbb5d29d36f` added zero-cost reference readiness to `video-run`; CI run **1044** passed the full suite.
- Planned-backend artifact binding began with RED `5d639e5af90759154451770b99a3c4ff9c7d27e2`; CI run **1082** passed Ruff and produced exactly **1 failed / 325 passed**, proving a zero-cost execution could accept a manifest claiming another planned backend. GREEN `9232de8f34756e1647894274960108b3389cadac` bound the manifest to `zero-cost-router`; CI run **1084** passed.
- Actual free-candidate binding began with RED `293ba4de9624fb9ccfbf9e91a4db42468b196440`; CI run **1086** passed Ruff and produced exactly **1 failed / 326 passed**, proving a manifest could claim an unconfigured provider. GREEN `afff51734b56895dcb35559d3e3c62ca3bad4600` requires AI artifact backends to belong to the configured cost-zero candidate IDs; CI run **1088** passed.
- Deterministic-fallback provenance binding began with RED `ea63ccea36c89d97c802e4e96c1f97b897c65897`; CI run **1090** passed Ruff and produced exactly **2 failed / 327 passed**, proving deterministic artifacts were accepted when fallback was disabled and arbitrary deterministic backends were accepted. GREEN `406175a940491d1ed9b6a803145b1b56e2849be9` requires fallback to be explicitly enabled and binds `backend=deterministic-reference-motion`, `degraded_from=zero-cost-router`, and `degradation_reason=zero_cost_routes_exhausted`; CI run **1092** passed on Python 3.11 / 3.12.
- Exact-byte provenance and immediate MoviePy consumption verification are closed: shot manifests record/recompute SHA-256 + size, and exact head `25b8742f82bcd2a18fe7f43dc3ecd4228a8ca6eb` passed CI run **1114** after `verify_moviepy_shot_artifacts()` was wired directly into composition.
- The representative reference-I2V archive contract reached a clean RED at `e38483a96ed45e3853ef940331e9880063759836`: CI run **1124** passed Ruff and produced exactly **1 failed / 332 passed** because the rights-safe source archive did not yet exist. GREEN `669f5357cf327976f759f1d05d33d3314ad99863` added only the repository-generated PPM reference plus its `hottop.render.v2` archive; CI run **1128** passed on Python 3.11 / 3.12.
- Motion Canvas execution-boundary review reached a clean RED at `f69a42f42bc57a603cc3697d2f19dfbfe862f282`: CI run **1132** passed Ruff and produced exactly **1 failed / 333 passed**, proving the bundled planning-only scaffold was reported `ready=True`. The GREEN separates the bundled scaffold from execution by pointing `anti-polish-short` at an operator-provided `video/motion-canvas-executor`; intermediate run **1135** exposed only the obsolete structured-command cwd assertion, and final exact head `5fa636e2cc7a858ee89b91aac1430e20b8ab8024` passed CI run **1138** on Python 3.11 / 3.12.
- Final-delivery media integrity began with RED `5377eb323afda20bc2a097a0e51544aa0298a253`: CI run **1142** passed Ruff and produced exactly **1 failed / 334 passed**, proving FFmpeg could return 0 and leave non-media bytes that were still reported as a successful final artifact. After correcting the verifier's canonical `FFmpegConfig` type name, GREEN exact head `7b131c1acdd80d07dabb95eed0b86cd0433768b9` passed CI run **1147** on Python 3.11 / 3.12. Finalized output now must pass ffprobe stream/codec/pixel-format/duration checks before execution is reported successful.
- Successful-stage residue cleanup began with RED `02255121a3f43b708ab1ba1096a9d6a76b0002ac`: CI run **1152** passed Ruff and produced exactly **1 failed / 335 passed**, proving a stage could return 0, leave a zero-byte expected output, correctly fail verification, but still leave that invalid file behind. GREEN `d40feb28e401be86d260569aedb26132799ecb1d` deletes an invalid file inside `_verify_stage_output()` before raising; CI run **1154** passed Ruff + full pytest on Python 3.11 / 3.12.

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
- Reference propagation, full-plan reference preflight, explicit deterministic degradation, backend-level artifact provenance, exact-byte shot binding, immediate MoviePy pre-consumption verification, successful-stage invalid-output cleanup, representative generated-original reference-I2V archive, and final-delivery media verification are closed for the normal unattended path.
- The bundled Motion Canvas project is now explicitly planning/preview-only and cannot satisfy execution readiness by itself. A future operator-provided Motion Canvas executor must actually emit the composite MP4 and should receive the same immediate pre-consumption byte-verification scrutiny before it can become a trusted execution path.
- Higher-quality voice/music adapters remain useful but must not displace stricter zero-cost video consistency/runtime work or introduce hidden cloud cost.

## Next actions

1. Continue Foundation accumulated diff / production-contract closure review and repair only concrete regressions, dead assumptions, or evidence/safety/integrity gaps. MoviePy remains the unattended compositor default.
2. If a real operator-provided Motion Canvas executor is introduced, require it to emit the expected composite artifact and add equivalent generated-shot byte verification at the consumption boundary before declaring that path trusted.
3. Benchmark FramePack only when operator-controlled GPU/runtime is available; never invoke its automatic >30GB model download from unattended Hottop/CI. Keep FastVideo as a future acceleration candidate until a measurable self-hosted performance gap exists.
4. Run a real free-route reference-I2V smoke only when a currently available public endpoint and its code/weights license gates are verified for the intended use; never consume paid credits or silently fall back to paid inference.
5. Keep PR #1 draft until exact-head CI and accumulated Foundation contract review are complete.

## Constraints

- No secrets, cookies or browser profiles in Git/CI logs.
- No autonomous model downloads, GPU provisioning, paid API calls, automatic overage or commercial-license activation.
- No unsupported factual superiority claims or invented competitor defects.
- No direct reproduction of actor likenesses, exact film frames, official posters, protected character designs, proprietary UI, logos, distinctive trade dress, copyrighted soundtrack or copied ad layouts without rights-cleared user assets.
- Preserve broad cultural/medium recognition while building original staging and assets.
