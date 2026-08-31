# Terminal-frame proof for generated-video integrity

Date: 2026-09-01

## Measured gap

The shared generated-video quality gate previously treated a zero `ffmpeg` exit code from the terminal probe as proof that the terminal frame decoded. The probe wrote to the null muxer, so the gate never observed decoded terminal-frame bytes. A zero-exit probe with no decoded frame payload could therefore produce the over-strong conclusion `terminal_frame_decodable=true`.

This is a final-media/generated-shot integrity defect, not a style decision: truncated or malformed tails must fail closed before generated media can be trusted for downstream identity, requested-action or composition evaluation.

## TDD evidence

RED commit: `bac333db261312daca8decd568f17bf3327c0c43`.

The new regression case supplies otherwise valid 2.0 s / 768×512 / 24 fps metadata and changing motion samples, while the terminal probe returns code 0 with an empty payload. On the prior implementation, Python 3.11 CI failed exactly on this case with `1 failed, 636 passed`: the report incorrectly remained `pass_=true` and `terminal_frame_decodable=true`.

GREEN exact head: `6b587eb1f9f95b1125e9f249994fb52d19b857be`.

Minimal implementation change:

- ask FFmpeg for exactly one gray raw terminal frame on `pipe:1`;
- require both `returncode == 0` and a non-empty decoded frame payload;
- otherwise retain the existing fail-closed reason `terminal frame not decodable`.

No provider routing, model behavior, network access, provisioning, download or paid fallback changed.

## Exact-head verification

On GREEN head `6b587eb1f9f95b1125e9f249994fb52d19b857be`:

- CI #2577 passed Python 3.11 and Python 3.12 Ruff + full pytest;
- production-smoke #288 passed both checked-in anti-polish cow and cinematic Odyssey execution, final-media/provenance verification and evidence upload;
- artifact `hottop-software3d-production-smoke`: 688,374 bytes, archive digest `sha256:06dd3368eb0ee8ef1f8b5b3bcae8a3eb0d409913be287b24240114e912f16b1f`;
- cinematic-delivery-smoke #155 passed actual 720p24 Odyssey delivery, runtime provenance, media/provenance verification and evidence upload;
- artifact `hottop-cinematic-software3d-delivery`: 624,450 bytes, archive digest `sha256:4ca096d287d373598608bd2d71de693ab7b018f446bb6ba4a2dc60e4143dd7af`.

PR #367 was SHA-locked squash-merged as `7ea0c2a52d336e262e6df11165c3440789b8e244`.

## Ecosystem radar consequence

LightX2V public tip remained `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`; its newest material work repairs SeedVR distributed operations and does not demonstrate Hottop-measured Wan2.2 I2V identity or requested-action gains. Continue no freshness-only repin.

A public LightX2V Wan2.2-TI2V-5B I2V report also shows meaningless color blocks/light patterns despite a runnable generation path. That is consistent with Hottop's existing doctrine: runtime success, decodability and generic motion are necessary but not sufficient evidence for semantic correctness, identity continuity or requested-action fidelity.

No ecosystem candidate in this cycle clears admission strongly enough to change the current zero-cost baseline or LightX2V operator route.

## Scope and rollback

This is a narrow local FFmpeg integrity hardening. It uses no optional heavy dependency and preserves bounded local execution. If a real compatibility defect is demonstrated, rollback is a direct revert of PR #367 while retaining the regression evidence for redesign.

`PROJECT.md` is intentionally unchanged because this work implements the existing generated-media/final-media integrity doctrine rather than changing durable project direction.
