# Qwen3-TTS CustomVoice routing review

Date: 2026-08-26
Milestone: Production v0.2
Workstream: PR #57, capability-preflight follow-up PR #72

## Measured gap

The canonical cow render preserves `speaker` + `delivery` through `hottop.video-plan.v1`, and Hottop already contains an operator-local/offline `audio_qwen3_tts` adapter. Before this workstream, normal `video-run` audio routing emitted only eSpeak dialogue commands, so the richer role metadata could not reach the reviewed Qwen3 CustomVoice path.

A later preflight review found a second, narrower integrity gap: Hottop correctly rejected the known 0.6B checkpoint when delivery instruction was required, but a malformed/unknown local `config.json` could omit or invent `tts_model_size` and still pass readiness. A non-CustomVoice or even non-Qwen3-TTS model config could also pass the same preflight. Because Production role-aware routing is capability-gated, unknown capability metadata must fail closed rather than being treated as equivalent to a proven 1.7B CustomVoice checkpoint.

## Upstream freshness check

Targeted review on 2026-08-26 confirms the official Qwen3-TTS CustomVoice API exposes `generate_custom_voice(text, speaker, language, instruct, ...)`, and official examples use named speakers plus an instruction string for delivery/prosody control.

A second source-level check found an important capability split that supersedes the earlier broad assumption that every CustomVoice checkpoint honors `instruct`: current official inference code explicitly discards `instruct` for the 0.6B model. Official model configs identify `Qwen3-TTS-12Hz-0.6B-CustomVoice` as `tts_model_size=0b6` and `Qwen3-TTS-12Hz-1.7B-CustomVoice` as `tts_model_size=1b7`. The Production role-aware route therefore must not silently claim delivery control when pointed at 0.6B.

The current official 1.7B CustomVoice model tree reviewed on 2026-08-26 is about 4.52 GB in total, including a roughly 3.83 GB main `model.safetensors` plus a roughly 682 MB speech-tokenizer model. That reinforces the existing operator-provisioning boundary: normal Hottop and CI do not download this checkpoint automatically.

The published Qwen repository/model pages declare Apache-2.0, but Hottop continues to distinguish code/model metadata from rights in generated/preset-voice usage. A current upstream issue is still asking for explicit commercial-use clarification for preset-speaker output, so operator review remains required before external commercial publication. Hottop does not infer that an Apache-2.0 model card alone clears every speaker/timbre right.

### Acceleration/runtime radar refresh

A targeted runtime refresh on 2026-08-26 found two materially different acceleration directions, neither of which currently clears Hottop's admission gate as a new default:

- `nari-labs/nari-qwen3-tts` advertises a high-throughput Qwen3-TTS 1.7B CustomVoice serving path with sub-50 ms time-to-first-audio at 10 requests/s, but its headline path is explicitly a **single-H100** serving implementation. That can be valuable for an already-provisioned operator benchmark, but it does not reduce Hottop's current zero-cost/local provisioning boundary and is not evidence of better Mandarin quality. Do not add it to normal `video-run` without a measured latency/throughput bottleneck and exact source/runtime review.
- SGLang-Omni's current Qwen3-TTS optimization tracker reports H100/H200 execution-path work, including removal of a Talker `torch.compile` path after crossed measurements showed no reproducible end-to-end benefit. This is useful evidence for Hottop's broader rule: acceleration claims require end-to-end measurement, not a nominal optimization switch. It remains operator-GPU infrastructure, not a guaranteed fallback.
- Community GUI/ComfyUI wrappers commonly offer first-use or on-demand model download behavior. That conflicts with Hottop's unattended boundary even when the underlying model is acceptable. Hottop should continue using its narrow local adapter and explicit local-model preflight rather than adopting wrappers that silently fetch multi-GB weights.

Decision: keep the reviewed official/local Qwen adapter as the integration surface. Treat H100/H200 serving stacks as future operator-only benchmark candidates, not as a reason to add dependencies or change the guaranteed eSpeak-family fallback.

## Admission decision

Keep Qwen3 CustomVoice as an explicit non-default voice backend behind local preflight:

- eSpeak remains the guaranteed zero-cost/offline fallback;
- require an operator-provisioned local model directory and local `qwen_tts` + PyTorch runtime;
- preserve offline Hugging Face mode and `local_files_only=True` in the existing adapter;
- map stable Hottop character roles to explicit Qwen preset speakers through config rather than guessing from text;
- map `AudioCue.delivery` to Qwen `--instruct` without changing dialogue text;
- require local `config.json` to prove `model_type=qwen3_tts`, `tts_model_type=custom_voice` and a supported `tts_model_size` before readiness can pass;
- for the normal Hottop role-aware video route, require an instruct-capable CustomVoice checkpoint; current 0.6B must fail closed because upstream ignores instruct, while current 1.7B is admitted by the local config capability check;
- missing or unknown model-size/capability metadata fails closed rather than being treated as a future-compatible success;
- retain standalone 0.6B basic synthesis only when no instruction is requested; do not present that path as delivery-controlled speech;
- fail closed when local model/runtime files are absent; no auto-install/model download is introduced;
- no voice cloning/reference-audio path is introduced by this workstream.

