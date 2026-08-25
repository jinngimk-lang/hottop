# Hottop Status

Last updated: 2026-08-25
Active workstream: PR #12 `prod/software3d-config-runtime`
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is the durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Foundation v0.1 — COMPLETE

PR #1, **Build Hottop brand creative engine foundation**, was squash-merged into `main` as `ee0ffb388745d7ed1f890d278cfbb17cccea167c`. Foundation established the cross-category creative/research contracts, provider-neutral render/video plan, trusted dry-run-first execution, first-class audio, zero-cost/operator generation boundaries, identity/reference controls, quality gates, artifact provenance, and selectable Anti-Polish / Controlled Badness.

## Durable motion contract

Default unattended path:

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg`

`video-run` remains dry-run by default. Only explicit `--execute` may spawn trusted configured stages after readiness passes. External model downloads, GPU provisioning, credentials, cloud uploads and paid services remain operator-controlled. Free-capacity exhaustion may retry within bounds or degrade to an explicit deterministic path; it never enables paid fallback.

References teach grammar, not pixels. Protected frames, likenesses, official character designs, copied UI/layouts, source footage and copyrighted soundtracks remain excluded by default. Surface roughness never relaxes continuity, directing, subtitle/dialogue correctness, comedy timing, product semantics, claim safety, rights safety or encoding integrity.

## Production v0.2 — first full config-to-MP4 evidence CLOSED

The deterministic software-3D baseline now proves the complete checked-in production contract rather than only isolated renderer/compositor pieces.

Current production evidence:

- `config/video/anti-polish-software3d.yml` is a zero-cost 360×640 / 12 fps / 10 s production profile using `generation_backend: software3d`, local eSpeak Mandarin dialogue, original synthetic music, procedural SFX/Foley, MoviePy composition and FFmpeg finalization.
- `src/hottop/video_software3d.py` uses real 3D vertices, transforms, perspective projection and depth-sorted faces. `src/hottop/video_software3d_production.py` renders the checked-in five-shot `examples/video/inkclaw-cow-snake.render.json` story with stable original character geometry and continuous workshop staging.
- software3d now participates in the same runtime provenance boundary as free-GPU generation: each generation command resolves a `shot-XXX.artifact.json` sidecar, the sidecar must declare `planned_generation_backend=software3d`, `artifact_kind=deterministic-generated`, `backend=software3d`, and the expected shot/path identity before composition proceeds. MoviePy independently re-verifies byte size + SHA-256 immediately before consuming every shot.
- PR #12 ordinary CI at code head `82d7870ca7a6650f7032c7a890319705b8daa261` passed Ruff + the full pytest suite on Python 3.11 and 3.12 after the provenance RED→GREEN cycle.
- `production-smoke` run **32823329496** executed the real checked-in story with `hottop video-run ... --execute` on a clean Ubuntu runner using only free/open local dependencies (`.[dev,video]`, FFmpeg, eSpeak). It completed successfully and uploaded artifact `hottop-software3d-production-smoke`.
- The uploaded evidence contains the final MP4, run-result, video plan, ffprobe report and five byte-bound shot sidecars. `run-result.json` reports `executed=true`, `ready=true`, five artifact manifest paths and 12 executed stage commands.
- Final media verification from that run: duration **10.008005 s**, video **H.264 / yuv420p**, audio **AAC**. Final MP4 SHA-256: `bab46a50557ddb984d42abb1342d5e74e2f73cd9aa1db83fdfa2369b4a48674a`.

The software-3D path is a guaranteed zero-cost real-motion baseline/fallback, **not** Hottop's cinematic quality ceiling. Its purpose is to make the entire production system usable without GPU/model downloads and to give reference-conditioned model backends a deterministic identity/continuity baseline to beat.

## Ecosystem / autonomy policy

`PROJECT.md` is canonical for the autonomous-owner mandate. `docs/operations/autonomous-ecosystem-radar.md` and `docs/operations/ecosystem-radar-policy.md` record the operating mechanics: continue the highest-value safe action within the same run; perform gap-first fresh upstream research; distinguish code and model/weights/data licenses; and integrate only source-verifiable, license-compatible, zero-cost-safe, testable and reversible improvements.

Fresh August 2026 findings keep official `zai-org/SCAIL-2` high on the multi-reference / character-animation benchmark list and confirm continued rapid WanGP evolution around longer/continued generation and reference memory. They remain candidate/operator stacks until exact revision, weights-license, hardware and measurable-quality gates are satisfied. Hottop should integrate narrow adapters/benchmarks rather than vendoring or auto-downloading large model stacks.

## Closed security / integrity boundaries

- ZeroGPU output URLs are confined to the configured Space origin and redirects are disabled, preventing bearer-token exfiltration and remote download steering.
- Comfy remote endpoints/outputs require safe parsed URL semantics; loopback HTTP is restricted to real loopback origins; output downloads carry no API token and do not follow redirects.
- WanGP references use an explicit exported-Settings placeholder, are locally rights-preflighted, and returned footage must pass the shared video-quality gate.
- Repeated `subject_id` references must carry consistent identity anchors before production commands are emitted.
- software3d generation sidecars are discovered and verified immediately after each generation stage and re-verified at MoviePy consumption.

## Next production actions

1. Use the successful software3d full-pipeline run as the deterministic benchmark, not as the visual-quality target.
2. Add a rights-safe reference/last-frame continuity benchmark that compares operator-owned/free GPU candidates against software3d on identity stability, motion, visual quality, reproducibility and failure recovery. Prioritize WanGP's current reference/continuation capabilities; keep SCAIL-2 as a high-value multi-reference benchmark candidate after exact weights/license/runtime review.
3. Improve the cinematic profile and local Mandarin dialogue quality while preserving a fully free fallback; stronger permissive/operator-owned TTS should enter through an isolated adapter and rights-safe voice policy.
4. Produce and archive a second full-pipeline cinematic-meme case (the original Odyssey witch/pigs story is the current representative source) so style routing is proven beyond Anti-Polish.
5. Prefer measurable production improvements over additional provider abstraction without a demonstrated gap.
