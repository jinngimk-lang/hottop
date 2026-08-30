# TTS benchmark execution-shape evidence — 2026-08-30

## Decision

Extend the existing provider-neutral `hottop.tts-benchmark.v1` evidence surface so latency/RTF readiness binds not only generation controls and hardware identity, but also the concrete execution shape used to obtain those timings.

This is an evidence-contract change only. It does not execute TTS, install dependencies, download models, provision accelerators, use credentials or call paid services.

## Measured gaps

Four false-ready classes were reproducible on the existing inspector.

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

- `mode` must be one of the currently supported execution shapes: `cli` or `server`;
- positive integer `concurrency`;
- positive integer `batch_size`;
- when `mode=server`, a nonblank `connection_strategy` plus positive integer `worker_count` and `threads_per_worker`.

A descriptive object such as `{ "note": "same settings" }` is not evidence. A normal single-process command-line benchmark is representable as:

```json
{"mode":"cli","concurrency":1,"batch_size":1}
```

RED CI #2306 passed Ruff and produced exactly 4 pytest failures / 582 passes: missing execution profile, descriptive-only profile, server mode without connection strategy, and missing evidence persistence. The first implementation made those new contracts pass; CI #2307 then exposed only legacy ready-fixture migration because old fixtures lacked the now-required profile. Those fixtures were migrated rather than weakening the gate.

### Unknown execution mode bypass

After execution-shape evidence became mandatory, one narrower false-ready remained: any nonblank `mode` other than the recognized `server` string could still pass as long as `concurrency` and `batch_size` were positive. A descriptive or invented mode such as `same-settings` therefore avoided the server-only connection-strategy gate while still making the benchmark ready.

Hottop now accepts only the two execution shapes that the benchmark contract actually defines and can interpret: `cli` and `server`. New runtime shapes such as in-process/library execution require an explicit contract extension before they can carry comparable latency/RTF evidence; they must not gain evidence semantics merely by choosing a new string.

RED CI #2321 passed Ruff and failed pytest on the new unknown-mode contract. The minimal implementation then passed Ruff and the full pytest suite on Python 3.11 and 3.12 in exact-head CI #2322.

### Server worker/thread topology was unbound

A fresh operator report on `gabriele-mastrapasqua/qwen3-tts` issue #24 (2026-08-29) demonstrates why `server + concurrency + batch_size` is still insufficient performance provenance: a dual-Xeon server launched with `--prefork 12 --prefork-threads 2` did not use the expected CPU topology under 24 concurrent requests, and the operator explicitly questioned prefork/thread and batching behavior. This is runtime-specific evidence, not a Hottop performance claim, but it proves worker/process topology can materially change what a server benchmark means.

Before this closure, Hottop accepted server evidence that bound connection strategy, concurrency and batch size while omitting the server worker/process count and threads per worker. Two measurements with materially different process/thread layouts could therefore share the same benchmark-wide execution profile semantics.

The server contract now also requires:

- positive integer `worker_count`;
- positive integer `threads_per_worker`.

The field names are intentionally provider-neutral. For Pure-C qwen3-tts they correspond to the effective `--prefork` / `--prefork-threads` shape; other runtimes should map their actual worker/process and per-worker threading semantics rather than copying upstream flag names. A single-worker server remains expressible with `worker_count=1` and the actual positive thread count.

RED exact head `fa917df5e9e730994e2a01cee0717215ffea96de` passed Ruff and produced exactly **1 failed / 602 passed**: server evidence without worker/thread topology incorrectly remained `ready=true`. GREEN exact head `faf5141e1bc3197fdfcb675cbb83ad998a69e5af` then passed the full Python 3.11/3.12 CI #2404.

This does not claim that declared worker topology was actually honored by the runtime. Invocation/config evidence remains required separately; the contract only prevents Hottop from calling server latency comparable when the declared process/thread shape is absent.

## Evidence semantics

`execution_profile` is declared measurement provenance, not proof that a runtime internally obeyed the declaration. Operator execution records must still retain the actual invocation/configuration when available. Different execution shapes should be separate benchmark evidence sets when their latency/RTF values are not directly comparable.

The benchmark coherence surface is now intentionally layered:

1. exact text/language/checkpoint-supported speaker;
2. concrete generation protocol + canonical digest;
3. concrete hardware profile + canonical digest;
4. backend/device-identity coherence;
5. recognized concrete execution profile (`cli` or `server`) + canonical digest; server mode additionally binds connection strategy, worker count and threads per worker;
6. cold/warm coverage;
7. one runtime revision per candidate;
8. one model revision per candidate;
9. distinct trial artifact paths plus WAV/PCM integrity and finite positive latency;
10. listening/speaker/onset evidence kept separate from speed.

This preserves Hottop's benchmark-first rule: runtime support or an optimization toggle is not a performance claim until the exact workload, hardware and execution shape are bound to measured artifacts.
