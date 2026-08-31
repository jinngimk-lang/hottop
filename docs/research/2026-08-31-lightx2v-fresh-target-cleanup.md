# LightX2V fresh-target cleanup evidence — 2026-08-31

## Measured gap

`run_lightx2v_shot()` previously invalidated the requested MP4 and artifact manifest only after local LightX2V preflight. A fresh invocation that failed earlier — for example because the operator-managed model path was missing — could therefore leave bytes from a previous successful run at the same target paths. Those stale bytes were not produced by the failed invocation and must not survive as plausible current evidence.

## Accepted contract

A fresh LightX2V invocation now resolves and removes the requested output path, and removes the optional artifact-manifest path, before local preflight. Any later preflight or generation failure therefore cannot leave an older MP4/manifest pair at the requested targets. This is evidence-integrity closure under the existing fail-closed operator-owned doctrine; it does not add a provider, network surface, download path, paid fallback or weaker quality gate.

## TDD and production evidence

- RED commit `ff80188c7cd70d12c7c459177325076148738c96`: CI #2554 failed the new stale-target cleanup regression contract against the old implementation.
- GREEN commit `b393171deecdca600a6a21b867571da2e8802578`: exact-head CI #2555 succeeded.
- The same GREEN head passed production-smoke #275, executing the checked-in anti-polish cow and cinematic Odyssey zero-cost production paths and their final-media/provenance verification.
- The same GREEN head passed cinematic-delivery-smoke #142, executing the 720p24 Odyssey delivery plus runtime provenance, final-media verification and evidence upload.
- Draft PR #360 preserved the RED/GREEN history. The connected Ready-for-review mutation failed with a connector-side GraphQL schema error, while GitHub REST correctly refused merging a draft. The unchanged verified head was therefore reopened as non-draft PR #361 and SHA-locked squash-merged as `3489a9321a0cdeb3708a652c88cb2d5e408fc000`.

## Ecosystem radar

LightX2V public `main` remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f` (2026-08-31 11:57:20 UTC). Its tip restores SeedVR distributed operations and reports SeedVR2 BF16/FP8 validation; it supplies no Hottop-measured Wan2.2 I2V identity, requested-motion, continuity or output-quality gain, so there is still no evidence for a freshness-only repin.

`5uck1ess/tts-bench` was also reviewed as a TTS benchmark-harness candidate. Its benchmark code is MIT, while its LICENSE explicitly separates model licensing from harness licensing. The repository/install surface is large and it does not yet beat Hottop's existing provenance/coherence benchmark contract on measured project evidence, so it remains radar-only and is not auto-installed or vendored.

## Durable-doctrine decision

`PROJECT.md` remains unchanged. Removing stale targets before a fresh fail-closed execution is a direct implementation of the already-canonical artifact-byte/provenance and fail-closed principles, not a new durable project direction.

## Remaining production boundary

The next true LightX2V quality milestone remains real generated media. When a reviewed local LightX2V checkout, Wan2.2 model and suitable operator GPU are actually provisioned, execute rights-safe multi-shot I2V and require complete byte-bound identity, requested-action motion, media quality, source/config/request/reference provenance and final composition verification. No model or large runtime is auto-provisioned by normal `video-run` or CI.
