# SMRABooth admission review — 2026-08-28

## Decision

Record SMRABooth as a **research/benchmark candidate only**. Do not add an executable `video-run` route, vendor upstream code, auto-install its runtime, download checkpoints/datasets, or claim runtime readiness.

## Why it is relevant

SMRABooth targets customized video generation where subject appearance and motion pattern must both remain consistent. It separates object-level subject representation from optical-flow-derived motion representation and combines sparse subject/motion LoRA injection. This directly matches Hottop's reference-conditioned continuity gap while making subject fidelity and motion fidelity separate controls.

## Reviewed source

- repository: `xuxuancheng0208/SMRABooth`
- exact source revision: `46ae0a59a6041fc22884123a3042ab95b99a2774`
- source license: Apache-2.0 (`LICENSE` present)
- upstream status: full code released; training dataset announced/released 2026-06-14
- published base: `Wan-AI/Wan2.1-T2V-1.3B`
- additional dependency: SEA-RAFT checkpoint

Source licensing does not establish the license/redistribution/publication rights of the dataset, SEA-RAFT checkpoint, base weights, trained LoRAs, or outputs. Those remain separate admission dimensions.

## Runtime and zero-cost fit

The documented setup is operator-managed and Blackwell-oriented: Python 3.11, PyTorch 2.7/CUDA 12.8 wheels, local Wan2.1 and SEA-RAFT checkpoints, prepared customized datasets, and explicit subject/motion LoRA training before inference. It is not a normal unattended Hottop dependency or drop-in inference-only adapter.

Hottop must not auto-run upstream downloads, fetch the Google Drive SEA-RAFT asset, fetch dataset/base weights in CI/normal `video-run`, call the route zero-cost merely because source is permissive, or treat paper/demo results as Hottop continuity evidence.

## Re-admission gate

Re-evaluate only when an operator has already provisioned the exact source/runtime/base/checkpoint assets and a rights-safe subject + motion benchmark pack. Before any executable route:

1. independently record rights for source, base weights, SEA-RAFT, trained LoRAs, benchmark inputs and intended outputs;
2. bind exact source/model/checkpoint revisions and local byte identities where possible;
3. compare against LightX2V/Wan2.2 on the same subject-bearing sequence;
4. require meaningful motion plus complete output-side subject continuity evidence across every subject-bearing shot;
5. measure motion-customization value separately from identity preservation;
6. preserve rollback and the guaranteed software3d baseline.

## Durable lesson

When a candidate claims to control both, evaluate **subject identity fidelity and motion fidelity as separate evidence dimensions**. A consistent subject with incorrect/degenerate motion is not a successful motion-conditioned result, and strong motion does not prove subject identity.