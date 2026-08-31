# LightX2V NVIDIA local-preflight evidence — 2026-08-31

## Measured gap

The operator-owned LightX2V route already failed closed on missing checkout/model/config, dirty or ambiguous source provenance, stale targets, runtime timeout, reference mutation and generated-media quality. It did not explicitly prove that a usable local NVIDIA GPU was visible before invoking LightX2V. In a misconfigured operator environment that could start the inference command and fail later, after unnecessary setup/runtime work.

## Accepted contract

`require_nvidia_gpu()` performs a bounded local-only `nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader,nounits` probe. It accepts at least one non-empty GPU row and fails closed when `nvidia-smi` is missing, times out, returns a non-zero status, raises an OS-level execution error or reports no visible GPU.

`run_lightx2v_shot()` calls this probe before starting the inference runner. Production keeps the real probe as the default. Unit tests inject an explicit no-op probe only where the generation path is being tested independently, so ordinary CI remains GPU-free without weakening the production default.

The probe does not provision hardware, install drivers, download models, call a hosted endpoint, consume credits or create a paid fallback.

## TDD and production evidence

- RED `e5ccb02f892c29641172a93935b9f2adb55a2859`: CI #2560 failed the new NVIDIA-preflight regression contract before the implementation existed.
- GREEN exact PR head `14905514fcf76fe64ba62fb2cccdd5184fc9f19a`: CI #2567 succeeded.
- The same GREEN head passed production-smoke #284, executing the checked-in anti-polish cow and cinematic Odyssey software3d production routes plus final media/provenance verification.
- The same GREEN head passed cinematic-delivery-smoke #151, executing the 720p24 Odyssey delivery plus runtime provenance, final-media/provenance verification and evidence upload.
- Production-smoke #284 uploaded `hottop-software3d-production-smoke` (artifact id `9763926169`, 687,896 bytes, archive digest `sha256:181fa429933044c73d2cfe3f97374279c9d2f1ec76b925fb5f88b57237420f87`).
- PR #363 was SHA-locked squash-merged from the exact verified head as `2eaa6f47a529e803999c798aae8c426a90c4c759`.

## Ecosystem radar

Public LightX2V freshness still does not justify a pin change on freshness alone. The currently reviewed tip work is centered on SeedVR/distributed-runtime changes rather than a measured Hottop Wan2.2 I2V identity/requested-motion gain, so the existing tested route remains pinned by evidence rather than recency.

A small `Wan2.2-Fast` repository surfaced during freshness search with Apache-2.0 code and a CUDA/ZeroGPU 4-step I2V path, but its effective runtime also composes external Wan2.2 Diffusers weights, third-party dual-transformer weights, Lightning LoRAs and compiled CUDA artifacts. Those code/weights/artifact licenses and exact provenance have not been independently admitted as one Hottop-compatible zero-cost bundle, and no Hottop quality benchmark shows it beating the tested LightX2V route. It therefore remains radar-only: no vendoring, auto-install or model download.

Qwen3-TTS community ports continue to demonstrate lower-hardware possibilities, including a Rust/ONNX/llama.cpp implementation reporting CPU/Vulkan/CUDA quantized execution, but those claims are not yet Hottop same-line Mandarin benchmark evidence. Existing operator-provisioned Qwen3-TTS benchmark candidates remain unchanged.

## Durable-doctrine decision

`PROJECT.md` remains unchanged. Explicit local accelerator availability is implementation closure under the already-canonical operator-owned, fail-closed, no-auto-provisioning doctrine rather than a new project direction.

## Remaining production boundary

The true LightX2V quality milestone remains real generated media. The repository now rejects a missing local NVIDIA runtime earlier, but this run still does not have an operator-provisioned reviewed LightX2V checkout, Wan2.2 model and suitable NVIDIA GPU to generate honest I2V evidence. Once those exist, generate at least two rights-safe subject-bearing shots and require identity, requested-action motion, media quality, exact request/source/config/reference provenance and final composition verification before claiming success.
