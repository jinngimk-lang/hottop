# qwentts.cpp preflight snapshot stability — 2026-08-29

## Decision

The read-only qwentts.cpp operator preflight must bind a **stable local artifact snapshot**, not merely a path, a size sampled before hashing, and a SHA-256 sampled later.

A local executable or GGUF that changes while its digest is being streamed is fail-closed with `ready=false`. Hottop must not emit a mixed provenance identity such as an old `size_bytes` combined with a digest of different bytes.

This strengthens the existing bounded-memory artifact-binding contract. It does not execute qwentts.cpp, access the network, download or build dependencies, provision GPU/CPU resources, change model-hub runtime status, or claim Mandarin quality.

## Why this was needed

The original preflight flow sampled `Path.stat().st_size` before streaming SHA-256. If an operator-managed multi-GB artifact was replaced, appended, truncated, or had its executable/file identity changed during hashing, the returned record could describe no single stable filesystem state.

That is a provenance-integrity problem even when the final digest is cryptographically correct: a digest is only useful when the other identity fields describe the same bytes.

## TDD evidence

- RED head: `53e4cb2e90a7b4029c1ab735003357f62792bf05`
- RED CI: #2042 — Ruff passed; Python 3.11 pytest failed on the new mutation-during-preflight contract; Python 3.12 was cancelled by fail-fast.
- GREEN implementation head: `6befa6cc43fa9a10dc110371a082df3d4adf2fb8`
- GREEN CI: #2043 — Python 3.11 and 3.12 both passed Ruff and the full pytest suite.

The regression mutates the talker GGUF immediately after its bytes are streamed. The previous code returned `ready=true`; the GREEN returns `ready=false` with an explicit `changed during preflight` blocker.

## Stable-snapshot contract

For each local preflight artifact, Hottop now compares filesystem signatures before and after streaming the digest. The signature includes:

- device id;
- inode;
- byte size;
- nanosecond modification time;
- nanosecond change time;
- file mode.

Any mismatch fails closed and no `LocalArtifactIdentity` is emitted for that unstable artifact. Read errors caused by disappearance/replacement during preflight fail closed through the same boundary.

The SHA-256 remains streamed in bounded chunks, and GGUF validation remains deliberately shallow: a complete fixed header plus exact bytes is an artifact-structure/provenance check, not a checkpoint parser.

### Symlink target binding

A later closure found that a stable byte snapshot was still insufficient when an operator supplied a symlink. The old flow stat'ed and hashed through the symlink, but called `Path.resolve()` only while constructing the final identity. A symlink retargeted after the second snapshot could therefore produce a mixed record: SHA-256 and size from the original target, but a canonical path naming the replacement target.

The preflight now resolves the supplied path to its concrete target **before** stat, hash, executable/header checks, and final identity construction. All byte and metadata checks operate on that same resolved target, so a later retarget of the symlink itself cannot rewrite the path associated with already-hashed bytes. Legitimate operator-managed symlinks remain supported; the contract binds the target that was selected at preflight start rather than rejecting symlinks categorically.

TDD evidence for this closure:

- RED head: `5b3ced7f8ef6152971453bb0678cc2799a469aaf`
- RED CI: #2052 — Ruff passed; Python 3.11 pytest failed on the symlink-retarget provenance contract.
- GREEN implementation head: `a9ab34ecadad3de329fa5140af1c9c9a4f8dab85`
- GREEN CI: #2053 — Python 3.11 and 3.12 both passed Ruff and the full pytest suite.

## Scope and non-claims

`ready=true` still means only that the supplied executable and GGUF-like inputs were present, locally readable, structurally acceptable to the shallow gate, stable during the preflight window, and byte-bound.

It does **not** prove:

- that the GGUFs contain the expected Qwen3-TTS checkpoint;
- checkpoint, preset-speaker, or output-publication rights;
- qwentts.cpp runtime compatibility on the operator machine;
- successful synthesis;
- Mandarin intelligibility, naturalness, onset stability, speaker consistency, latency, or RTF.

The actual 1.7B same-line Mandarin A/B remains blocked until an operator provisions the reviewed local runtime and exact GGUF assets.