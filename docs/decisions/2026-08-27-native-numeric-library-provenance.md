# Native numeric library byte provenance for cinematic delivery

Date: 2026-08-27
Milestone: Production v0.2
Status: accepted and post-merge verified

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
- Post-merge `main` CI #1781 passed.
- Post-merge cinematic-delivery-smoke #55 passed the full 720p24 production, numeric-provenance capture, media/provenance verification and artifact-upload path.

No renderer math, FFmpeg/media threshold, provider routing, model download, GPU provisioning, credential or paid behavior changed.

## Exact production evidence

### PR-head smoke #54

Cinematic-delivery-smoke #54 produced Actions artifact `hottop-cinematic-software3d-delivery` with digest:

`sha256:29c54db3c3bb67ee5be41018cb09a9b93b3d89dc666b938047a85644c6768cae`

Its `runtime-provenance.json` records one loaded BLAS library:

- resolved path: `/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/site-packages/numpy.libs/libscipy_openblas64_-61654e39.so`;
- `internal_api`: `openblas`;
- `user_api`: `blas`;
- reported version: `0.3.34.0.0`;
- size: `25210641` bytes;
- SHA-256: `6cad8d2ad994ddc43d2ccdb0fb5d9458373ff1b87ef7ff420f2f94406eb8f082`.

The same artifact reports NumPy `2.5.2`, 4 logical CPUs and OpenBLAS/pthreads with 4 runtime threads.

### Post-merge smoke #55

Post-merge cinematic-delivery-smoke #55 produced artifact digest:

`sha256:ff4743ed561a3f2da2fe2ca5c82e4b5ee545d68b829b50fb0f85600346559529`

Direct artifact inspection confirms the same loaded native BLAS byte identity:

- resolved path: `/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/site-packages/numpy.libs/libscipy_openblas64_-61654e39.so`;
- OpenBLAS version `0.3.34.0.0`;
- size `25210641` bytes;
- SHA-256 `6cad8d2ad994ddc43d2ccdb0fb5d9458373ff1b87ef7ff420f2f94406eb8f082`.

The final 720p24 Odyssey MP4 SHA-256 is again:

`c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`

The real final-media seam evidence remains within the accepted gate:

- intra-shot p95 `0.933903`;
- max seam delta `4.184792`;
- max seam/intra ratio `4.480971`.

This evidence is scoped to the exact GitHub-hosted runtimes and checked-in production path. The absolute library path is diagnostic context, not a portable identity; the file size/hash is the durable byte identity.

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
