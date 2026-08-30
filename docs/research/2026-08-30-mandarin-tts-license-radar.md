# Mandarin TTS license/runtime radar — 2026-08-30

## Decision

No new unattended or production TTS route is admitted by this review.

Two candidates were re-checked because they could materially reduce the current Mandarin-quality gap if their rights/runtime surfaces became clean enough:

1. Step-Audio-EditX / Step-Audio-Tokenizer;
2. Supertonic 3 / unofficial Supertonic-ZH.

The result is deliberately asymmetric: Step-Audio-Tokenizer now has an explicit `apache-2.0` model-card license surface, but Step-Audio-EditX still has conflicting/insufficient checkpoint-license evidence; official Supertonic 3 still does not support Mandarin, while the available Mandarin preview is gated and non-commercial/evaluation-only.

## Step-Audio-EditX re-check

Reviewed public surfaces on 2026-08-30:

- `stepfun-ai/Step-Audio-Tokenizer` currently exposes `license: apache-2.0` in its Hugging Face model-card metadata;
- `stepfun-ai/Step-Audio-EditX` has historical Hugging Face revisions whose README metadata contains `license: apache-2.0`;
- the current Step-Audio-EditX model page, however, still shows a YAML metadata warning and its detailed `License Agreement` wording states that the **code in the open-source repository** is Apache-2.0;
- the model repository contains multi-GB released checkpoint shards, but no independently reviewed checkpoint-specific license file/text was found in this pass that resolves the code-vs-weights ambiguity;
- the official local setup remains CUDA/PyTorch based, with model repositories cloned/downloaded separately before local inference.

### Admission result

Keep Step-Audio-EditX **research / benchmark signal only** for now.

The tokenizer's clearer Apache-2.0 metadata is useful but does not automatically license the main Step-Audio-EditX checkpoint family. Hottop must keep these separate:

1. source-code license;
2. Step-Audio-EditX checkpoint license;
3. Step-Audio-Tokenizer checkpoint license;
4. prompt/reference-audio rights;
5. generated-output publication rights.

Re-admit only if the main checkpoint surface becomes unambiguous enough that a reasonable operator can bind exact checkpoint bytes to a clear grant without relying on an inferred or conflicting model-card convention.

## Supertonic 3 / Mandarin re-check

Official `Supertone/supertonic-3` remains a compact, on-device ONNX TTS family and does not require a GPU. Its official language list still omits Mandarin Chinese.

A community Mandarin preview (`dove88/supertonic-zh`) exists, but the reviewed public model card states:

- it is unofficial;
- access is gated;
- the current build is evaluation-only / non-commercial because of its training-data basis;
- commercial licensing is a separate path;
- example usage may enable automatic model download.

### Admission result

Do **not** add Supertonic-ZH to Hottop's model hub or normal benchmark route.

The official Supertonic 3 runtime remains interesting as a low-cost/on-device architecture reference, but lack of official Mandarin support means it does not address the current measured Mandarin gap. The community Mandarin preview fails the zero-cost commercial/rights admission boundary.

## What this review changes

Nothing in production routing.

- eSpeak family remains the guaranteed local fallback.
- Qwen3-TTS 1.7B remains the primary operator-owned Mandarin quality target.
- qwentts.cpp / CrispASR / audio.cpp remain the prepared local cross-runtime benchmark candidates.
- Step-Audio-EditX remains gated pending unambiguous main-checkpoint licensing.
- Supertonic-ZH remains non-admitted due to gated/non-commercial Mandarin weights.

## Re-admission triggers

Re-open this review only if one of the following becomes true:

- StepFun publishes explicit checkpoint-license metadata/text for Step-Audio-EditX itself that resolves the current ambiguity;
- Supertone releases official Mandarin support under rights compatible with Hottop's intended use;
- a third-party Mandarin Supertonic release provides a clear commercially compatible model license and rights-clean training/data statement;
- operator-local evidence shows a new route can materially beat the existing prepared candidates under Hottop's same-line Mandarin A/B protocol without violating the no-auto-download/no-paid-fallback policy.

Upstream support claims or a successful demo are not production-quality evidence.