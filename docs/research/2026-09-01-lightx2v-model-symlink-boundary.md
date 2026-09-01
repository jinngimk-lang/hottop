# LightX2V model symlink boundary evidence — 2026-09-01

## Measured gap

Hottop's LightX2V model provenance walker previously selected files with `Path.is_file()` and then read them with `open()`. Both operations dereference symlinks. A symlink placed inside the reviewed operator-owned model directory could therefore point to bytes outside that directory and still be included in generation/model provenance.

That behavior made the logical `model_path` boundary misleading: the digest covered the dereferenced bytes, but the operator model tree was not self-contained and inference could silently depend on unrelated local files outside the reviewed root.

## Decision

Before hashing model bytes, inspect every symlink entry under the model tree and require its strict resolved target to remain inside the resolved model root. Escaping, broken, or cyclic links fail closed before GPU probe or inference. Symlinks whose resolved target remains inside the reviewed model root continue to be allowed so valid local model layouts are not rejected unnecessarily.

This is a local-preflight/provenance hardening only. It adds no network call, install, model download, paid provider, credit consumption or GPU provisioning.

## TDD evidence

- RED exact head `88615b4bd931cfce78a5e3c78da381c3c2deb0f9`: CI #2687 failed the new escaping-model-symlink regression under the old dereferencing behavior. Python 3.12 was cancelled by fail-fast and is not counted as RED evidence.
- First implementation `b853410c89233e2430b41a83f561e6fe160df702`: CI #2688 proved the implementation failed closed, but the test over-specified an internal diagnostic that the existing broad provenance wrapper normalizes; result was `1 failed, 657 passed`.
- GREEN exact head `824a57122fe91f8898278f2f6bc6d5cef240dd06`: CI #2689 passed Ruff plus full pytest on Python 3.11 and 3.12. The final regression asserts the behavioral contract: `LightX2VError`, zero GPU-probe calls, zero inference-runner calls and no output artifact.

PR #406 was SHA-locked squash-merged as `d372c6709ab32dbcdd1fe25ab13025c540c1873c`.

## Production media evidence on GREEN head

- production-smoke #335 completed the checked-in zero-cost software3d cow + Odyssey route through moving shots, Mandarin/audio, MoviePy, FFmpeg, final H.264/AAC verification, artifact manifests and seam checks. Uploaded evidence was 687,895 bytes with artifact ZIP SHA-256 `f5b4c912b86a9e07c886fbd8b5a454536ee4eb45c4e25d6d34158467e353fdf3`.
- cinematic-delivery-smoke #202 completed the independent real 720p24 Odyssey delivery. Verification required H.264/yuv420p video at 720x1280 and 24 fps, AAC audio, positive duration, five shot manifests and runtime/executable/numeric-library/font provenance. Seam evidence was `intra_p95=0.934`, `max_delta=4.185`, `max_ratio=4.481`, within the workflow limits. Uploaded evidence was 624,453 bytes with artifact ZIP SHA-256 `a6a8d9f495cd6ef2dcf3fc7acac067123285126d386acc6696131dda786d1b15`.

## Ecosystem radar

LightX2V public `main` advanced to exact revision `26cfa87782e109ffdccb20d5f437561cefa9a530` on 2026-09-01 with `fix: prevent first-step recompilation in MiniMax-H3 attention (#1469)`. The change is MiniMax-H3 compile-performance maintenance, not same-case Wan2.2 I2V identity/requested-action evidence, so Hottop does not freshness-only repin.

Open LightX2V reports continue to justify separating execution/media integrity from generated-content correctness: reported cases include correct-length I2V output with static frames (#895), meaningless color/light output (#1170), and materially worse content/motion versus a comparable Diffusers route (#603). Accelerated/distilled Wan2.2 routes therefore remain gated until exact code+weights+config provenance, image-conditioning correctness, license chain and Hottop same-case identity/requested-action quality are demonstrated.

`mingshi2333/Qwen3-TTS-ncnn` remains a gated Apache-2.0 operator-owned runtime candidate for Qwen3-TTS CPU/Vulkan execution. It still requires separately reviewed build/model acquisition and Hottop lacks a rights-safe same-line Mandarin A/B against the current 1.7B CustomVoice target, so it is not integrated into unattended execution.

## Doctrine impact and rollback

`PROJECT.md` does not change: keeping operator-owned model bytes inside a reviewable local boundary is a stricter implementation of existing ZERO_COST/local-preflight/fail-closed/byte-provenance doctrine, not a new product direction.

Rollback is a normal revert of PR #406. The guaranteed deterministic software3d baseline is otherwise unchanged.
