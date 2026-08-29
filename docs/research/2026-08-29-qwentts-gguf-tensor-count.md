# qwentts.cpp GGUF tensor-count preflight hardening

Date: 2026-08-29

## Context

Hottop's read-only `qwentts.cpp` operator preflight is deliberately narrower than model execution. It exists to bind operator-provisioned local benchmark inputs before any separate Mandarin A/B run, while preserving `ZERO_COST_MODE=true` and the project's no-auto-download/no-auto-build/no-GPU-provisioning boundaries.

Before this change, a non-empty model artifact passed the shallow GGUF structure gate when it had:

- the `GGUF` magic;
- a complete 24-byte fixed header;
- stable before/after filesystem identity;
- a bounded-memory SHA-256 identity;
- a runtime role distinct from the executable and the other model GGUF.

That still admitted a header-shaped artifact whose GGUF `tensor_count` was zero.

## RED

PR #203 first corrected the test fixtures so a fixture intended to represent a usable model declares one tensor, then added an explicit zero-tensor fixture.

Exact RED head:

- `1f8a2b4cc35dcd8d0ae954d95cb65845e58ad88a`
- CI #2076: Ruff passed; pytest failed on the new zero-tensor contract.

This demonstrated that a structurally header-shaped, zero-tensor model input could previously reach `ready=true`.

## GREEN

The implementation now reads the GGUF `tensor_count` directly from bytes 8–15 of the already captured 24-byte fixed header and rejects `tensor_count == 0`.

No extra file read is introduced. The existing 1 MiB streaming SHA-256 remains the artifact-binding mechanism, and the check does not parse GGUF metadata.

A first full-suite GREEN attempt then exposed two older test fixtures that still encoded `tensor_count=0` while intending to represent valid model artifacts. Those fixtures were corrected to one tensor; the production gate was not weakened.

Final exact GREEN head:

- `d57a8ada9eeea5bb014a11c7fc374615d57468b7`
- CI #2079: Python 3.11 and 3.12 both passed Ruff and the full pytest suite.

## Boundary

This remains a **shallow structural preflight**, not semantic model verification.

`ready=true` still does **not** prove:

- that the GGUF contains the expected Qwen3-TTS checkpoint;
- that talker/tokenizer mode or size matches the intended benchmark;
- source/model/tokenizer/checkpoint license or commercial rights;
- that `qwentts.cpp` can initialize or synthesize successfully;
- checkpoint/runtime speaker capability;
- Mandarin intelligibility, onset stability, speaker consistency, naturalness, latency, or RTF.

The operator benchmark must continue to bind exact source/build/backend, talker/tokenizer bytes, text, speaker, generation controls, and output WAV bytes, then apply PCM integrity, duration, repeat-speaker, onset and listening/quality evidence separately.

## Why the gate is intentionally small

The GGUF fixed header already exposes `tensor_count`, so rejecting zero tensors removes an impossible-model false positive without adding metadata parsing, new dependencies, model execution, network access, large-memory reads, downloads, builds, GPU provisioning, credentials, or paid behavior.

Reference: the GGUF fixed-header layout is defined by the ggml/GGUF specification: magic, version, `tensor_count`, then metadata key/value count.
