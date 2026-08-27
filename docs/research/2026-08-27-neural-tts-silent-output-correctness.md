# Neural-TTS silent-output correctness radar — 2026-08-27

## Why this matters

Hottop already rejects empty and non-finite neural-TTS waveforms before PCM/WAV creation. That boundary is still incomplete if a backend returns a non-empty waveform containing only digital silence: the file is structurally valid but contains no usable dialogue.

This note records upstream evidence and the narrow Hottop contract being tested. It does **not** enable a provider, download a model, provision GPU capacity, add credentials, or change normal `video-run` routing.

## Fresh upstream evidence

### CosyVoice can return zero-second audio for some inputs

`QwenAudio/CosyVoice#1800`, opened 2026-01-22, reports a vLLM-backed CosyVoice3 service where some text inputs generate normally while others produce **0s audio**; the same report also mentions unnecessary trailing silence on some outputs. The issue was later closed by the stale bot rather than by a documented root-cause fix.

This is not proof that every CosyVoice runtime has the defect, and Hottop has not independently reproduced that exact serving stack. It is sufficient evidence that “the model returned an audio-shaped object” is not a safe success criterion.

### Existing non-finite evidence remains relevant

`QwenAudio/CosyVoice#1930`, opened 2026-08-08, reports 64/64 non-finite generations on the official Fun-CosyVoice3-0.5B-2512 checkpoint under TensorRT+FP16, while eager and FP32 TensorRT controls passed. Hottop already hardened both current neural-TTS writers against NaN/Inf based on this class of failure.

## Hottop gap found in this cycle

Both current local writers reject:

- an empty sample sequence;
- invalid/non-positive sample rate where applicable;
- NaN/Inf samples.

But both still accept a non-empty **all-zero** waveform and write it as a successful WAV. That creates a silent-corruption path: a structurally valid file can be mistaken for usable dialogue before later media assembly.

## Narrow production contract

For current neural-TTS adapters, an all-zero waveform is invalid production output and must fail **before** WAV creation. This is intentionally narrower than a general loudness or VAD threshold:

- do not reject quiet but real speech;
- do not add provider-specific heuristic loudness thresholds;
- do not trim or rewrite audio in the adapter;
- keep later duration/intelligibility/media checks separate.

The RED contract is shared by Qwen3-TTS and CosyVoice3 so their basic waveform-integrity semantics remain aligned.

## Admission consequence

A neural TTS route is not successful merely because inference returns finite samples. At minimum the waveform must contain non-zero signal before it can be serialized as production dialogue. Higher-level intelligibility, delivery, duration and publication-rights evidence remain separate gates.
