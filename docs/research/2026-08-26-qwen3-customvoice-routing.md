# Qwen3-TTS CustomVoice routing review

Date: 2026-08-26
Milestone: Production v0.2
Workstream: PR #57

## Measured gap

The canonical cow render preserves `speaker` + `delivery` through `hottop.video-plan.v1`, and Hottop already contains an operator-local/offline `audio_qwen3_tts` adapter. Before this workstream, normal `video-run` audio routing emitted only eSpeak dialogue commands, so the richer role metadata could not reach the reviewed Qwen3 CustomVoice path.

## Upstream freshness check

Targeted review on 2026-08-26 confirms the official Qwen3-TTS CustomVoice API exposes `generate_custom_voice(text, speaker, language, instruct, ...)`, and official examples use named speakers plus an instruction string for delivery/prosody control.

A second source-level check found an important capability split that supersedes the earlier broad assumption that every CustomVoice checkpoint honors `instruct`: current official inference code explicitly discards `instruct` for the 0.6B model. Official model configs identify `Qwen3-TTS-12Hz-0.6B-CustomVoice` as `tts_model_size=0b6` and `Qwen3-TTS-12Hz-1.7B-CustomVoice` as `tts_model_size=1b7`. The Production role-aware route therefore must not silently claim delivery control when pointed at 0.6B.

The published Qwen repository/model pages declare Apache-2.0, but Hottop continues to distinguish code/model metadata from rights in generated/preset-voice usage. A current upstream issue is still asking for explicit commercial-use clarification for preset-speaker output, so operator review remains required before external commercial publication. Hottop does not infer that an Apache-2.0 model card alone clears every speaker/timbre right.

## Admission decision

Keep Qwen3 CustomVoice as an explicit non-default voice backend behind local preflight:

- eSpeak remains the guaranteed zero-cost/offline fallback;
- require an operator-provisioned local model directory and local `qwen_tts` + PyTorch runtime;
- preserve offline Hugging Face mode and `local_files_only=True` in the existing adapter;
- map stable Hottop character roles to explicit Qwen preset speakers through config rather than guessing from text;
- map `AudioCue.delivery` to Qwen `--instruct` without changing dialogue text;
- for the normal Hottop role-aware video route, require an instruct-capable CustomVoice checkpoint; current 0.6B must fail closed because upstream ignores instruct, while current 1.7B is admitted by the local config capability check;
- retain standalone 0.6B basic synthesis only when no instruction is requested; do not present that path as delivery-controlled speech;
- fail closed when local model/runtime files are absent; no auto-install/model download is introduced;
- no voice cloning/reference-audio path is introduced by this workstream.

## Guaranteed fallback boundary

The guaranteed eSpeak-NG/eSpeak route now operationalizes the same preserved dialogue semantics without pretending to match neural TTS quality. A recurring Hottop `character` maps to a stable bounded deterministic eSpeak pitch, and `delivery` maps to a bounded cadence adjustment around the configured base rate. Production-smoke applies this resolver to the canonical cow/Odyssey dialogue before full rendering, so a cadence choice that breaks the real dialogue budget is caught in production evidence rather than remaining a unit-test-only assumption.

This deterministic route remains a synthetic fallback: the compact pitch space may collide for arbitrary role labels, it does not claim natural acting, and it does not supersede Qwen3-TTS/CosyVoice quality benchmarking. The Qwen checkpoint-capability and preset-speaker/output-rights gates above are unchanged.

## TDD / implementation evidence

PR #57 RED head `94023c05abe0557aef21bda804c3cfa3a43c7d59` added the focused config→runtime-command contract. CI run 1550 passed Ruff and failed pytest, proving the normal production config/runtime surface did not yet accept or route `qwen3-customvoice`.

GREEN head `7ffde866e16fdda3a877f54a5a162f102e90ba7c` added the typed Qwen3 CustomVoice audio config, local readiness routing, role→preset-speaker mapping, `delivery→--instruct`, and Qwen `--output` fresh-output handling. CI run 1552 passed.

Fresh upstream review then invalidated one assumption in that first GREEN: 0.6B silently ignores instruct. RED head `5981adba9a089b01b306df1911112f7ff4d26305` added a capability contract requiring the Production route to reject 0.6B and accept an otherwise complete 1.7B CustomVoice model. CI run 1553 failed pytest with Ruff green as expected. The follow-up implementation makes environment inspection read only the already-provisioned local `config.json`; it requires instruct capability for the Production readiness path and also rejects an instruction-bearing standalone request on 0.6B. No network lookup or model-name guessing is used.

PR #67 then closed the guaranteed-fallback half of the same semantic gap. RED CI 1607 proved the eSpeak-family runtime still discarded role/delivery controls. Exact final head `0d8211305f0f29a0675fd8d1e5e8f1d26590c570` passed CI 1610 and production-smoke 153. Artifact inspection showed stable role pitch for the canonical cow case (`young-cow=44`, `mother-cow=46`) while different young-cow deliveries produced different rates (169/162 wpm); Odyssey roles were likewise separated. The PR merged as `2d11b02a35e2dbe460917bb4b15d4b6ec4e941a6`.
