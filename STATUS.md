# Hottop Status

Last updated: 2026-08-25
Active branch: `main`
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is the durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Foundation v0.1 — COMPLETE

PR #1, **Build Hottop brand creative engine foundation**, was squash-merged into `main` as `ee0ffb388745d7ed1f890d278cfbb17cccea167c` after the verified PR head passed Ruff + the full pytest suite on Python 3.11 and 3.12. The resulting `main` push then passed CI again.

Foundation v0.1 established Hottop as a cross-category, evidence-aware hot-topic brand creative engine with:

- adaptive natural-language intent and promotion semantics;
- trend/comparison research, enrichment, evidence discipline and semantic bridge search;
- category-default / constraint-deletion reframing;
- flexible creative formats/media plus hard Creative Review and contextual ranking;
- provider-neutral `hottop.render.v2` and config-driven `hottop.video-plan.v1`;
- dry-run-first trusted video execution;
- MoviePy headless composition + FFmpeg compatibility/final-media verification;
- first-class dialogue, original synthetic music and procedural SFX/Foley;
- zero-cost, operator WanGP, local Wan2.2 and explicit Comfy API generation boundaries;
- rights-safe reference I2V, cross-shot identity locks, generated-video quality gates and byte-bound artifact provenance;
- Anti-Polish / Controlled Badness as a selectable style strategy rather than a universal look.

## Closed security / integrity findings

The Foundation closure review found and repaired concrete production-boundary issues before merge:

- **ZeroGPU bearer-token / SSRF boundary:** remote SSE output URLs are confined to the configured Space origin and output-download redirects are disabled, so the Hugging Face bearer token cannot be redirected to an attacker-controlled host.
- **Comfy output SSRF boundary:** remote endpoints require HTTPS; loopback HTTP must parse as a real loopback host rather than merely share a string prefix; remote outputs require HTTPS; local HTTP outputs must remain same-loopback-origin; output downloads carry no API token and do not follow redirects.
- **WanGP reference binding:** rights-safe references use the explicit `__HOTTOP_REFERENCE_IMAGE__` exported-Settings placeholder, are locally preflighted, and must match every shot before GPU execution.
- **WanGP generated output:** returned footage must pass the shared ffprobe/ffmpeg motion/duplicate/decodability gate before composition; rejected output is deleted.
- **Cross-shot identity:** repeated `subject_id` references must carry consistent identity anchors before production commands are emitted.

## Durable motion contract

Default unattended path:

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg`

`video-run` remains dry-run by default. Only explicit `--execute` may spawn trusted configured stages after readiness passes. External model downloads, GPU provisioning, optional package installation, credentials, cloud uploads and paid services remain operator-controlled.

References teach grammar, not pixels. Protected frames, likenesses, official character designs, copied UI/layouts, source footage and copyrighted soundtracks remain excluded by default. Surface roughness never relaxes continuity, directing, subtitle/dialogue correctness, comedy timing, product semantics, claim safety, rights safety or encoding integrity.

## Production v0.2 goal

The next milestone moves from architecture completeness to **repeatable production evidence**. The flagship acceptance target is a real, playable vertical product short generated from a checked-in Hottop render source and production profile, with the same original character remaining recognizable across shots and the product benefit emerging through story rather than banner-ad UI.

Priority order:

1. Produce a representative config-to-MP4 run with real generated/pseudo-3D shot assets rather than a slideshow/vector placeholder.
2. Preserve subject identity through reference-conditioned generation and reject identity/quality failures before composition.
3. Keep one continuous story geography, dialogue, original BGM/SFX and natural shot transitions through the full pipeline.
4. Archive the exact render source, production config, artifact provenance and final-media verification evidence needed to reproduce the run.
5. Turn the successful run into the baseline for repeated hotspot/product production instead of adding more provider abstractions first.

Representative sources already available:

- `examples/video/inkclaw-cow-snake.render.json` — high-roughness original Anti-Polish story.
- `examples/video/inkclaw-odyssey-witch-pigs.render.json` — lower-roughness cinematic mythic meme.
- `examples/video/hottop-zero-cost-reference-i2v.render.json` — repository-generated rights-safe reference-I2V example.

## Immediate next action

Start Production v0.2 from current `main`, use the existing InkClaw cow/snake story as the first flagship production case, and prioritize **actual consistent moving imagery** over additional orchestration surface area.
