# Neural-TTS planned-dialogue duration correctness — 2026-08-27

## Gap

Hottop already preserved `AudioCue.duration_seconds` through `hottop.video-plan.v1` and MoviePy had a later material-overrun guard, but the operator-local Qwen3-TTS production route did not receive that planned dialogue slot. A valid neural waveform could therefore be generated materially longer than its narrative window before the compositor discovered the problem.

This is an execution-integrity issue, not a naturalness/style preference: dialogue that overruns its slot can collide with the next action or line and waste operator GPU work that can never be admitted to the timeline.

## TDD evidence

- RED exact `b3aef79e9739238c03291304d803de0e237dcf21`, CI #1834: Ruff passed; full pytest reached the intended new boundary and failed two contracts. Qwen3-TTS accepted a 1.25-second waveform for a 1.0-second slot, and normal `video-run` routing omitted `--max-duration-seconds` for a bounded Qwen dialogue cue.
- GREEN implementation `3a2c8a6c41b8b541188751aad63ee3e86c84c35a`, CI #1835: Python 3.11 and 3.12 both passed Ruff + full pytest. Production-smoke #189 also passed the guaranteed software3d/eSpeak baseline; cinematic-delivery-smoke #56 is recorded separately as the final 720p regression gate for this exact production-code head.

## Narrow fix

The Qwen3-TTS local request/CLI now accepts an optional positive `max_duration_seconds`.

When a planned duration is present:

1. the normal Qwen `video-run` route passes `AudioCue.duration_seconds` as `--max-duration-seconds`;
2. after model output has passed empty/finite/serialized-PCM non-silence checks, Hottop computes duration from the exact PCM frame count and returned sample rate;
3. audio longer than the planned slot fails closed **before** any WAV or temporary output file is created;
4. unbounded standalone requests and cues without a planned duration preserve their prior behavior.

CosyVoice3 is not currently a normal `video-run` production route, so this work does not add a speculative duration API there merely for symmetry. Its existing waveform-integrity gates remain unchanged until an actual routed benchmark requires a duration contract.

## Fresh upstream context

Fresh review on 2026-08-27 reinforces why this must be an output-side gate rather than prompt policy:

- `QwenLM/Qwen3-TTS#23` reports that explicit instructions such as “finish within five seconds” or “audio duration should not exceed 5 seconds” did not control generated wall-clock length across 1.7B Base, CustomVoice and VoiceDesign; only vague speaking-rate instructions had an effect.
- The official `generate_custom_voice(...)` API exposes speaker/language/optional instruction text plus generic generation kwargs; it does not document an exact wall-clock duration contract.
- `QwenLM/Qwen3-TTS` discussion #211 reports over-generation / missing-EOS / long-running inference cases; lowering `max_new_tokens` can mitigate some cases but is not an exact audio-duration control.

These observations do not justify a provider switch, hidden serving stack or new model download. They support Hottop's existing correctness-first policy: exact timeline requirements are verified against produced artifacts, not inferred from prompts or successful inference calls.

## Durable consequence

When a neural-TTS production route receives a bounded dialogue cue, **planned slot duration is a fail-closed artifact constraint, not a style hint**. The adapter must reject materially overlong produced PCM before serialization/consumption. Natural-language speed/duration instructions may still shape performance, but they are never proof that the returned waveform fits the timeline.

This remains separate from MoviePy's later duration validation, intelligibility evaluation, delivery/naturalness benchmarking and final-media audio coverage checks. No paid service, model auto-download, GPU provisioning, RMS/VAD/loudness heuristic or provider change is introduced by this closure.
