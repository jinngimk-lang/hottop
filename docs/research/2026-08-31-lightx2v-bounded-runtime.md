# LightX2V bounded runtime closure — 2026-08-31

## Measured production gap

The operator-owned LightX2V adapter executed the inference subprocess with no runtime bound. A stalled CUDA/runtime/model invocation could therefore hold one unattended Production v0.2 shot indefinitely. `subprocess.TimeoutExpired` also escaped the Hottop error boundary directly, leaving any partial output file behind.

This is an implementation-level closure of the existing fail-closed / bounded unattended execution doctrine. It does not change provider strategy, make LightX2V the default unattended backend, add network access, provision hardware, download models, or relax the guaranteed `software3d` zero-cost route. `PROJECT.md` therefore does not require a doctrine change.

## TDD evidence

RED head: `d18107e296839eb253bb6390026c133363a49b03` on PR #358.

- CI #2547 ran Ruff successfully and failed the new contract on Python 3.11 with exactly `2 failed, 628 passed`.
- Failure 1 proved the operator runner received no `timeout` argument.
- Failure 2 proved `subprocess.TimeoutExpired` escaped directly instead of becoming `LightX2VError` and cleaning the partial video.

## Implemented contract

`LightX2VAdapterConfig` now carries a positive `generation_timeout_seconds` value with a deliberately generous four-hour default for operator-owned large-model inference. The cinematic LightX2V config records the same bound explicitly, and the CLI exposes an override.

`run_lightx2v_shot` passes the bound to the subprocess runner. A timeout deletes the expected output path and raises `LightX2VError` with the configured bound. This keeps a hung local inference finite while avoiding retries, paid fallback, model downloads or provider expansion.

The timeout is an execution control, not part of generated-media identity: prompt/model/task/seed request provenance and generation-config byte provenance remain separate. Successful generated output still must pass source/config/reference stability checks, media quality gates, identity/requested-motion continuity gates and artifact byte binding.

## Fresh ecosystem check

At the time of this work, ModelTC/LightX2V public `main` remained at `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`, committed 2026-08-31 11:57:20 UTC. Its tip fixes SeedVR distributed-op exports and reports SeedVR2 BF16/FP8 validation; it does not provide measured Wan2.2 I2V continuity, requested-motion or Hottop runtime benefit. Hottop therefore keeps the reviewed local subset and does not repin for freshness alone.

## Remaining real-media gate

The next LightX2V milestone remains real rights-safe Wan2.2 I2V generation on an operator-provisioned local checkout/model/GPU, with at least two subject-bearing shots and complete identity, requested-action motion, media-quality and provenance evidence. The bounded runtime contract prevents that run from becoming an unbounded unattended stall; it does not substitute for real generated-video evidence.
