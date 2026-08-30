# TTS benchmark execution-shape evidence — 2026-08-30

## Decision

Extend the existing provider-neutral `hottop.tts-benchmark.v1` evidence surface so latency/RTF readiness binds not only generation controls and hardware identity, but also the concrete execution shape used to obtain those timings.

This is an evidence-contract change only. It does not execute TTS, install dependencies, download models, provision accelerators, use credentials or call paid services.

## Measured gaps

Two false-ready classes were reproducible on the existing inspector.

### Backend/device mismatch

A hardware profile could declare `backend=cpu` while naming only an H100 GPU, or declare `backend=cuda` while naming only a CPU, and still become `ready=true`. That made the canonical hardware-profile digest internally inconsistent.

The hardened contract now requires:

- `backend=cpu` → a concrete nonblank `cpu` identity;
- accelerator backends (`cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps`, `xpu`) → a concrete nonblank `gpu` or generic `accelerator` identity;
- the pre-existing generic requirement for at least one concrete device identity remains.

RED CI #2304 passed Ruff and produced exactly 2 pytest failures / 580 passes on the new mismatch contracts. The minimal implementation passed Python 3.11/3.12 full CI #2305.

### Execution shape missing from performance evidence

The benchmark could also compare latency/RTF while omitting whether a candidate was measured through a one-shot CLI, a persistent server, a specific concurrency level or a particular batch size. This is material for the prepared Qwen3-TTS 1.7B routes: qwentts.cpp's reviewed runtime evidence already shows server connection/OpenMP-team and batch/concurrency shape can alter performance, while current public Qwen3-TTS benchmarking practice binds workload/concurrency instead of treating a runtime name as sufficient provenance.

The benchmark-wide `execution_profile` is therefore required for `ready=true` and is canonicalized with sorted-key JSON plus SHA-256. Minimum concrete fields are:

- nonblank `mode`;
- positive integer `concurrency`;
- positive integer `batch_size`;
- when `mode=server`, a nonblank `connection_strategy`.

A descriptive object such as `{ "note": "same settings" }` is not evidence. A normal single-process command-line benchmark is representable as:

```json
{"mode":"cli","concurrency":1,"batch_size":1}
```

RED CI #2306 passed Ruff and produced exactly 4 pytest failures / 582 passes: missing execution profile, descriptive-only profile, server mode without connection strategy, and missing evidence persistence. The first implementation made those new contracts pass; CI #2307 then exposed only legacy ready-fixture migration because old fixtures lacked the now-required profile. Those fixtures were migrated rather than weakening the gate.

## Evidence semantics

`execution_profile` is declared measurement provenance, not proof that a runtime internally obeyed the declaration. Operator execution records must still retain the actual invocation/configuration when available. Different execution shapes should be separate benchmark evidence sets when their latency/RTF values are not directly comparable.

The benchmark coherence surface is now intentionally layered:

1. exact text/language/checkpoint-supported speaker;
2. concrete generation protocol + canonical digest;
3. concrete hardware profile + canonical digest;
4. backend/device-identity coherence;
5. concrete execution profile + canonical digest;
6. cold/warm coverage;
7. one runtime revision per candidate;
8. one model revision per candidate;
9. distinct trial artifact paths plus WAV/PCM integrity and finite positive latency;
10. listening/speaker/onset evidence kept separate from speed.

This preserves Hottop's benchmark-first rule: runtime support or an optimization toggle is not a performance claim until the exact workload, hardware and execution shape are bound to measured artifacts.
