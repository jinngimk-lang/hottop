# TTS benchmark CPU-count provenance — 2026-08-31

## Decision

For CPU-backed `hottop.tts-benchmark.v1` latency / realtime-factor evidence, require both a concrete CPU identity and a positive integer `logical_cpu_count` in the shared `hardware_profile`.

This extends, rather than replaces, the existing execution-shape contract. Server benchmarks must continue to bind `mode`, concurrency, batch size, connection strategy, worker count and threads per worker. Available logical CPU count is a separate measurement-environment fact needed to interpret that topology.

## Why this closes a measured gap

Before this change, a benchmark could be `ready=true` with:

- `backend=cpu`;
- a CPU label;
- a server topology such as 12 workers × 2 threads;
- no declaration of how many logical CPUs the host actually exposed.

That made the same declared topology appear comparable on materially different hosts. A 2026-08-29 Pure-C Qwen3-TTS community report (`gabriele-mastrapasqua/qwen3-tts#24`) provides a concrete runtime signal: on a dual-Xeon host reporting 24 total threads, the operator ran `--prefork 12 --prefork-threads 2` with 24 concurrent requests and observed that runtime utilization did not trivially equal the declared topology. The report is not Hottop performance evidence, but it demonstrates why available CPU capacity is part of interpretable provenance.

## Contract

For `hardware_profile.backend == "cpu"`:

- `cpu` must be a nonblank identity;
- `logical_cpu_count` must be a positive integer;
- the whole hardware profile remains canonicalized and SHA-256 bound in benchmark evidence.

A declared logical CPU count is still **measurement provenance, not proof of runtime affinity or utilization**. Operator execution records should preserve actual invocation, affinity/NUMA settings, environment and any runtime telemetry when those facts matter. Hottop must not infer that a process used all declared CPUs merely because they existed.

Accelerator-backed profiles are unchanged.

## TDD evidence

- RED commit `8aa9cadfe948c518ee0ccc680ec254f86fbd3061`: CI #2410 passed Ruff and failed pytest because a CPU-backed benchmark without `logical_cpu_count` still became ready.
- GREEN implementation `1c01e0cc586c81c485c80cc3c6bde5ab6c604b7c`: added the fail-closed CPU-count gate. Full-suite CI then exposed an older server-topology fixture that still claimed a ready dual-Xeon CPU benchmark without CPU-count provenance.
- Fixture correction `6e67f77ae5d91f1e0f46e1d2abb2cd2f4e685223`: the existing 12×2 dual-Xeon fixture now declares 24 logical CPUs instead of weakening the production gate. CI #2412 passed Ruff and full pytest on Python 3.11 and 3.12.

## Scope boundary

This change does not execute a neural runtime, download a model, provision CPU/GPU resources, change provider routing, or claim a performance improvement. It only prevents latency / RTF evidence from being marked ready when CPU capacity provenance is too incomplete to interpret.