# LightX2V generation-request provenance closure — 2026-08-31

## Measured gap

The operator-owned LightX2V route already bound accepted output bytes, actual local generator source revision, exact generation-config bytes, and (for I2V) exact rights-safe reference bytes. It did not bind the exact request semantics passed to inference: prompt, negative prompt, task, model class and seed. That left a reproducibility/evidence gap: two materially different inference requests could share the same source/config/reference provenance shape.

During review of this path, the CLI exposed a directly related correctness bug: `--seed` was parsed but not forwarded into `LightX2VAdapterConfig`, so any explicit non-default CLI seed was silently replaced by the adapter default `42`.

## Change

Accepted LightX2V shot artifacts now optionally carry `generation_request_sha256` plus `generation_request_size_bytes`. The adapter computes these from canonical UTF-8 JSON with schema `hottop.lightx2v-generation-request.v1` over:

- `model_cls`;
- `task`;
- `seed`;
- `prompt`;
- `negative_prompt`.

Canonical serialization uses sorted keys, compact separators and `ensure_ascii=false`. The manifest stores the digest/byte-count pair rather than duplicating prompt text. Existing artifact manifests remain backward compatible because the new pair is optional at the generic schema level; LightX2V writes it for newly accepted artifacts.

The CLI now forwards `--seed` into `LightX2VAdapterConfig`, so the request digest and actual inference command agree on explicit operator seed choice.

## TDD evidence

RED head `072e77df9bc07734305170e1b21ea35fa99fe333` added the request-binding contract before implementation. CI #2539 failed exactly at `test_lightx2v_artifact_manifest_binds_exact_generation_request` with `KeyError: 'generation_request_sha256'`; Ruff passed and the suite reported `1 failed, 626 passed` on Python 3.11 before fail-fast cancellation of the sibling matrix job.

GREEN implementation added the request identity pair, schema validation, manifest persistence and explicit CLI seed forwarding. Exact-head CI and production smoke evidence are recorded in `STATUS.md` after the final documentation head is verified.

## Doctrine impact

This is an implementation-level strengthening of existing provenance doctrine, not a provider-strategy change. `PROJECT.md` already requires bound source/plan/provenance, archived prompts and fail-closed generated-media evidence, so no canonical direction change is required.

The new digest does **not** prove model/checkpoint identity, output identity continuity, requested-action motion fidelity, semantics or visual quality. Those remain independent dimensions. It also adds no network call, provider, model download, paid dependency, auto-install path or GPU provisioning.

## Fresh upstream check

ModelTC/LightX2V public `main` advanced again on 2026-08-31 to `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` (11:57 UTC). The tip restores SeedVR distributed-op exports and reports SeedVR2 BF16/FP8 validation; its parent `7d6df6659a332ce09d43860eef5321e7dc7e36ed` is CI/lint behavior. These changes do not provide Hottop-measured Wan2.2 I2V identity, requested-action motion, continuity or output-quality gain, so they do not justify a freshness-only repin of Hottop's tested LightX2V route.
