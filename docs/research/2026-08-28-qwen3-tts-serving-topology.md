# Qwen3-TTS 1.7B serving-topology benchmark note

Date: 2026-08-28
Milestone: Production v0.2

## Why this matters

Hottop's unresolved Mandarin quality ceiling is still a real operator-provisioned Qwen3-TTS 1.7B CustomVoice same-line A/B. Public serving results are useful for planning that benchmark, but they can be misread if serving topology, cache/execution shape and first-use behavior are not bound as provenance.

This note does **not** change the guaranteed eSpeak-family fallback, the reviewed local Qwen adapter, model-download policy, provider routing or Production v0.2 quality claims. It narrows how future operator-local acceleration evidence must be recorded.

## Fresh evidence

Reviewed source: `sgl-project/sglang-omni` issue #1418, opened 2026-08-08 and updated 2026-08-25:

- https://github.com/sgl-project/sglang-omni/issues/1418
- official Qwen3-TTS source `main` observed at `QwenLM/Qwen3-TTS@022e286b98fbec7e1e916cb940cdf532cd9f488e` during this review.

The issue reports Qwen3-TTS 1.7B measurements on one H100 where a single instance peaks at about **10.26 QPS**, while **two replicas on the same card under DP2 + MPS peak at 15.26 QPS**. The model is unchanged between those arms; the serving topology changes. Reported C16 English WER is approximately 1.04% versus 1.07%, so the large throughput difference is not evidence of a different model-quality regime.

The same work later reports a three-way H100 calibration of roughly **10.59 / 14.86 / 15.61 QPS** for baseline single instance / optimized single instance / DP2 pool. On H200 the relationship changes again, which reinforces that absolute throughput is hardware- and topology-bound rather than a portable model property.

The issue also records an intermittent overload failure on H200 involving a CUDA device-side assert. That is another reason Hottop must not promote throughput numbers without the matching stability/error evidence.

A second fresh correctness signal appears in `sgl-project/sglang-omni` issue #1428, opened 2026-08-09:

- https://github.com/sgl-project/sglang-omni/issues/1428

It reports same-seed output divergence on the **first use of an exact prompt even at concurrency=1**. The submitted reproduction attributes the stable `A → B` first-use pattern to radix-cache state changing `q_len`, which selects a different FlashInfer FA2 specialization; a very small numerical difference then reorders sampled codec-token candidates and autoregressively produces a different waveform. The report also notes that deterministic inference avoids the observed divergence by preventing that execution-shape change, rather than proving the kernels themselves shape-invariant.

Regardless of eventual upstream resolution, this is enough to make a single cold trial inadmissible as Hottop quality evidence. Future A/Bs must distinguish cold-first-use from warmed repeated runs and bind cache/deterministic execution-shape state instead of assuming one seeded generation represents a stable distribution.

## Hottop implication

A serving-topology improvement is not a model-quality improvement, and one cold generation is not a robust quality sample. Future Qwen3-TTS acceleration evidence must keep at least these dimensions separate:

1. **model/checkpoint identity**;
2. **serving/runtime source and local patch identity**;
3. **hardware identity**;
4. **serving topology** — single instance, process/stage isolation, same-card multi-replica, MPS, data parallelism and relevant concurrency limits;
5. **execution shape/cache state** — radix/prefix-cache mode, deterministic mode and other settings that can change kernel dispatch for the same logical request;
6. **traffic shape** — request concurrency/rate, prompt set and dataset hash;
7. **trial state** — cold-first-use versus warmed/repeated trial, seed and repetition count;
8. **throughput/latency** — QPS, TTFA and overload/failure behavior;
9. **audio quality** — same-line Mandarin intelligibility, delivery/naturalness, non-empty/finite/non-silent serialized PCM and slot-fit duration;
10. **publication rights** and no hidden paid/network/model-fetch dependency.

Do not compare a single-instance Hottop result against a multi-replica/MPS public number as though they were the same system. Do not credit dispatch/process-topology gains to Qwen model quality or to an inference kernel unless the A/B isolates that variable. Do not accept a single same-seed cold generation as reproducibility evidence. Same seed is meaningful only when the execution-shape/cache conditions are also bound or deliberately varied as part of the test.

## Benchmark rule for the future operator run

When Qwen3-TTS 1.7B is actually provisioned on an operator machine, run the **quality A/B first on one explicitly bound topology and execution-shape policy**. Only after the same-line Mandarin quality gate passes should serving acceleration be tested as a separate experiment.

For any quality or acceleration A/B:

- hold checkpoint, text, speaker, language, `instruct`, audio format and evaluation set constant;
- record exact topology and concurrency settings;
- record cache/deterministic-mode settings that may alter execution shape;
- bind runtime/container/patch provenance as required by `2026-08-26-qwen3-tts-serving-provenance.md`;
- run and label a cold-first-use trial separately from warmed repeated trials;
- use repeated warmed trials for quality/latency conclusions rather than one seeded sample;
- if cache state is intentionally varied, report the outputs as a cache-invariance experiment rather than mixing them into ordinary repeatability statistics;
- report throughput and TTFA separately from audio-quality metrics;
- include failures/OOM/device-assert outcomes, not only successful requests;
- do not promote a topology whose throughput gain is accompanied by a measurable Mandarin-quality regression or instability.

## Decision

Keep the reviewed official/local Qwen3-TTS adapter as Hottop's integration surface. Treat SGLang-Omni topology/cache work as **operator-only benchmark guidance**, not a new provider and not a production dependency.

This adds durable evidence dimensions to the existing TTS serving contract: **serving topology and execution-shape/cache state are part of the measured system**, and **cold-first-use must be separated from warmed repeated trials**. It does not weaken the existing 1.7B capability gate, final PCM integrity gates, publication-rights review, eSpeak fallback or zero-paid/no-auto-download policy.
