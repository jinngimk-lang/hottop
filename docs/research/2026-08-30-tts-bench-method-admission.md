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
- candidate/runtime revision and cold/warm trial identity;
- **per-candidate runtime identity**: every trial grouped under one candidate label must use the same exact `runtime_revision`; comparing two revisions requires two distinct candidate identities instead of mixing binaries/builds under one label;
- **per-candidate cold/warm coverage**: every candidate must provide at least one `cold` trial and at least one `warm` trial before the benchmark can be `ready=true`;
- repeated trials remain first-class evidence: one cold plus multiple independent warm trials is valid and preferred when measuring repeated-run speaker consistency or warmed-runtime variance;
- exact WAV path, SHA-256 and size;
- sample rate, channels, sample width, frame count and duration;
- digital-silence rejection;
- positive finite measured latency and derived realtime factor;
- an explicit `listening_required=true` marker so speed/stream integrity cannot be mistaken for naturalness or speaker-quality proof.

A benchmark trial is an artifact instance, not merely a row label. Two trial rows must not reuse the same **resolved WAV path**, because one physical artifact cannot prove two independently produced executions. This is intentionally narrower than byte uniqueness: two independently produced files may have identical SHA-256 bytes, and that byte equality is useful deterministic repeatability evidence rather than a failure.

Cold/warm coverage is a benchmark-completeness gate, not a claim that one cold and one warm sample are sufficient for production quality. Runtime-revision consistency is likewise an evidence-coherence gate: it prevents cold/warm or repeated-trial results from silently crossing implementation revisions. Future operator Qwen3-TTS 1.7B A/B runs should pair this artifact evidence with multiple warm repeats plus the already-required repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights review.

### 2026-08-30 closure evidence

A first TDD contract demonstrated that the previous inspector could report `ready=true` for a candidate represented only by a single warm trial. RED CI #2241 failed on the new coverage contract after Ruff passed. The minimal implementation groups trials by candidate, requires `{cold, warm}` coverage, and deliberately allows additional warm repeats. Exact-head CI #2243 passed Ruff and the full pytest suite on Python 3.11 and 3.12; the durable-record head then passed CI #2244, and the merged main passed CI #2246.

A second TDD contract demonstrated that a candidate could satisfy cold/warm coverage while mixing `runtime_revision=audio.cpp@abc` and `audio.cpp@def`. RED CI #2249 passed Ruff and failed pytest on the new provenance contract. The minimal implementation groups runtime revisions by candidate and fails closed when a candidate label spans more than one revision. GREEN CI #2250 passed the full pytest suite on both Python 3.11 and 3.12 before the durable-record update.

## Re-admission / expansion gate

Do not adopt more of tts-bench merely because it is popular or actively maintained. Add another benchmark dimension only when it closes a measured Hottop evidence gap, its dependencies/licenses are independently reviewed, and it can be kept isolated from unattended model download/provisioning.