## Guaranteed fallback boundary

The guaranteed eSpeak-NG/eSpeak route now operationalizes the same preserved dialogue semantics without pretending to match neural TTS quality. A recurring Hottop `character` maps to a stable bounded deterministic eSpeak pitch, and `delivery` maps to a bounded cadence adjustment around the configured base rate. Production-smoke applies this resolver to the canonical cow/Odyssey dialogue before full rendering, so a cadence choice that breaks the real dialogue budget is caught in production evidence rather than remaining a unit-test-only assumption.

This deterministic route remains a synthetic fallback: the compact pitch space may collide for arbitrary role labels, it does not claim natural acting, and it does not supersede Qwen3-TTS/CosyVoice quality benchmarking. The Qwen checkpoint-capability and preset-speaker/output-rights gates above are unchanged.

## TDD / implementation evidence

PR #57 RED head `94023c05abe0557aef21b306df1911112f7ff4d26305` added the focused config→runtime-command contract. CI run 1550 passed Ruff and failed pytest, proving the normal production config/runtime surface did not yet accept or route `qwen3-customvoice`.

GREEN head `7ffde866e16fdda3a877f54a5a162f102e90ba7c` added the typed Qwen3 CustomVoice audio config, local readiness routing, role→preset-speaker mapping, `delivery→--instruct`, and Qwen `--output` fresh-output handling. CI run 1552 passed.

Fresh upstream review then invalidated one assumption in that first GREEN: 0.6B silently ignores instruct. RED head `5981adba9a089b01b306df1911112f7ff4d26305` added a capability contract requiring the Production route to reject 0.6B and accept an otherwise complete 1.7B CustomVoice model. CI run 1553 failed pytest with Ruff green as expected. The follow-up implementation makes environment inspection read only the already-provisioned local `config.json`; it requires instruct capability for the Production readiness path and also rejects an instruction-bearing standalone request on 0.6B. No network lookup or model-name guessing is used.

PR #67 then closed the guaranteed-fallback half of the same semantic gap. RED CI 1607 proved the eSpeak-family runtime still discarded role/delivery controls. Exact final head `0d8211305f0f29a0675fd8d1e5e8f1d26590c570` passed CI 1610 and production-smoke 153. Artifact inspection showed stable role pitch for the canonical cow case (`young-cow=44`, `mother-cow=46`) while different young-cow deliveries produced different rates (169/162 wpm); Odyssey roles were likewise separated. The PR merged as `2d11b02a35e2dbe460917bb4b15d4b6ec4e941a6`.

PR #72 closed the remaining local capability fail-open. RED head `9b1afd141de14eb19ab1d849d68ef2f2585389cf` passed Ruff and failed pytest in CI 1623 because missing/unknown model-size metadata and wrong model/model-type configs were not rejected. GREEN implementation head `0d969d3cf76b20950f29b7a0d4ca2f678d022a01` requires a proven Qwen3-TTS CustomVoice config, admits only the known 0.6B/1.7B size identities, and requires 1.7B whenever `instruct` is needed. CI 1624 passed on Python 3.11 and 3.12. This change performs local metadata validation only; it does not download weights, provision a GPU, contact Hugging Face, or weaken the eSpeak fallback.

## 2026-08-28 dialogue-input integrity follow-up

Fresh Production review tightened the input contract before any TTS backend is selected.

- PR #143 established that all `AudioCue.text` is trimmed and blank/whitespace-only text fails at the `hottop.video-plan.v1` model boundary.
- PR #145 added a dialogue-specific lexical-content gate: `kind=dialogue` must contain at least one Unicode alphanumeric character. Punctuation-only strings such as `……？！` fail before eSpeak/Qwen/CosyVoice runtime work, while symbolic text remains valid for SFX/Foley descriptions.
- PR #145 TDD evidence: RED `427517bda8c9f086e726375d5b7cba709965433a` failed the new contract; GREEN exact head `e262f1119e60d4a8f4f22bcfca2b345b74124106` passed CI #1935, production-smoke #200 and 720p cinematic-delivery-smoke #67 before merge.
- Post-merge `main@668372e7ed5276df46af7997d5f5aa204f68d5b5` passed CI #1936 and production-smoke #201; the 720p post-merge smoke is tracked separately until complete.

The rule is intentionally input-semantic, not provider-specific. It does **not** claim punctuation-only prompts are the root cause of upstream Qwen failures. It prevents Hottop from spending any speech runtime on a dialogue cue with no lexical speech content.

Fresh upstream evidence supports retaining the existing runtime protections as separate layers. `vllm-project/vllm-omni` issue #4576 reports short Chinese inputs such as `1次`/`2次` intermittently producing 10–36 seconds of garbled Qwen3-TTS output. Hottop therefore keeps both the duration-derived generation-token ceiling (resource protection) and produced-PCM duration gate (artifact truth); lexical input validation does not replace either one.
