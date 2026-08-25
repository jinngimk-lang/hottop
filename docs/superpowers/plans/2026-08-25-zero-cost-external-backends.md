# Zero-Cost External Video Backends — Implementation Plan

## Goal

Keep Hottop's default video path strictly non-paying while allowing an operator to use mature locally installed projects such as WanGP without copying their application code into Hottop.

## Current decision

- Default unattended route remains `zero-cost-router` + free Hugging Face ZeroGPU + deterministic MoviePy/FFmpeg fallback.
- Operator-owned GPU backends are optional and explicit.
- Wan2.2 remains the simple native local backend.
- WanGP is treated as an external interoperability target because its Community License 2.0 permits free internal/company use but restricts selling/embedding/exposing WanGP itself as a paid product or service.
- LTX-2.x is license-gated. Its current Community License has a revenue threshold that can require a paid commercial agreement; Hottop must not label it universally free for commercial production.

## Implementation slices

1. **Shell-safe external command contract — completed in this workstream.** `src/hottop/video_external.py` accepts only an operator-provided executable name and three explicit placeholders: prompt, duration_seconds, output. It never interprets shell syntax and exposes no secret/environment placeholder.
2. **TDD contract — completed.** `tests/test_video_external_command.py` covers normal expansion, unknown-placeholder rejection and executable-name validation.
3. **Plan integration — next.** Extend `hottop.video-plan.v1` generation command construction so `generation_backend: external` can emit this contract for a configured local operator backend.
4. **WanGP profile — next.** Add a non-default `config/video/wangp-operator.yml` that references an already-installed executable/work directory and does not download weights or provision GPU resources.
5. **Execution boundary — next.** Make `video-run --execute` accept the external command only after `video-doctor` confirms the executable and working directory; run with argv arrays, `shell=False`, fresh output verification and existing media/provenance gates.
6. **Real smoke — after integration.** When an operator environment is explicitly supplied, run one short local MP4 smoke and compare against native Wan2.2 on motion, identity continuity, latency and artifact validity. No unattended model download.
7. **LTX-2 audio/video experiment — separate lane.** Only after the intended commercial/license status is explicitly recorded; compare synchronized native audio against Hottop's existing free local voice/music/SFX pipeline.

## Non-regression rules

- Never replace the default free router with WanGP or LTX-2.
- Never bundle WanGP code into Hottop or expose it as a paid Hottop backend.
- Never silently download models, install custom nodes, create credentials or consume paid credits.
- If an operator backend is missing, fall back to the existing zero-cost path rather than failing the entire creative pipeline.
- Generated footage still passes the same quality, provenance, rights and final-delivery media gates.
