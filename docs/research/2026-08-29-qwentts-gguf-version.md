# qwentts.cpp GGUF version preflight gate — 2026-08-29

## Context

Hottop's read-only qwentts.cpp operator preflight already bound local executable/talker/tokenizer artifacts by resolved path, byte size and streaming SHA-256, required a complete 24-byte GGUF fixed header, rejected zero-tensor model inputs, protected against filesystem mutation during hashing, and kept incompatible runtime roles byte/path-distinct.

A remaining false-ready condition existed in the same fixed header: the preflight did not inspect the 32-bit GGUF version field. An artifact could therefore present `GGUF` magic, a complete fixed-header shape and `tensor_count > 0` while declaring an unsupported version such as `99`, yet still report `ready=true`.

## Upstream evidence

The reviewed ggml GGUF header defines the order `magic -> version -> tensor count -> key/value count`, and current upstream `ggml/include/gguf.h` defines `GGUF_VERSION 3`.

This work deliberately uses only that fixed-header fact. It does not parse metadata, tensor descriptors or model architecture, and it does not claim semantic checkpoint identity.

## TDD evidence

- RED `4d9808abea46776208f40832639b7b59b2af933e` -> CI #2085: Ruff passed; pytest failed on the new unsupported-version contract. Python 3.12 was cancelled by fail-fast after the 3.11 failure.
- GREEN `8ad53aa3d09d5c9c0ba617dd7cc2025f4d5b4076` -> CI #2086: Python 3.11 and 3.12 both passed Ruff + full pytest.

## Contract

For talker/tokenizer GGUF inputs, the shallow local preflight now requires:

- correct `GGUF` magic;
- at least the complete 24-byte fixed header;
- fixed-header version exactly `3` for the currently reviewed qwentts/ggml route;
- `tensor_count > 0`;
- bounded-memory streaming SHA-256 and stable before/after filesystem identity;
- resolved-target provenance and incompatible runtime-role distinctness.

`ready=true` still means only that operator-provided local benchmark inputs passed these shallow structure/provenance checks. It does **not** prove checkpoint identity, model/tokenizer rights, qwentts runtime compatibility, supported speaker conditioning, synthesis success or Mandarin quality.

## Safety / cost boundary

No qwentts execution, network access, model download, dependency build/install, GPU provisioning, credential use, paid API or runtime-ready promotion is added by this gate.

## Future compatibility

If the reviewed qwentts/ggml runtime later supports a new GGUF format version, Hottop must update the accepted version only alongside exact upstream/runtime evidence and a regression test. Do not widen the version set merely because a file has plausible bytes.
