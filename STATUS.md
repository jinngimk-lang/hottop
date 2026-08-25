# Hottop Status

Last updated: 2026-08-25
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1 closure
PR: #1 — open, draft, mergeable at last fetch

> This file is the short-lived execution snapshot. `PROJECT.md` is the durable doctrine. For exact CI/head state, re-fetch the current PR/branch rather than trusting an embedded historical run number.

## Current state

Hottop is a cross-category, evidence-aware hot-topic brand creative engine. The foundation now covers adaptive intent, promotion semantics, comparison/trend research, category reframing, semantic bridge search, flexible creative formats/media, hard Creative Review + contextual ranking, provider-neutral `hottop.render.v2`, config-driven `hottop.video-plan.v1`, and dry-run-first production execution.

The stale four-panel/InkClaw-only README has been replaced with the current architecture and operating contract.

## Motion production contract

Default unattended path:

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg`

- MoviePy is the default headless compositor; Motion Canvas is planning/interactive-preview unless an operator supplies a real executor.
- FFmpeg performs compatibility finalization and final media verification.
- Audio is first-class: role-aware dialogue, original synthetic music and procedural SFX/Foley are preserved in the plan and mixed before finalization.
- `video-run` is dry-run by default. Only explicit `--execute` may spawn trusted configured stages after readiness passes.
- Fresh-output checks, failure cleanup, final media verification and `shell=False` structured commands are enforced.

## Generation routes

### Zero-cost router

- Only configured `cost_per_unit: 0` candidates are eligible; paid fallback is forbidden.
- Rights-safe reference I2V carries explicit `generated-original` or `user-provided-rights-cleared` metadata.
- Local reference preflight happens before upload/free GPU use.
- Generated video is quality-gated for decodability, motion and duplicate-frame ratio; rejected artifacts are deleted before failover.
- Optional deterministic reference-motion degradation is explicit and provenance-labelled, never misreported as AI-generated.
- Accepted shot artifacts are bound to configured backend identity plus SHA-256/byte size and re-verified immediately before MoviePy consumption.
- ZeroGPU output downloads are restricted to the configured Space origin and download redirects are disabled, so a remote SSE result cannot redirect a Hugging Face bearer token to an attacker-controlled host.

### Operator WanGP

- WanGP is operator-managed; Hottop does not install it or download models automatically.
- Reference I2V uses the fixed `__HOTTOP_REFERENCE_IMAGE__` Settings placeholder rather than guessing provider-specific fields.
- Reference files and rights metadata are checked locally before session creation.
- Cross-shot `subject_id` / identity-lock semantics are validated before production-plan commands are emitted.
- Identity anchors are injected into generation prompts so every backend receives the same subject semantics.
- Dry-run fail-closes when a shot has a reference but exported Settings lack the placeholder, or when Settings contain the placeholder but a shot has no reference.
- WanGP output passes the shared ffprobe/ffmpeg generated-video quality gate before being returned; rejected output is deleted.

### Other routes

- Wan2.2 remains an optional operator-controlled local route; model downloads/GPU provisioning are never automatic.
- `comfy-api-v2` remains an explicit optional remote/self-hosted route with environment-only credentials and explicit execution.
- Comfy remote endpoints require HTTPS; plain HTTP is accepted only for structurally validated loopback endpoints. Remote job output URLs must use HTTPS, while local HTTP output is allowed only from the same loopback origin. Output downloads do not carry the API bearer token and do not follow redirects.

## Style / creative direction

- Anti-Polish / Controlled Badness remains a selectable differentiation strategy: **low production feel + high comedy control**.
- `roughness_score` routes surface polish; it is not a universal product look.
- Roughness never relaxes character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety, rights safety or encoding integrity.
- Social/hotspot work remains ad-light by default: no in-asset URL/QR/hard CTA unless conversion intent explicitly requires it.
- References teach grammar, not pixels; protected frames, likenesses, official character designs, copied UI/layouts, source footage and copyrighted soundtracks are excluded by default.

## Representative sources

- `examples/video/inkclaw-cow-snake.render.json` — high-roughness original Anti-Polish story.
- `examples/video/inkclaw-odyssey-witch-pigs.render.json` — lower-roughness cinematic mythic meme.
- `examples/video/hottop-zero-cost-reference-i2v.render.json` — generated-original rights-safe reference-I2V example.

## Current verification

Recent closure work was introduced RED-first and then brought GREEN on both Python 3.11 and 3.12, including:

- cross-shot reference identity consistency and prompt identity anchors;
- WanGP reference placeholder binding + rights/file preflight;
- WanGP generated-video quality gate;
- `video-run` WanGP placeholder/reference dry-run fail-closed checks;
- ZeroGPU cross-origin bearer-token/SSRF confinement;
- Comfy endpoint parsing and remote-output SSRF confinement;
- README architecture synchronization.

The latest security implementation head was GREEN on both supported Python versions before this documentation-only synchronization. Always re-fetch the current head's CI before making a completion or merge claim.

## Remaining closure actions

1. Verify this final synchronized head on Python 3.11 / 3.12 with Ruff + full pytest.
2. Re-fetch PR #1 mergeability, comments/review threads and current head after the verification run. Branch-protection details are not readable through the current GitHub integration, so do not infer them.
3. Synchronize the PR summary and mark PR #1 ready for review if no blocking finding appears.
4. Treat the final merge as the remaining irreversible repository action: use the verified expected-head SHA and do not merge a moved head accidentally.
5. After merge, verify `main` contains the merged head and record the next milestone rather than continuing Foundation indefinitely.
