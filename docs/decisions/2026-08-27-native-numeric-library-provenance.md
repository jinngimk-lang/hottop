# Native numeric library byte provenance for cinematic delivery

Date: 2026-08-27
Milestone: Production v0.2
Status: accepted on PR head; post-merge re-verification required before this record is final

## Problem

Hottop's 720×1280/24fps Odyssey delivery evidence already bound CPU identity, logical CPU count, BLAS/OpenMP environment, NumPy configuration/runtime reports and the pinned `threadpoolctl==3.6.0` helper. Those reports identify the numerical stack semantically, but they did not bind the exact native numeric library bytes actually loaded into the NumPy process.

For repeatability analysis this leaves a provenance gap: two hosted runners can report the same OpenBLAS version/API while loading different binary builds. The production acceptance rule remains quality/media/integrity-contract-first rather than universal hash-first, but material runtime identity should be byte-bound when it can be measured safely.

## TDD closure

PR #104, `Bind loaded numeric library bytes in delivery provenance`, closed this gap.

- RED `af535b28ea5b03358f65a52970ce250e31d061b8`: CI #1779 passed Ruff and failed exactly the new native-library provenance contract (`1 failed / 504 passed`).
- GREEN `cef9dde7427b9e7ba6e3606496fde34d79a2d3e3`: reuses the already-pinned `threadpoolctl.threadpool_info()` and records every resolved loaded numeric-library path once, with `internal_api`, `user_api`, version, byte size and SHA-256. The same delivery job rereads the resolved file and fail-closes if size/hash no longer match.
- Exact-head CI #1780 passed.
- Exact-head cinematic-delivery-smoke #54 passed.
- PR #104 had no review threads and was squash-merged as `40dc5f4e1e7289b8f2c5c1bf7903be01a4b218ac`.

No renderer math, FFmpeg/media threshold, provider routing, model download, GPU provisioning, credential or paid behavior changed.

## Exact PR-head production evidence

Cinematic-delivery-smoke #54 produced Actions artifact `hottop-cinematic-software3d-delivery` with digest:

`sha256:29c54db3c3bb67ee5be41018cb09a9b93b3d89dc666b938047a85644c6768cae`

Its `runtime-provenance.json` records one loaded BLAS library:

- resolved path: `/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/site-packages/numpy.libs/libscipy_openblas64_-61654e39.so`;
- `internal_api`: `openblas`;
- `user_api`: `blas`;
- reported version: `0.3.34.0.0`;
- size: `25210641` bytes;
- SHA-256: `6cad8d2ad994ddc43d2ccdb0fb5d9458373ff1b87ef7ff420f2f94406eb8f082`.

The same artifact reports NumPy `2.5.2`, 4 logical CPUs, OpenBLAS/pthreads with 4 runtime threads, and `numpy_runtime_sha256 = a6892f4c6800952bafcf8d8666b3e052f725d890b5ac4613e1d53d5464658683`.

This evidence is scoped to that exact GitHub-hosted runtime. The absolute library path is diagnostic context, not a portable identity; the file size/hash is the durable byte identity.

## Decision

For production evidence paths that depend materially on native numerical libraries and can inspect the loaded runtime safely, Hottop should bind the exact loaded library bytes in addition to semantic runtime reports.

At minimum retain:

1. resolved runtime path as diagnostic context;
2. library API identity (`internal_api` / `user_api`) when exposed;
3. reported version;
4. exact byte size;
5. exact SHA-256;
6. existing NumPy/runtime/thread/CPU/source/plan/media provenance.

The evidence collector must fail closed if a reported loaded library cannot be resolved to a real file, if no expected native numerical library is detected for a path that requires one, or if its bytes change before verification.

## Boundaries

- Native-library byte identity explains runtime provenance; it does not redefine success as bitwise output equality.
- Do not infer causality from a binary hash change alone. Accepted visual/audio/media/integrity gates remain the production contract.
- Do not copy or archive third-party system libraries into Hottop merely to preserve provenance; record identities only.
- Do not reduce thread count, quality or throughput solely to chase a universal output hash.
- This contract does not prove neural/generated-video identity continuity; generated routes retain independent source/model/reference/output/evaluator evidence gates.
- Operator GPU/model readiness remains independently fail-closed.
