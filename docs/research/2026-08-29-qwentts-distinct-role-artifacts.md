# qwentts.cpp distinct model-role artifact preflight — 2026-08-29

## Finding

The reviewed qwentts.cpp runtime loads two different GGUF model roles together: a **talker** model through `--model` and a shared **tokenizer/codec** model through `--codec`. Hottop's read-only operator preflight previously validated each supplied GGUF independently, so the same valid GGUF path—or the same exact bytes copied under two filenames—could satisfy both inputs and incorrectly produce `ready=true`.

This is an input-set provenance defect, not an audio-quality defect: every individual file can be locally present, stable, structurally GGUF-like and exact-byte-bound while the set as a whole is still invalid for the intended runtime topology.

## TDD evidence

- RED `3ff5c34a770aa48be0ebf6c94b042b7656afcde7` → CI #2059: Ruff passed; pytest failed on the new distinct-role contract.
- GREEN `3baeddfad9b4167f449e9ddc0bf0d291364d673e` → CI #2060: Python 3.11/3.12 Ruff + full pytest passed.
- Exact-head PR was squash-merged as `719f5b35660a49baa4724b9ea6b741c1d4f1c273`.

## New contract

`inspect_qwentts_cpp_inputs()` now fails closed when the talker and tokenizer/codec identities resolve to the same path **or** have the same exact SHA-256 bytes.

The existing protections remain unchanged:

- each path is resolved to one concrete target before identity binding;
- files must be present and non-empty;
- the qwentts executable must be executable;
- GGUF inputs must expose the complete 24-byte fixed-header surface;
- exact SHA-256 is streamed in bounded 1 MiB chunks;
- before/after filesystem signatures protect against mutation during hashing;
- no qwentts execution, network access, build, model download, GPU provisioning, credential use or runtime-ready promotion occurs.

`ready=true` therefore means only that the operator supplied a stable, byte-bound **and role-distinct** benchmark input set. It still does not prove semantic checkpoint identity, model/tokenizer rights, speaker capability, runtime compatibility, synthesis success or Mandarin quality.

## Upstream provenance

Reviewed qwentts.cpp source remains `ServeurpersoCom/qwentts.cpp@a8a7716b530e49fed537c57711247c12fbbb903c`. At that revision, upstream documents separate `--model` talker and `--codec` tokenizer/codec GGUF inputs and its CustomVoice examples use different talker and tokenizer artifacts.

## Reuse rule

For future multi-artifact operator preflights, validating each artifact independently is insufficient when the runtime assigns semantically different roles. The **input set** must also enforce role relationships that can be proved without executing the model. This does not justify deep model parsing or guessing model identity from filenames; exact semantic identity remains a later, separately evidenced gate.