# Qwen3-TTS serving benchmark provenance review

Date: 2026-08-26
Milestone: Production v0.2

## Why this matters

Hottop's current Mandarin quality ceiling is still the operator-provisioned Qwen3-TTS 1.7B CustomVoice benchmark. Recent public serving results are useful for runtime planning, but several headline numbers are **not results from an unmodified upstream checkout**. A serving benchmark is therefore not reproducible enough for Hottop if it records only the model name and upstream repository revision.

This review does **not** change the guaranteed eSpeak-family fallback, the reviewed local Qwen adapter, or the no-auto-download boundary. It tightens the evidence expected from any future operator-local acceleration benchmark.

## Fresh public evidence

### M* / Nari benchmark

The published M* Qwen3-TTS 1.7B CustomVoice report states that its benchmark applied custom source patches that expose `codec_chunk_frames` as an init-time YAML override and add an initial code-chunk ramp. Those changes are explicitly described as absent from the referenced upstream revision. Reported median p95 TTFA rises from about 104 ms at 1 RPS to about 948 ms at 12 RPS, with the tested series stopping there because higher-load profiles could not satisfy continuity and sustainability together.

Admission implication: these numbers describe the **pinned patched runtime**, not generic M* or generic Qwen3-TTS.

### vLLM-Omni benchmark

The published vLLM-Omni report states that it used a dynamic PCM-onset trim override, so its results also describe a patched runtime rather than an unmodified build. The report binds the model revision, public runtime revision, container image SHA-256, dataset projection hash, traffic shape and localhost network path. Its median p95 TTFA ranges from about 56.8 ms at 1 RPS to about 396.9 ms at 20 RPS.

Admission implication: the container/runtime patch identity is part of the measured system and must be preserved alongside the public source revision.

### SGLang-Omni benchmark

The published SGLang-Omni report says Qwen3-TTS support remains under active development and uses a pinned CustomVoice compatibility baseline plus dynamic speech-onset trim. Median p95 audible TTFA grows from about 120.9 ms at 1 RPS to about 2.38 s at 12 RPS. The report explicitly frames candidate differences as configuration-only **after** fixing that compatibility baseline.

Admission implication: a future Hottop benchmark must distinguish upstream source, compatibility override/patch, launch configuration and model/checkpoint identity rather than flattening them into one provider label.

## Hottop evidence contract for future operator TTS acceleration

Any serving/runtime benchmark considered for Production v0.2 should record, when applicable:

1. exact Qwen3-TTS model/checkpoint identity and local model metadata;
2. exact serving/runtime source revision;
3. exact local source patches or compatibility overrides, preferably by commit/diff hash;
4. container image digest or environment lock when containers are used;
5. CUDA/PyTorch/runtime identity on the actual operator machine;
6. request shape, language, preset speaker, `instruct` semantics and audio format;
7. dataset/prompt-set hash and traffic/load methodology;
8. output-audio evidence, not latency alone: complete audio, duration, non-silence and same-line Mandarin quality comparison against the current baseline;
9. no hidden network model fetch, paid API, credential dependency or unbounded cache/bootstrap step in normal Hottop execution.

A fast benchmark with an unrecorded local patch is not admissible evidence. Likewise, a benchmark can prove throughput/latency without proving Mandarin naturalness or delivery control.

## Decision

Keep the reviewed official/local Qwen3-TTS adapter as Hottop's integration surface. Treat M*, vLLM-Omni, SGLang-Omni and Nari-style high-throughput serving stacks as **operator-only acceleration candidates** whose value must be demonstrated on the operator's provisioned hardware with exact patched-runtime provenance and a same-line Mandarin A/B.

This supersedes any loose interpretation that an upstream Git SHA alone is sufficient provenance for an accelerated TTS result. It does not supersede the existing 1.7B CustomVoice capability gate, speaker/output-rights review, eSpeak fallback, or zero-paid/no-auto-download policy.
