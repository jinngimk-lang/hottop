# LightX2V local-model byte provenance — 2026-09-01

## Measured gap

The operator-owned LightX2V path already bound source revision, generation config bytes, generation request bytes, rights-safe reference bytes and generated-video bytes. `model_path`, however, was only checked for local directory existence. A local weight/config file under that model tree could therefore change while a shot was being generated without invalidating the result, and the artifact manifest could not prove which exact local model bytes produced the shot.

This matters directly to Production v0.2: a generated MP4 is not reproducible evidence unless the local model asset that produced it is independently byte-bound alongside source/config/request/reference/output provenance.

## TDD evidence

RED exact head: `2d80289278b8ba73ef7203de517458a24f18f309`.

CI #2611 reached Ruff successfully. Python 3.12 pytest produced exactly `2 failed, 646 passed`:

- manifest had no `generation_model_sha256` field;
- changing `weights.bin` during generation did not raise `LightX2VError`.

Python 3.11 was cancelled by fail-fast after the 3.12 failure, so it is not claimed as independent RED evidence.

GREEN exact head: `106cda9f05433252938a9f17a0c861c93c2ae8e3`.

- CI #2613 passed Python 3.11 and 3.12.
- production-smoke #303 passed checked-in cow + Odyssey generation, final-media/provenance verification and evidence upload. Artifact `hottop-software3d-production-smoke`: 688,374 bytes, digest `sha256:53d0dca4aaf6a3c4b92cb5cf499ef2e816127eef846f8cdd94dd3267c77c5538`.
- cinematic-delivery-smoke #170 passed actual 720p24 Odyssey delivery, runtime provenance, final-media verification and evidence upload. Artifact `hottop-cinematic-software3d-delivery`: 623,331 bytes, digest `sha256:8d99e56be002e4ebf6606195fd5db488c2ea495bc697fbad95f1f330ab9e5ec5`.

PR #381 was SHA-locked to that exact GREEN head and squash-merged as `82e0c73abe78be1d75ac7689654ae58a3202aa51`.

## Implemented contract

For an already-provisioned local `model_path`, Hottop now computes a deterministic tree identity before GPU generation:

1. enumerate local regular files recursively;
2. sort by relative POSIX path;
3. bind each logical path length + path bytes + file-size metadata + actual file bytes into SHA-256;
4. record the total model-file bytes read;
5. after generation, compute the same identity again before accepting the output;
6. if digest or byte count changed, delete the generated output and fail closed;
7. when an artifact manifest is requested, record `generation_model_sha256` and `generation_model_size_bytes` next to source/config/request/reference/output provenance.

The operation is local and read-only. It does not install LightX2V, contact Hugging Face, download models, provision a GPU, invoke a hosted endpoint or consume credits. The added cost is local storage I/O before and after an operator-owned generation run.

## Security and provenance boundary

This proves the exact regular-file bytes visible under the configured local model directory at the two verification points. It does not claim that a model is semantically correct, safe, high quality or licensed merely because its bytes are stable. Code license and weight/model/data license remain distinct admission dimensions; operator review is still required before provisioning those assets.

The existing semantic boundary also remains: successful execution, byte stability, decodability, media quality and generic motion do not prove subject identity or requested action.

## Ecosystem radar

- The official Wan2.2-I2V-A14B model repository continues to present an Apache-2.0 license, but exact model revision/bytes still have to be bound locally for Hottop evidence.
- Upstream LightX2V reports still show that technically successful runs can produce static, degraded or meaningless content; model-byte identity therefore complements rather than replaces identity/action/semantic gates.
- Recent Qwen3-TTS serving work reports measurable Mandarin CER improvements, but Hottop still needs same-line operator-owned local A/B evidence plus exact runtime/model provenance before changing the prepared TTS route.

No candidate justified auto-installation, a paid fallback, a large unattended download or a freshness-only pin in this cycle.

## Rollback

Rollback is narrow: revert PR #381. That removes model-tree hashing and the two optional manifest fields without changing software3d, MoviePy, FFmpeg, audio routing, zero-cost behavior or the LightX2V command surface.

## Doctrine decision

`PROJECT.md` is intentionally unchanged. Exact model-byte binding is a stricter implementation of the existing artifact/provenance and fail-closed operator-owned doctrine, not a new durable product direction.
