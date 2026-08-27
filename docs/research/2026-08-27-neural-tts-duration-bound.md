# Neural-TTS planned-dialogue duration correctness — 2026-08-27

## Gap

Hottop already preserved `AudioCue.duration_seconds` through `hottop.video-plan.v1` and MoviePy had a later material-overrun guard, but the operator-local Qwen3-TTS production route initially did not receive that planned dialogue slot. A valid neural waveform could therefore be generated materially longer than its narrative window before the compositor discovered the problem.

A second, later-identified gap remained after adding the output-duration gate: Hottop rejected an overlong WAV only **after Qwen inference had finished**. Upstream Qwen3-TTS exposes a generation-token limit, and public missing-EOS reports show inference can otherwise continue far beyond the useful dialogue window. Artifact correctness was protected, but operator GPU time was not bounded by the known slot.

These are execution-integrity issues, not naturalness/style preferences: dialogue that overruns its slot can collide with the next action or line, and runaway generation can consume operator-owned compute for output that can never be admitted to the timeline.

## TDD evidence

### Output-duration gate

- RED exact `b3aef79e9739238c03291304d803de0e237dcf21`, CI #1834: Ruff passed; full pytest reached the intended new boundary and failed two contracts. Qwen3-TTS accepted a 1.25-second waveform for a 1.0-second slot, and normal `video-run` routing omitted `--max-duration-seconds` for a bounded Qwen dialogue cue.
- GREEN implementation `3a2c8a6c41b8b541188751aad63ee3e86c84c35a`, CI #1835: Python 3.11 and 3.12 both passed Ruff + full pytest. Production-smoke #189 also passed the guaranteed software3d/eSpeak baseline; cinematic-delivery-smoke #56 is recorded separately as the final 720p regression gate for this exact production-code head.

### Pre-generation resource bound

- RED exact `8c012eec4328f2a11cb71fcdfef0332acc69e065`, CI #1840: Ruff passed; Python 3.12 full pytest reached the intended new contract and finished **1 failed / 515 passed**. The sole failure was `KeyError: 'max_new_tokens'`: a bounded 2.0-second Qwen request still invoked `generate_custom_voice(...)` without any generation ceiling.
- GREEN implementation `1bd3187043739ec0b2fb467497312a86500ef601`, CI #1841: Python 3.11 and 3.12 both passed Ruff + full pytest. For a bounded request Hottop now derives a codec-token ceiling from the official 12.5-frames/s tokenizer rate and passes it to `generate_custom_voice(...)` before inference runs.

## Narrow fix

The Qwen3-TTS local request/CLI accepts an optional positive `max_duration_seconds`.

When a planned duration is present:

1. the normal Qwen `video-run` route passes `AudioCue.duration_seconds` as `--max-duration-seconds`;
2. before inference, Hottop derives `max_new_tokens = min(2048, ceil(max_duration_seconds × 12.5) + 1)`;
3. `12.5` is the published Qwen-TTS tokenizer codec-frame rate; the extra one token is reserved for EOS/control, and the cap never exceeds Qwen3-TTS's upstream default `2048` generation limit;
4. after inference, model output still must pass empty/finite/serialized-PCM non-silence checks;
5. Hottop then computes real duration from exact PCM frame count and returned sample rate, and audio longer than the planned slot fails closed **before** any WAV or temporary output file is created;
6. unbounded standalone requests and cues without a planned duration preserve their prior behavior and do not receive a new `max_new_tokens` override.

The token bound is a **resource guard**, not proof of wall-clock duration. The output-side PCM duration gate remains authoritative because codec tokens, EOS behavior and final sample duration are not interchangeable evidence.

CosyVoice3 is not currently a normal `video-run` production route, so this work does not add a speculative duration API there merely for symmetry. Its existing waveform-integrity gates remain unchanged until an actual routed benchmark requires a duration contract.

## Fresh upstream context

Fresh review on 2026-08-27 reinforces why both generation-time and output-side boundaries matter:

- `QwenLM/Qwen3-TTS#23` reports that explicit instructions such as “finish within five seconds” or “audio duration should not exceed 5 seconds” did not control generated wall-clock length across 1.7B Base, CustomVoice and VoiceDesign; only vague speaking-rate instructions had an effect.
- The official `generate_custom_voice(...)` API accepts generic generation kwargs including `max_new_tokens`; its implementation defaults that ceiling to `2048`.
- The official Qwen-TTS tokenizer documentation identifies the 12Hz tokenizer as operating at **12.5 FPS**.
- `QwenLM/Qwen3-TTS` missing-EOS reports show generation can continue for many minutes on problematic inputs and explicitly recommend a hard token limit; related serving reports also describe codec repetition / missing-EOS over-generation.

These observations do not justify a provider switch, hidden serving stack or new model download. They support Hottop's correctness-first policy: use the upstream generation ceiling to bound wasted compute when the timeline already provides a hard slot, and still verify exact timeline requirements against produced artifacts.

## Durable consequence

When a Qwen3-TTS production route receives a bounded dialogue cue, **planned slot duration is both a bounded-generation resource constraint and a fail-closed artifact constraint, not a style hint**. The adapter should constrain generation before operator compute is spent on obviously inadmissible runaway output, then independently reject materially overlong produced PCM before serialization/consumption.

Natural-language speed/duration instructions may still shape performance, but they are never proof that the returned waveform fits the timeline. A token ceiling likewise does not replace artifact validation.

This remains separate from MoviePy's later duration validation, intelligibility evaluation, delivery/naturalness benchmarking and final-media audio coverage checks. No paid service, model auto-download, GPU provisioning, RMS/VAD/loudness heuristic or provider change is introduced by this closure.