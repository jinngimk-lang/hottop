# Qwen3-TTS runtime repeatability — 2026-08-29

## Why this matters

Production v0.2 treats neural-TTS quality as output evidence, not as a property inherited from a model name. A fresh third-party runtime report reinforces that boundary: the same Qwen3-TTS 1.7B Base model invoked repeatedly with a named `--voice` was reported to emit different voices across runs in MLX-Audio. This is runtime-specific evidence, not proof of an official Qwen3-TTS CustomVoice defect.

## Evidence boundary

- Public report: `Blaizzy/mlx-audio` issue #892, opened 2026-08-17 and closed by #895.
- Reported surface: `Qwen3-TTS-12Hz-1.7B-Base-bf16` through MLX-Audio CLI with `--voice Chelsie`.
- Expected by reporter: repeated generation uses the same selected voice.
- Observed by reporter: repeated generations used different voices.
- Do **not** generalize this to Hottop's official Qwen adapter, qwentts.cpp, Qwen3-TTS-ncnn, or preset CustomVoice without reproducing it on the exact runtime/model path.

Source: https://github.com/Blaizzy/mlx-audio/issues/892

## Hottop consequence

Future operator-local Mandarin A/B must treat **repeat speaker consistency** as a first-class output gate, not a one-shot listening note. Bind at minimum:

1. exact runtime/source revision and backend/build identity;
2. exact model/tokenizer/GGUF/checkpoint bytes where locally inspectable;
3. exact Mandarin text, language, preset speaker/voice selection, seed and sampling controls;
4. generation ceiling and cold/warm trial identity;
5. every produced WAV's SHA-256, duration and serialized-PCM integrity result;
6. repeated-trial speaker consistency plus short-onset stability, intelligibility and naturalness.

A single successful WAV does not prove stable speaker identity. Runtime-specific regressions also must not be promoted into model-family claims without reproduction.

## Admission impact

No route changes in this review. `qwen3-tts-qwentts-cpp-1b7` and `qwen3-tts-ncnn-0b6` remain `benchmark_candidate / integration_ready=false / runtime_status=unprobed`. eSpeak remains the guaranteed local fallback. No model download, runtime installation, credential, GPU provisioning or paid action is authorized by this record.
