# TTS accelerator-count provenance — 2026-08-31

## Decision

Accelerator-backed TTS latency / realtime-factor evidence must bind a positive integer `device_count` in the shared `hardware_profile` before `hottop.tts-benchmark.v1` can become `ready=true`.

This supplements the existing benchmark-method contract in `docs/research/2026-08-30-tts-bench-method-admission.md`:

- CPU evidence uses `backend=cpu`, a concrete CPU identity and positive `logical_cpu_count`.
- Accelerator evidence uses one recognized backend (`cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps` or `xpu`), a concrete `gpu` or generic `accelerator` identity, and positive `device_count`.
- `device_count` is provider-neutral. It replaces an old unvalidated fixture-only `gpu_count` spelling instead of creating vendor-specific count fields.

## Why this closes a real evidence gap

Before this change, profiles such as:

```json
{"backend":"cuda","gpu":"NVIDIA H200 SXM"}
```

could still produce ready latency / RTF evidence. That made one-device and multi-device measurements structurally indistinguishable even though the hardware scale materially changes the meaning of performance numbers.

The count is still **declared measurement provenance**, not proof that the runtime actually used every declared device or used them with a particular tensor/pipeline/data-parallel topology. Actual invocation, runtime config and telemetry remain separate evidence. Different hardware counts should be represented by different benchmark evidence sets rather than mixed into one directly comparable surface.

## TDD evidence

- RED exact head `77882ba1cc9100649728a8fbedc2cf19df86bfa2`, CI #2430: Ruff passed; pytest failed on the new accelerator-count contract.
- Minimal GREEN added the accelerator `device_count` gate without changing runtime/provider behavior.
- Full-suite CI then exposed one legacy fixture that used unvalidated `gpu_count`; the fixture was migrated to provider-neutral `device_count` rather than weakening the production gate.
- GREEN exact head `6a835fa64af6ccc3eedcd3d9bbe29b45d2fa43df`, CI #2434: Ruff and full pytest passed on Python 3.11 and 3.12.

## External freshness context

Recent public Qwen3-TTS serving benchmarks report hardware scale explicitly (for example, a specific single-H200 setup together with concurrency). Hottop treats that only as a methodology signal: public runtime performance is not imported as Hottop performance evidence, and a declared `device_count` does not substitute for locally bound runtime/output evidence.

## Safety / cost boundary

This change performs no TTS execution, network call, model download, dependency installation, GPU provisioning, credential use or paid action. It only strengthens the read-only evidence inspector.