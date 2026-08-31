# tts-bench method admission — 2026-08-30

## Decision

Admit **benchmark methodology only** from `5uck1ess/tts-bench`; do not vendor or execute its installer/model stack in unattended Hottop.

Reviewed source:

- repository: `5uck1ess/tts-bench`
- exact revision: `020a69422c96224785a8dc4b95466676119a7dc2`
- reviewed date: 2026-08-30
- bench-code license: MIT; the repository LICENSE explicitly says this license applies only to the benchmark code and each TTS model keeps its own license.

## Why it matters to Hottop

Production v0.2 already has fail-closed local artifact preflights for qwentts.cpp, CrispASR and audio.cpp Qwen3-TTS candidates. The next operator benchmark needs a shared evidence surface after those runtimes produce WAVs, rather than another provider adapter.

The useful design signal from tts-bench is the separation of:

1. **speed evidence** — cold/warm timing and realtime factor;
2. **artifact/objective evidence** — audio bytes plus measurable stream/quality metadata;
3. **listening/preference evidence** — a separate human-facing dimension rather than pretending one aggregate metric proves naturalness.

The upstream project itself withdrew a prototype aggregate objective quality score when it did not track subjective ranking closely enough. Hottop therefore must not collapse Mandarin naturalness, speaker consistency, onset stability or intelligibility into a single speed/PCM score.

## Rejected integration surface

The upstream quick-start is not admissible for normal Hottop execution:

- it reports roughly 39 GB of per-model virtual environments plus roughly 125 GB of Hugging Face model weights for the full suite;
- installers can fetch/build model-specific dependencies and acceleration kernels;
- benchmarked models have independent licenses and runtime requirements;
- cloning paths can require reference audio and therefore separate rights review.

Hottop must not invoke those installers, auto-download their model set, or infer model rights from the MIT benchmark-code license.

## Hottop integration

Hottop independently implements a narrow, provider-neutral local evidence inspector:

`hottop-models inspect-tts-benchmark --spec <benchmark.json>`

It reads only an operator-authored JSON spec and already-produced local WAV files. It does not execute TTS, access the network, install dependencies, download models, provision GPU resources or invoke paid services.

The v1 evidence contract binds:

- exact benchmark text, language and preset speaker label;
- **one explicit generation protocol for the whole benchmark** — operator-authored seed, sampling controls, generation ceiling and any other settings required to make the compared runs semantically equivalent; the protocol must be non-empty finite JSON, must contain an integer `seed`, a positive integer `max_new_tokens` generation ceiling and at least one explicit sampling control (`temperature`, `top_p`, `top_k` or a nonblank `sampling_mode`), is canonicalized with sorted keys and is preserved with a SHA-256 digest in the evidence; greedy sampling remains representable with `temperature=0`;
- **one explicit hardware profile for the whole benchmark** — operator-authored CPU/GPU/backend/count/runtime-environment facts needed to interpret latency and realtime-factor comparisons; the profile must be non-empty finite JSON, must name one currently understood backend class (`cpu`, `cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps` or `xpu`), and must include at least one concrete nonblank device identity under `cpu`, `gpu` or generic `accelerator`; it is canonicalized with sorted keys and preserved with a SHA-256 digest in the evidence;
- candidate/runtime/model revision and cold/warm trial identity;
- **per-candidate runtime identity**: every trial grouped under one candidate label must use the same exact `runtime_revision`; comparing two runtime revisions requires two distinct candidate identities instead of mixing binaries/builds under one label;
- **per-candidate model identity**: every trial grouped under one candidate label must use the same exact `model_revision`; comparing two checkpoint/model revisions requires two distinct candidate identities instead of silently mixing model artifacts under one label;
- **per-candidate cold/warm coverage**: every candidate must provide at least one `cold` trial and at least one `warm` trial before the benchmark can be `ready=true`;
- repeated trials remain first-class evidence: one cold plus multiple independent warm trials is valid and preferred when measuring repeated-run speaker consistency or warmed-runtime variance;
- exact WAV path, SHA-256 and size;
- sample rate, channels, sample width, frame count and duration;
- digital-silence rejection;
- positive finite measured latency and derived realtime factor;
- an explicit `listening_required=true` marker so speed/stream integrity cannot be mistaken for naturalness or speaker-quality proof.

A benchmark trial is an artifact instance, not merely a row label. Two trial rows must not reuse the same **resolved WAV path**, because one physical artifact cannot prove two independently produced executions. This is intentionally narrower than byte uniqueness: two independently produced files may have identical SHA-256 bytes, and that byte equality is useful deterministic repeatability evidence rather than a failure.

The generation protocol is a **declared benchmark-control contract**, not proof that a runtime internally obeyed a flag. It closes a concrete evidence-coherence hole by preventing a ready benchmark from omitting seed/sampling/generation-ceiling identity altogether or substituting descriptive metadata such as `{ "note": "same settings" }`. Operator execution records should still retain the actual CLI/config provenance for each runtime; incompatible semantics across runtimes require separate candidate/protocol design rather than pretending similarly named flags are equivalent.

