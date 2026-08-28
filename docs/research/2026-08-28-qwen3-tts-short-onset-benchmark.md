# Qwen3-TTS short-onset benchmark risk

Date: 2026-08-28
Milestone: Production v0.2
Status: benchmark requirement, not a production defect claim

## Why this matters

Hottop's remaining neural-TTS quality gate is a real operator-local Qwen3-TTS 1.7B Mandarin A/B against the guaranteed eSpeak-family fallback. Existing Hottop controls already fail closed on invalid dialogue text, runaway generation budget, produced PCM duration, non-finite samples and serialized digital silence. Those controls protect execution and artifact integrity, but they do not prove the first second of a short utterance has stable speaker identity or natural delivery.

A fresh upstream issue in `QwenLM/Qwen3-TTS` reports a fine-tuned 1.7B Base voice whose short utterances and opening roughly 1–2 seconds can show wrong timbre or apparent gender flips while longer generations are stable. The report is specific to a LoRA-fine-tuned Base model, so Hottop must **not** generalize it into a claim that preset 1.7B CustomVoice has the same defect.

The useful conclusion is narrower: a future Hottop 1.7B Mandarin benchmark that evaluates only longer lines or whole-clip averages can miss onset instability. Short-line quality must be measured separately.

## Benchmark implication

When an operator-provisioned 1.7B CustomVoice runtime is genuinely available, the same-line A/B protocol should include both:

1. **short dialogue / onset trials** — compact production-like Chinese lines, with the first 1–2 seconds reviewed separately for speaker/timbre stability, intelligibility and delivery;
2. **normal production-length lines** — enough duration to judge overall naturalness, cadence and instruction adherence.

Keep existing evidence dimensions unchanged:

- exact model/checkpoint and runtime/patch/container identity;
- hardware, serving topology, execution/cache policy and cold-vs-warmed state;
- repeated trials and seeds where supported;
- latency/throughput/failure rate as operational metrics only;
- Mandarin intelligibility, speaker consistency, delivery/instruction adherence and naturalness as quality metrics;
- produced-duration and serialized-PCM integrity gates;
- publication/preset-speaker rights review.

A short-onset failure is a speech-quality failure even if total duration, PCM integrity and throughput are acceptable. Conversely, this upstream issue is not evidence to reject Qwen3-TTS CustomVoice before Hottop runs its own bound benchmark.

## Admission decision

No new dependency, serving stack, model download or provider route is admitted by this research note. The official/local Qwen adapter remains the reviewed integration surface; eSpeak-family Mandarin remains the guaranteed zero-cost fallback. The 1.7B route stays operator-provisioned and fail-closed until real local benchmark evidence exists.

## Source

- `QwenLM/Qwen3-TTS` issue #343, opened 2026-07-10: fine-tuned 1.7B short/opening utterance instability. Review observed 2026-08-28.
