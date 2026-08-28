# Qwen3-TTS runtime repeatability — 2026-08-29

## Why this matters

Production v0.2 treats neural-TTS quality as output evidence, not as a property inherited from a model name. A fresh third-party runtime report initially looked like repeated speaker drift: the same Qwen3-TTS 1.7B Base model invoked repeatedly with `--voice Chelsie` emitted different-sounding voices across runs in MLX-Audio.

The merged upstream fix makes the root cause more precise and more useful for Hottop: **Qwen3-TTS Base checkpoints do not expose the preset-speaker table used by CustomVoice**. MLX-Audio accepted an unsupported `--voice`, silently dropped the conditioning, and generated unconditioned speech. The correct behavior is fail-closed capability validation, not pretending that an unsupported speaker request was honored.

## Evidence boundary

- Public report: `Blaizzy/mlx-audio` issue #892, opened 2026-08-17 and closed by merged PR #895 on 2026-08-20.
- Reported surface: `Qwen3-TTS-12Hz-1.7B-Base-bf16` through MLX-Audio CLI with `--voice Chelsie`.
- Reporter expectation: repeated generation uses the selected voice.
- Observed behavior: repeated generations sounded like different random voices.
- Upstream root cause from #895: Base checkpoints ship an empty preset-speaker table; `--voice` was silently ignored and generation proceeded with no speaker embedding. Base voice conditioning is instead via rights-gated `ref_audio` + `ref_text` cloning, while preset speakers belong to CustomVoice checkpoints.
- Upstream fix: reject unsupported `voice` on Base models and correct examples to use real CustomVoice preset speakers instead of silently degrading to unconditioned speech.
- Do **not** generalize #892 to Hottop's official Qwen CustomVoice adapter, qwentts.cpp, Qwen3-TTS-ncnn, or the Qwen model family without reproduction on the exact runtime/checkpoint path.

Sources:

- https://github.com/Blaizzy/mlx-audio/issues/892
- https://github.com/Blaizzy/mlx-audio/pull/895

## Hottop consequence

Future operator-local Mandarin A/B must enforce two independent gates:

1. **capability binding before execution** — a requested preset speaker/voice, instruction mode or cloning mode must be supported by the exact checkpoint/runtime path; unsupported conditioning fails closed rather than being silently dropped;
2. **repeat speaker consistency after execution** — even when the capability is valid, repeated trials must verify output-side speaker stability rather than relying on one successful WAV.

Bind at minimum:

1. exact runtime/source revision and backend/build identity;
2. exact model/tokenizer/GGUF/checkpoint bytes where locally inspectable;
3. exact checkpoint capability mode (`Base`, `CustomVoice`, cloning/reference mode, etc.);
4. exact Mandarin text, language, preset speaker/voice selection or rights-cleared reference conditioning, seed and sampling controls;
5. generation ceiling and cold/warm trial identity;
6. every produced WAV's SHA-256, duration and serialized-PCM integrity result;
7. repeated-trial speaker consistency plus short-onset stability, intelligibility and naturalness.

A single successful WAV does not prove stable speaker identity. More importantly, a runtime must never report success for a conditioning request it did not actually apply. Runtime-specific regressions also must not be promoted into model-family claims without reproduction.

## Admission impact

No route changes in this review. `qwen3-tts-qwentts-cpp-1b7` and `qwen3-tts-ncnn-0b6` remain `benchmark_candidate / integration_ready=false / runtime_status=unprobed`. eSpeak remains the guaranteed local fallback. No model download, runtime installation, credential, GPU provisioning or paid action is authorized by this record.
