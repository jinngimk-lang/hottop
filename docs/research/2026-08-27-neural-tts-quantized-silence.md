# Neural-TTS quantized-silence correctness — 2026-08-27

## Gap

Hottop already rejected empty, non-finite and exact-all-zero **float-domain** neural-TTS waveforms before WAV creation. That contract still admitted a non-zero sub-LSB waveform such as `1e-12, -1e-12, 1e-12`: every sample becomes integer zero when serialized as signed 16-bit PCM, so the resulting WAV is digitally silent even though the model-returned floats were not exactly zero.

The production truth is therefore the bytes that will actually be serialized, not merely the pre-quantization floating-point tensor.

## TDD evidence

- Initial test commit `ed34c1b7a65c090e5b6c083d21bf292917e52816` was blocked by Ruff import ordering and did not yet prove the production bug.
- Isolated RED exact `78bc20073a6fa313c3ad0c72fd925f6992761d50`, CI #1828: Ruff passed; Python 3.11 full pytest reached the target contract and failed exactly twice, once for Qwen3-TTS and once for CosyVoice3 (`2 failed / 511 passed`). Both writers accepted a sub-LSB non-zero waveform that quantized to all-zero PCM.
- GREEN exact `409d3e37ed4a03cd9b3769042eaf350315b9e43c`, CI #1830: Python 3.11 and 3.12 both passed Ruff + the full pytest suite.

## Narrow fix

Both local neural-TTS writers now:

1. reject empty input;
2. reject NaN/Inf;
3. preserve the existing float-domain exact-zero rejection;
4. quantize to the exact int16 PCM representation that would be written;
5. reject the result if **all serialized PCM samples are zero**;
6. only then create the temporary WAV and atomically replace the final output.

This remains deliberately narrower than RMS, VAD, loudness normalization or silence trimming. Quiet but representable speech is still accepted. Duration, intelligibility, delivery quality and final-media checks remain independent higher-level gates.

## Fresh upstream context

Freshness review on 2026-08-27 did not surface an upstream report of this exact sub-LSB quantization bug. It did reinforce the broader correctness-first boundary:

- `QwenAudio/CosyVoice#1930`, opened 2026-08-08, reports 64/64 non-finite outputs on the official Fun-CosyVoice3-0.5B-2512 checkpoint under TensorRT+FP16 while eager/FP32 controls passed.
- `vllm-project/vllm-omni#6455`, opened 2026-08-21, reports a CosyVoice3 streaming STFT device mismatch.
- `vllm-project/vllm-omni#6158`, opened 2026-08-13, documents rare Qwen3-TTS codec repetition / missing-EOS behavior, including reproduction with the official CUDA implementation.

These are evidence that successful inference calls and audio-shaped return objects are not sufficient production proof. They do **not** justify switching providers, adding serving stacks, auto-downloading models or changing Hottop's zero-cost/operator-local routing.

## Durable consequence

For Hottop neural-TTS adapters, `non-silent` means the narrow exact-all-zero check on the **PCM samples that are actually going to be serialized**. Float-domain non-zero alone is insufficient. Broader perceptual silence/intelligibility policies require separate measured evidence before admission.
