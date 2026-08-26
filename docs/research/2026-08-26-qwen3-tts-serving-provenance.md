# Qwen3-TTS serving benchmark provenance review

Date: 2026-08-26
Milestone: Production v0.2

## Why this matters

Hottop's current Mandarin quality ceiling is still the operator-provisioned Qwen3-TTS 1.7B CustomVoice benchmark. Recent public serving results are useful for runtime planning, but several headline numbers are **not results from an unmodified upstream checkout**. A serving benchmark is therefore not reproducible enough for Hottop if it records only the model name and upstream repository revision.

This review does **not** change the guaranteed eSpeak-family fallback, the reviewed local Qwen adapter, or the no-auto-download boundary. It tightens the evidence expected from any future operator-local acceleration benchmark.

All three reviewed reports use `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` at model revision `0c0e3051f131929182e2c023b9537f8b1c68adfe`, BF16, Ryan, English, PCM16 mono 24 kHz. Those settings make the throughput evidence useful for runtime architecture, but they are **not a Mandarin naturalness benchmark** and do not satisfy Hottop's same-line Mandarin A/B gate.

## Fresh public evidence

### M* / Nari benchmark

The published M* Qwen3-TTS 1.7B CustomVoice report states that its benchmark applied custom source patches that expose `codec_chunk_frames` as an init-time YAML override and add an initial code-chunk ramp. Those changes are explicitly described as absent from the referenced upstream base `ea5e5a4b9c11d0493a1ba3986e07c1bafa1460a5`. Reported median p95 TTFA rises from about 104 ms at 1 RPS to about 948 ms at 12 RPS, with the tested series stopping there because higher-load profiles could not satisfy continuity and sustainability together.

The reported environment is a single H100 SXM 80 GB on Google Cloud with NVIDIA driver `580.173.02`, CUDA compatibility 13.0, CUDA toolkit 12.9 and Python 3.12.3. The client and serving runtime ran on the same VM over localhost, so the latency excludes a production network path. The report also binds the Seed-TTS prompt projection SHA-256 `c95cb482f71117cbc46ac4e3aa5eab5c199bb0386d9e5600d912e157da8d2866`.

Admission implication: these numbers describe the **pinned patched runtime**, not generic M* or generic Qwen3-TTS. A Hottop result would need to bind the local patch/diff identity in addition to the public base revision.

### vLLM-Omni benchmark

The published vLLM-Omni report states that it used a dynamic PCM-onset trim override, so its results also describe a patched runtime rather than an unmodified build. The report binds public runtime revision `a4ea67a21b20054dacc6e83952f9bd407e8ee4e7`, runtime image ID `sha256:5cba1538c6f8ee81e8bea6708c24e68d7b2640f466a9fbf2ef15e68f2168b48b`, the same Seed-TTS projection hash, traffic shape and localhost network path. Median p95 TTFA ranges from about 56.8 ms at 1 RPS to about 396.9 ms at 20 RPS.

Admission implication: the container/runtime patch identity is part of the measured system and must be preserved alongside the public source revision. A container digest does not by itself prove Mandarin quality or `instruct` delivery control.

### SGLang-Omni benchmark

The published SGLang-Omni report says Qwen3-TTS support remains under active development and uses a pinned CustomVoice compatibility baseline plus dynamic speech-onset trim. It binds SGLang-Omni revision `2cac60e8ac38cf5d3c7091ec3dd15782bc8b1f41`, SGLang revision `fdebc938f7f4d16fe6b9f55dcd9a767cf0899ea1` and benchmark revision `328bd5b0132f06ae76dc36d122da7ab84ed64198`. Median p95 audible TTFA grows from about 120.9 ms at 1 RPS to about 2.38 s at 12 RPS. The report explicitly frames candidate differences as configuration-only **after** fixing that compatibility baseline, and notes that upstream CustomVoice/VoiceDesign streaming support is still incomplete at the tested boundary.

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