The hardware profile is likewise a **declared measurement-environment contract**, not proof that the declared hardware was actually used. It prevents speed evidence from becoming `ready=true` with no usable hardware identity or with an undefined execution class. Requiring one of the currently understood backend classes plus a CPU/GPU/generic-accelerator identity keeps device identity provider-neutral while preventing arbitrary labels from acquiring benchmark semantics. A future backend class must enter through an explicit contract/evidence update instead of becoming comparable merely because it is a nonblank string. Operator execution records should still preserve independent runtime/environment provenance where available. If candidates are intentionally measured on different hardware, they belong in separate benchmark evidence sets rather than one directly comparable latency/RTF surface.

Cold/warm coverage is a benchmark-completeness gate, not a claim that one cold and one warm sample are sufficient for production quality. Runtime- and model-revision consistency are evidence-coherence gates: they prevent cold/warm or repeated-trial results from silently crossing implementation or checkpoint revisions. Future operator Qwen3-TTS 1.7B A/B runs should pair this artifact evidence with multiple warm repeats plus the already-required repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights review.

### 2026-08-30 closure evidence

A first TDD contract demonstrated that the previous inspector could report `ready=true` for a candidate represented only by a single warm trial. RED CI #2241 failed on the new coverage contract after Ruff passed. The minimal implementation groups trials by candidate, requires `{cold, warm}` coverage, and deliberately allows additional warm repeats. Exact-head CI #2243 passed Ruff and the full pytest suite on Python 3.11 and 3.12; the durable-record head then passed CI #2244, and the merged main passed CI #2246.

A second TDD contract demonstrated that a candidate could satisfy cold/warm coverage while mixing `runtime_revision=audio.cpp@abc` and `audio.cpp@def`. RED CI #2249 passed Ruff and failed pytest on the new provenance contract. The minimal implementation groups runtime revisions by candidate and fails closed when a candidate label spans more than one revision. GREEN CI #2250 passed the full pytest suite on both Python 3.11 and 3.12 before the durable-record update.

A third TDD contract demonstrated that a candidate could preserve one runtime revision while mixing two model/checkpoint revisions across cold and warm trials. RED CI #2256 passed Ruff and failed pytest on the new model-coherence contract. The minimal implementation promotes `model_revision` to required trial/evidence data, groups model revisions by candidate and fails closed when one candidate label spans multiple model revisions. GREEN CI #2261 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

A fourth TDD contract demonstrated that the benchmark could be `ready=true` without binding seed, sampling or generation-ceiling settings at all. RED CI #2269 passed Ruff and failed pytest after adding the new generation-protocol contract. The minimal implementation requires one non-empty finite JSON `generation_protocol` for the full benchmark, preserves it in evidence and binds its canonical sorted-key JSON bytes with SHA-256. Existing ready fixtures were updated to declare the same protocol rather than weakening the gate. Exact-head GREEN CI #2274 passed Ruff and the full pytest suite on Python 3.11 and 3.12; the merged main then passed CI #2277.

A fifth TDD contract demonstrated that latency/RTF evidence could become `ready=true` while omitting hardware identity entirely. RED CI #2280 passed Ruff and failed pytest on the new hardware-profile contract. The minimal implementation requires one non-empty finite JSON `hardware_profile` for the whole benchmark, preserves it in evidence and binds its canonical sorted-key JSON bytes with SHA-256. Existing ready fixtures were updated to declare a shared profile rather than weakening the gate. Exact-head GREEN CI #2285 passed Ruff and the full pytest suite on Python 3.11 and 3.12; merged main then passed CI #2288.

A sixth TDD contract showed that merely requiring a non-empty `hardware_profile` still permitted false-ready latency/RTF evidence such as `{ "note": "same machine" }` or a profile with a CPU label but no execution backend. RED CI #2289 passed Ruff and failed pytest on concrete hardware-identity contracts. The minimal implementation now requires a nonblank `backend` plus at least one nonblank device identity under `cpu`, `gpu` or generic `accelerator`; the generic form deliberately keeps Vulkan/MPS/XPU and future operator backends representable without hard-coding a vendor taxonomy. Exact-head GREEN CI #2290 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

A seventh TDD contract showed that a non-empty but purely descriptive `generation_protocol`, for example `{ "note": "same settings" }`, could still become `ready=true` even though it bound none of the controls needed for a comparable generation run. RED CI #2296 passed Ruff and failed pytest on the new concrete-control contract. The minimal implementation now requires an integer `seed`, a positive integer `max_new_tokens` ceiling and at least one explicit sampling control, while validating present `temperature`, `top_p`, `top_k` and `sampling_mode` values and preserving `temperature=0` as an explicit greedy protocol. Exact-head GREEN CI #2297 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

An eighth TDD contract showed that an arbitrary nonblank backend such as `banana` could still become `ready=true` when paired with a generic accelerator label, giving undefined hardware classes comparable latency/RTF semantics. The first test-only run was stopped by lint and was not treated as behavioral RED. Corrected RED CI #2421 passed Ruff and failed pytest on the unknown-backend contract. The minimal implementation closes the vocabulary to `cpu`, `cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps` and `xpu`; generic `accelerator` remains available for device identity within those execution classes. GREEN CI #2422 passed Ruff and the full pytest suite on Python 3.11 and 3.12.

## Re-admission / expansion gate

Do not adopt more of tts-bench merely because it is popular or actively maintained. Add another benchmark dimension only when it closes a measured Hottop evidence gap, its dependencies/licenses are independently reviewed, and it can be kept isolated from unattended model download/provisioning.