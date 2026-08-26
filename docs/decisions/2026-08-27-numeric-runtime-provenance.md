# Numeric runtime provenance for cinematic software3d evidence

Date: 2026-08-27
Milestone: Production v0.2
Status: accepted evidence contract; post-merge re-verified

## Problem

Hottop already bound source/plan bytes, package versions, FFmpeg/FFprobe/eSpeak/font bytes and CPU identity for 720×1280/24fps Odyssey delivery. Cross-run evidence nevertheless showed that visually near-identical accepted outputs can differ in encoded bytes across hosted runners. CPU identity narrowed the explanation, but it still did not identify the numerical execution stack used by NumPy/BLAS or its thread configuration.

The production rule remains contract-first rather than hash-first: visual/audio/media/integrity gates define acceptance. Numeric runtime identity is provenance used to interpret scoped byte differences; it is not a reason to lower quality or force universal bitwise determinism.

## TDD and real production evidence

PR #102, `Bind numeric runtime provenance in cinematic delivery evidence`, established the contract.

- RED `a3836c2f16a30db5b75007bd440967bd75ccfa62`: CI #1765 passed Ruff and failed exactly the new numeric-runtime contract.
- Initial GREEN `8db6a0573dfa6825cd095a60873a7fe04b61b3e9`: captured logical CPU count, relevant BLAS/OpenMP environment, `numpy.show_config()` and `numpy.show_runtime()` plus SHA-256 identities for both reports.
- Real delivery counterexample on `389e7857430dfcedceeb8005577f5482ba1e0383`: repository CI #1769 passed, but cinematic-delivery-smoke #47 failed because `threadpoolctl` was not installed. This proved the evidence helper must be an explicit dependency rather than an assumed NumPy transitive.
- Evidence fix `1b92c62b5cf03121f70589126b48cc0f9e7266b7`: CI #1771 and cinematic-delivery-smoke #49 passed.
- Supply-chain hardening `32e93ff079066e126b55811d5be8db62356779b3`: pins reviewed `threadpoolctl==3.6.0`; exact-head CI #1773, production-smoke #187 and cinematic-delivery-smoke #51 all passed.

PR #102 was squash-merged as `05575adbbfc9b462a5744c7d3c0994458654d5b0`. Post-merge CI #1774, production-smoke #188 and cinematic-delivery-smoke #52 all passed.

## Exact 720p evidence from cinematic-delivery-smoke #51

The uploaded `hottop-cinematic-software3d-delivery` artifact has Actions digest:

`sha256:257ff8331775a4025f016ee073e3f566da4495fbeef0b5f421813f27e811f866`

Its `runtime-provenance.json` records:

- Python `3.12.14`;
- platform `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`;
- CPU `AMD EPYC 9V74 80-Core Processor`, vendor `AuthenticAMD`, 4 logical CPUs;
- NumPy `2.5.2`;
- `threadpoolctl 3.6.0`;
- OpenBLAS `0.3.34.0.0`, pthreads, `num_threads=4`, architecture `Haswell` in `numpy.show_runtime()`;
- no explicit `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `BLIS_NUM_THREADS` or `VECLIB_MAXIMUM_THREADS` environment override;
- `numpy_config_sha256 = 422bb24e208bebe15309bfe2c9ba8e2d67652badd4b780b388a1ed25ded73623`;
- `numpy_runtime_sha256 = bd30c90a6818f0549b73f0ed15cd3351d356f4917fb5fec3618f27e73e794353`.

The accepted output remained the established Odyssey delivery:

- final MP4 SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`;
- H.264, 720×1280, yuv420p, 24fps + AAC, 15.0 seconds;
- seam intra-shot p95 `0.933903`;
- max seam delta `4.184792`;
- max seam/intra ratio `4.480971`.

This proves that the new provenance fields are present in the actual delivery artifact, not merely declared in workflow source.

## Post-merge comparison: #51 vs #52

Post-merge cinematic-delivery-smoke #52 repeated the same accepted production contract on `main@05575adb...`, but the hosted CPU changed:

| Evidence | PR-head #51 | Post-merge #52 |
|---|---|---|
| CPU | AMD EPYC 9V74 80-Core Processor | AMD EPYC 7763 64-Core Processor |
| vendor | AuthenticAMD | AuthenticAMD |
| logical CPUs | 4 | 4 |
| NumPy | 2.5.2 | 2.5.2 |
| OpenBLAS runtime | 0.3.34.0.0, pthreads, 4 threads, Haswell | same |
| `numpy_config_sha256` | `422bb24e208bebe15309bfe2c9ba8e2d67652badd4b780b388a1ed25ded73623` | same |
| `numpy_runtime_sha256` | `bd30c90a6818f0549b73f0ed15cd3351d356f4917fb5fec3618f27e73e794353` | same |
| video-plan SHA-256 | `40d5b341e357572bfe10c4d9e0ba8bbc81038f31ba0b3b8f7467e94109b4031f` | same |
| final MP4 SHA-256 | `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df` | same |
| seam metrics | `0.933903 / 4.184792 / 4.480971` | same |

The #52 Actions artifact digest is `sha256:1dad9f6e22e211fcb37dc95b518aa978b326e1b3ace4347517615909d1e641c1`.

This is a useful counterexample to simplistic CPU-only causality. A CPU model change can coexist with byte-identical accepted output when the observed numerical runtime evidence is unchanged. Earlier cross-run evidence also showed cases where changed hosted CPU/runtime context coincided with different bytes but near-identical decoded quality. Together, these observations justify recording both hardware and numerical runtime identity while avoiding single-factor causal claims.

## Dependency admission

`threadpoolctl 3.6.0` is used only as a small numerical-runtime evidence helper. Its upstream/PyPI metadata declares BSD-3-Clause, Python >=3.9, and the PyPI 3.6.0 release was published through Trusted Publishing with Sigstore attestations. Hottop pins the reviewed version so evidence capture cannot drift silently.

The dependency does not provision GPUs, download models, make network inference calls, enable paid services or alter rendering math.

## Decision

For repeatability evidence, Hottop binds both hardware identity and material numerical runtime identity when the production path depends on NumPy/native BLAS execution.

At minimum, new 720p cinematic software3d evidence should retain:

1. CPU/machine identity and `/proc/cpuinfo` byte hash when available;
2. logical CPU count;
3. relevant BLAS/OpenMP thread environment;
4. human-readable `numpy.show_config()` and `numpy.show_runtime()` reports plus SHA-256 identities;
5. the `threadpoolctl` package version used to expose native threadpool runtime details;
6. the existing source/plan/package/executable/font/shot/final-media provenance.

These fields help interpret byte variance. They do not convert byte equality into the production success definition and must not be used to weaken visual/audio/media/integrity gates.

## Boundaries

- Do not infer single-factor causality from one changed provenance field on hosted runners.
- Do not force single-threaded or lower-quality execution solely to chase stable hashes.
- Do not treat an environment report as proof that a generated/neural route preserves identity or quality; those routes retain their own output-side evidence gates.
- Operator GPU/model readiness remains independently fail-closed.
