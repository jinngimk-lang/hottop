# Qwen3-TTS CustomVoice routing review

Date: 2026-08-26
Milestone: Production v0.2
Workstream: PR #57

## Measured gap

The canonical cow render now preserves `speaker` + `delivery` through `hottop.video-plan.v1`, and Hottop already contains an operator-local/offline `audio_qwen3_tts` adapter. Normal `video-run` audio routing still only emits eSpeak dialogue commands, so the richer role metadata cannot yet reach the reviewed Qwen3 CustomVoice path.

## Upstream freshness check

Targeted review on 2026-08-26 confirms the official Qwen3-TTS CustomVoice API still exposes `generate_custom_voice(text, speaker, language, instruct, ...)`. Official examples continue to use named speakers and pass an instruction string for delivery/prosody control. The published `qwen-tts` Python package declares Apache-2.0 code licensing and Python 3.11/3.12 support.

The adapter remains operator-owned and local-only. Hottop must not infer that the code license grants rights to arbitrary model/data assets, and must not download model weights during normal `video-run` or CI.

## Admission decision

Keep Qwen3 CustomVoice as an explicit non-default voice backend behind local preflight:

- eSpeak remains the guaranteed zero-cost/offline fallback;
- require an operator-provisioned local model directory;
- require the local `qwen_tts` + PyTorch runtime;
- preserve offline Hugging Face mode and `local_files_only=True` in the existing adapter;
- map stable Hottop character roles to explicit Qwen preset speakers through config rather than guessing from text;
- map `AudioCue.delivery` to Qwen `--instruct` without changing the dialogue text;
- fail closed when a role has no configured mapping unless an explicit default speaker is configured;
- no voice cloning/reference-audio path is introduced by this workstream.

## TDD contract

PR #57 RED head `94023c05abe0557aef21bda804c3cfa3a43c7d59` adds the focused config→runtime-command contract. CI run 1550 passes Ruff and fails pytest, proving the normal production config/runtime surface does not yet accept or route `qwen3-customvoice`.

The GREEN implementation should remain narrow: add a typed Qwen3 CustomVoice audio config, extend the voice-backend literal, make voice readiness call the existing local environment inspector, and make `_runtime_audio_commands()` emit `python -m hottop.audio_qwen3_tts` commands with configured speaker plus cue delivery. No provider abstraction, network transport, credential, auto-install or model download is justified.
