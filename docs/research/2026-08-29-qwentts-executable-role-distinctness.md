# qwentts.cpp executable/model role distinctness — 2026-08-29

## Finding

Hottop's read-only qwentts.cpp operator preflight already required the talker GGUF and tokenizer/codec GGUF to be different resolved targets with different exact bytes. A remaining input-set provenance gap allowed the **qwentts executable itself** to be reused as either model artifact when the reused file happened to be executable and structurally GGUF-like.

That state is not a valid benchmark input topology. The executable, talker model and tokenizer/codec model are three semantically different runtime roles. Passing each artifact's role-local checks independently is insufficient when the same concrete artifact can satisfy incompatible roles.

## TDD evidence

- RED `92f0337d2b964c7a7ae665616aa8b9fc58f5af41` → CI #2068: Ruff passed; pytest failed on the new executable/model role-distinctness contract.
- GREEN `0d346443ae86f4d0accbba50ed8f1f4326806c46` → CI #2069: Python 3.11/3.12 Ruff + full pytest passed.

## New contract

`inspect_qwentts_cpp_inputs()` now fails closed when the qwentts executable and either GGUF model input share the same resolved path **or** the same exact SHA-256 bytes.

The existing protections remain unchanged:

- resolve each path to one concrete target before identity binding;
- require non-empty local files and executable permission for the runtime binary;
- require the complete 24-byte fixed GGUF header surface for model inputs;
- stream exact SHA-256 in bounded 1 MiB chunks;
- compare before/after device, inode, size, mtime_ns, ctime_ns and mode to reject mutation during hashing;
- reject talker/tokenizer same-path or same-byte reuse;
- do not run qwentts.cpp, access the network, download/build anything, provision GPU resources, use credentials or promote model-hub runtime status.

`ready=true` therefore means only that the operator supplied a stable, byte-bound, structurally GGUF-like and **role-distinct executable/talker/tokenizer input set**. It still does not prove checkpoint identity, checkpoint or output rights, preset-speaker capability, qwentts runtime compatibility, synthesis success or Mandarin quality.

## Upstream and radar context

The reviewed qwentts.cpp source remains `ServeurpersoCom/qwentts.cpp@a8a7716b530e49fed537c57711247c12fbbb903c`, where the documented topology separates the executable runtime from `--model` talker and `--codec` tokenizer/codec artifacts.

The 2026-08-29 targeted TTS scan also found additional local/community Qwen3-TTS runtimes, including ONNX and containerized wrappers. None currently beats the already reviewed qwentts.cpp 1.7B CustomVoice path for Hottop's measured gap while also improving its zero-cost/operator-controlled admission boundary. Several wrappers auto-download models or target different checkpoint capabilities, so no new runtime was admitted in this workstream.

## Reuse rule

When a benchmark/runtime consumes multiple operator-supplied artifacts with different semantic roles, preflight must validate **cross-role relationships** in addition to each artifact independently. Role-distinctness that can be proven from resolved path and exact bytes should fail closed before execution; deeper semantic model identity remains a separate later gate rather than something inferred from filenames.