# Qwen3-TTS HIP admission — 2026-08-29

## Why this candidate matters

Hottop's current neural-TTS quality target is operator-owned Qwen3-TTS 1.7B CustomVoice with exact-runtime/output evidence. `piedshag/qwen3-tts-hip` is a local Rust + ROCm/HIP implementation that could lower the serving/runtime overhead for AMD operator hardware while preserving a zero-paid path.

This record is an **admission review**, not a production-quality claim and not an executable integration.

## Reviewed upstream

- repository: `piedshag/qwen3-tts-hip`
- exact source revision: `5b60101c62e3a689e0d73aecde32ee40d7af33f9`
- source license at that revision: MIT
- runtime family: Rust 2024 + ROCm/HIP + rocBLAS/HIPRTC on Linux x86_64
- expected model layout: operator-provisioned local Qwen3-TTS snapshot

The upstream README reports:

- CustomVoice 0.6B support;
- **basic CustomVoice 1.7B support**;
- 0.6B deterministic text/code parity against exported Python fixtures;
- native HIP codec-stage waveform parity against Python fixtures;
- local R9700 measurements around `0.54` RTF for hot 0.6B streaming and around `0.41` RTF for deterministic greedy 0.6B;
- an optimized deterministic greedy 1.7B 39-frame benchmark around `0.50` RTF;
- **1.7B EOS/stopping parity still needs more work**.

Those numbers are upstream-local measurements. They are not Hottop benchmarks.

## Admission verdict

**Research / benchmark candidate only. Do not add an unattended production route yet.**

Reasons:

1. 1.7B stopping/EOS parity is explicitly incomplete upstream; Hottop already treats missing-EOS / repetition / over-generation as a hard production-integrity risk.
2. The reviewed project targets AMD ROCm/HIP hardware; Hottop has no operator runtime evidence for this stack in the current environment.
3. Source-code MIT licensing does not settle Qwen checkpoint/tokenizer rights, reference/voice-clone rights, or final output publication rights.
4. Upstream parity and RTF results are useful implementation evidence, but do not establish Mandarin intelligibility, speaker consistency, onset stability, delivery control, artifact duration, or publication quality.
5. Full reference-audio encoding / ICL ref-code prompting is not ported to the Rust runtime; Base voice cloning currently uses precomputed x-vector prompt artifacts, which remain rights-gated.

## Zero-cost / safety boundary

Normal Hottop must not:

- auto-install Rust/ROCm or this repository;
- download Qwen model snapshots;
- provision AMD GPU drivers/runtime;
- execute upstream benchmark/parity scripts unattended;
- interpret upstream `0.50 RTF` or parity claims as Hottop quality evidence;
- enable reference/cloning paths without rights-cleared source audio and an explicit capability/rights review.

If the candidate is evaluated later, all source/model/tokenizer/prompt/output bytes must remain operator-provisioned and separately bound.

## Re-admission gate

Reconsider a narrow Hottop adapter only after all of the following are true:

1. an operator provides a local AMD ROCm/HIP runtime and the exact reviewed source/build identity;
2. exact Qwen3-TTS 1.7B CustomVoice model/tokenizer bytes are locally provisioned and rights-cleared for the intended use;
3. upstream 1.7B EOS/stopping parity is either closed or independently bounded by Hottop;
4. the same Mandarin lines used by the existing Qwen benchmark protocol are generated with bound speaker, seed/sampling, generation ceiling and cold/warm trial identity;
5. every WAV passes non-empty, finite, serialized-PCM non-silence, duration, exact-byte provenance and publication-rights gates;
6. repeated trials measure speaker consistency, short-onset stability, intelligibility, naturalness, latency/RTF and failure behavior;
7. the result beats or materially complements the existing eSpeak guarantee / operator-local Qwen routes under a documented rollback path.

Until then, `qwen3-tts-hip` is a useful AMD-local radar signal, not a production backend.