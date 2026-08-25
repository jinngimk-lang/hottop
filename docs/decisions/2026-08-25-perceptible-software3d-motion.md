# Perceptible motion is a deterministic production gate

Date: 2026-08-25
Status: accepted for Production v0.2

## Context

Direct inspection of the guaranteed software3d production artifacts showed a false-success class that the existing codec, frame-uniqueness and provenance checks did not catch. The cow and Odyssey outputs were valid MP4s with changing frames, but the motion inside most two-second shots still read as near-static cards. At the shared 4 fps / 96x54 grayscale sampling policy, the measured adjacent-frame mean was only about 0.52 for the Anti-Polish cow story and 0.73 for the cinematic Odyssey story, below the existing generated-video motion policy of 2.0.

Frame uniqueness is therefore insufficient evidence that a narrative video is meaningfully moving.

## Decision

The guaranteed deterministic software3d route must pass a perceptible-motion contract in addition to producing decodable, byte-bound video.

For the current baseline:

- every checked-in story shot moves a stable scene anchor by at least 18 screen pixels from shot start to shot end;
- camera motion includes style-routed depth change rather than only translating the entire frame sideways;
- sampled rendered pixels must reach mean adjacent grayscale delta >= 2.0 and duplicate ratio <= 0.60 under the repository test policy;
- Anti-Polish may use deliberately obvious/awkward pan+dolly motion;
- cinematic Odyssey uses controlled pan+crane+dolly plus a mild focal-length change;
- the numerical gate is shared, but the directing grammar remains style-routed;
- no quality failure may be excused as Controlled Badness.

This policy does not imply that every future backend must use the same implementation or camera amplitudes. It requires equivalent evidence that the delivered narrative motion is perceptible rather than technically frame-unique but functionally frozen.

## Evidence

PR #51 (`Make software3d motion perceptible`) established the closure:

- initial production evidence: ~0.52 cow / ~0.73 Odyssey mean sampled motion;
- CI #1521 demonstrated that the first camera-motion change remained below the intended policy;
- a later CI failure exposed an accidental Pillow-only test dependency; the test was rewritten to parse Hottop's deterministic RGB PNG output with the Python standard library instead of adding Pillow;
- exact PR head `f43762bc8c089a46024b72aa21bb32984b08b589` passed CI #1525 on Python 3.11 and 3.12;
- Odyssey sampled scene means at the accepted head were approximately 2.29 / 2.76 / 2.75 / 2.79 / 2.38 across shots 1–5 with duplicate ratio 0;
- production-smoke #99 completed both checked-in cow and Odyssey config → moving shots → Mandarin audio/music/SFX → MoviePy → FFmpeg → final-media/provenance paths;
- PR #51 was squash-merged as `e00aa91cb24555f3b3d74a1729a28979ae097274`.

Post-merge `main` verification is recorded in `STATUS.md` once the corresponding production-smoke run completes.

## Superseded assumption

The weaker assumption “multiple different frames imply acceptable deterministic video motion” is retired. Frame uniqueness remains useful, but it cannot substitute for perceptible motion evidence.

## Rollback / safety

The change is deterministic and zero-cost. It adds no model, GPU, network, credential or paid dependency. If a future story needs a different camera grammar, adjust the style-routed staging while preserving or replacing the motion evidence contract with an equally strict measured criterion rather than lowering the bar.
