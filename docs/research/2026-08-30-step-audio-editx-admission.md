# Step-Audio-EditX admission review — 2026-08-30

## Decision

**Research / benchmark signal only. Do not add an executable Hottop route or model-hub benchmark candidate yet.**

Step-Audio-EditX is unusually relevant to Hottop's Mandarin-quality gap: it supports Mandarin zero-shot TTS, explicit emotion/speaking-style/paralinguistic control, local inference and a relatively modest single-GPU footprint. The reviewed source repository is Apache-2.0. However, the public model-card surface does not provide a sufficiently explicit, independently machine-readable **weights/checkpoint license** for Hottop to treat the released model artifacts as production-admissible. StepFun maintainers have stated in a Hugging Face discussion that they intend Apache-2.0 terms, but the model card's license wording still specifically says the **code** is Apache-2.0. Under Hottop's code-vs-weights separation rule, that ambiguity keeps the weights fail-closed.

This candidate may be re-reviewed if StepFun publishes unambiguous checkpoint-license metadata/text for Step-Audio-EditX and Step-Audio-Tokenizer.

## Reviewed provenance

- Source repository: `stepfun-ai/Step-Audio-EditX`
- Exact reviewed source revision: `a652e87052c109e26f616d60971376ff47a829d4`
- Repository source license: Apache-2.0 (GitHub repository license metadata)
- Public model artifacts referenced upstream:
  - `stepfun-ai/Step-Audio-EditX`
  - `stepfun-ai/Step-Audio-EditX-AWQ-4bit`
  - `stepfun-ai/Step-Audio-Tokenizer`
- Public model-card wording reviewed on 2026-08-30: model checkpoints are released, while the explicit License Agreement wording says the **code in the open-source repository** is Apache-2.0.
- Official Hugging Face discussion reviewed on 2026-08-30: StepFun maintainers state that they adopt Apache-2.0, but the thread itself exists because users identified ambiguity between code and checkpoint licensing. Hottop does not convert that discussion into a stronger machine-readable weights grant than the published model surface currently provides.

## Why it is relevant

The upstream project reports:

- Mandarin, English, Sichuanese, Cantonese, Japanese and Korean support;
- zero-shot TTS / voice cloning from prompt audio;
- explicit emotion controls;
- speaking-style controls such as child, older, whisper, serious, warm, radio and advertising;
- paralinguistic controls including sigh, inhale/exhale, laughter, chuckle, cough and related cues;
- local inference with a 3B model;
- roughly 12 GB critical GPU memory and 16 GB as a safer target for the standard path;
- a local-only model-source option after artifacts have been downloaded;
- optional AWQ 4-bit quantization and vLLM support.

These features map directly to Hottop's first-class `speaker + delivery` contract and could eventually provide a useful independent Mandarin expressive-TTS comparison against Qwen3-TTS 1.7B.

## Runtime and unattended-policy review

The official setup is **not** compatible with normal unattended `ZERO_COST_MODE=true` execution as published:

- it requires an NVIDIA CUDA runtime;
- setup instructions explicitly clone/download model repositories from Hugging Face;
- the application supports model-source modes that include remote Hugging Face / ModelScope behavior;
- voice cloning requires prompt audio, which is separately rights-gated.

Therefore Hottop must not call upstream download/setup paths automatically. A future adapter, if ever admitted, must use only operator-provisioned local source/runtime/model paths and must fail closed before any network/model download.

## Rights and safety boundary

Keep these dimensions separate:

1. source-code license;
2. Step-Audio-EditX checkpoint license;
3. Step-Audio-Tokenizer checkpoint license;
4. prompt/reference-audio rights for zero-shot cloning;
5. dataset/training provenance where relevant;
6. generated-output publication rights and claim posture.

Do not use voice cloning unless the operator supplies rights-cleared reference audio and authority to synthesize that voice. Hottop should prefer preset/non-cloning expressive speech for ordinary benchmark comparisons when available.

## Re-admission gate

Reconsider a model-hub `benchmark_candidate` only when all of the following are true:

1. StepFun publishes clear checkpoint-license metadata/text for both required model artifact families, compatible with the intended use;
2. operator has already provisioned exact source/runtime/model bytes locally;
3. Hottop can run in explicit local/offline mode with no hidden model download;
4. exact model/tokenizer/source/runtime identities can be bound into benchmark provenance;
5. the same Mandarin lines are compared against the existing qwentts.cpp / CrispASR / audio.cpp Qwen3-TTS 1.7B candidates under bounded generation settings;
6. output evidence separately covers PCM integrity, duration, repeated speaker consistency, short-onset stability, intelligibility, naturalness, delivery adherence, latency/RTF and publication-rights posture.

A public demo, leaderboard position, runtime launch success or upstream quality claim is not enough.

## Current action

No executable adapter, registry entry, dependency, model download, GPU provisioning, hosted call, credential or paid fallback is added by this review.