# FFprobe metadata shape integrity — 2026-09-01

## Measured gap

`inspect_video_quality()` already rejected invalid JSON, non-finite metadata, malformed dimensions, incomplete terminal frames and incomplete motion samples. But syntactically valid JSON could still have structurally invalid ffprobe containers: a top-level list, a non-object `format`, or non-object entries in `streams`. Those shapes could raise during `.get(...)` access or be misclassified instead of producing a deterministic rejection report.

Production v0.2 treats malformed generated-media metadata as failed evidence, never as an exception path.

## TDD and production evidence

- RED head `905fa77748f315c6de44936167d250741f48aba5`, CI #2606: installation and Ruff succeeded; Python 3.11 pytest failed on the new malformed-shape regression before the implementation commit. The Python 3.12 job was cancelled after the branch advanced, so the RED claim is intentionally limited to the independently observed 3.11 failure.
- GREEN head `63c5b0a91efbb895535232f0f4d56e6acbb38cde`, CI #2607: exact-head CI passed.
- production-smoke #300 passed the checked-in anti-polish cow + cinematic Odyssey production path and final-media/provenance verification. Artifact `hottop-software3d-production-smoke`: 687,894 bytes, digest `sha256:363ed3091f79cdb2599a702df8faa3381fe7f3e706b32acab5858a969767614c`.
- cinematic-delivery-smoke #167 passed the exact same implementation head through actual 720p24 Odyssey delivery, runtime provenance and final-media verification. Artifact `hottop-cinematic-software3d-delivery`: 624,448 bytes, digest `sha256:95e5c9a29b91c9155688ff61906b32aacfbf110457abe96d49ceea19e5842b50`.
- PR #379 was SHA-locked to the exact GREEN head and squash-merged as `b7899e066ec743008d185ee532ef7dab32da7288`.

## Change

The inspector now validates the ffprobe metadata container contract before consuming values:

- top-level metadata must be an object;
- `format` must be an object;
- `streams` must be a list;
- every stream entry must be an object.

Any structural mismatch returns `pass_=false` with `ffprobe metadata structure invalid` before duration, dimensions, terminal-frame or motion decoding. Valid metadata keeps all existing floors and motion/integrity checks unchanged.

## Doctrine / rollback

This is implementation hardening of the existing generated-media/final-media integrity doctrine. It does not alter provider routing, model selection, network behavior, ZERO_COST policy, creative style or quality thresholds, so `PROJECT.md` remains unchanged.

Rollback is the single PR #379 squash merge if a legitimate ffprobe representation is later demonstrated to violate the assumed object/list structure; any relaxation must first have a regression fixture and equivalent fail-closed semantics.

## Radar context

LightX2V public tip remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; its latest material work is still SeedVR distributed-operation repair rather than a Hottop-measured Wan2.2 I2V identity/requested-action improvement. No freshness-only repin is justified.

The audio serving ecosystem has fresher operator-owned candidates, including Apache-2.0 SGLang-Omni support for Qwen3-TTS/CosyVoice-family serving, but serving-code license does not settle model/weight licenses and no Hottop same-line Mandarin quality/latency/provenance win has yet been measured. It remains gated rather than auto-installed or admitted.
