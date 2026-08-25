import {Rect, Txt, makeScene2D} from '@motion-canvas/2d';
import {waitFor} from '@motion-canvas/core';

import plan from '../generated-plan';

const shotAssetPath = (index: number): string =>
  `/shots/shot-${String(index).padStart(3, '0')}.mp4`;

export default makeScene2D(function* (view) {
  let cursor = 0;

  for (const shot of plan.shots) {
    const gap = Math.max(0, shot.start_seconds - cursor);
    if (gap > 0) {
      yield* waitFor(gap);
    }

    const activeAudio = plan.audio_cues
      .filter(cue => cue.start_seconds >= shot.start_seconds && cue.start_seconds < shot.end_seconds)
      .map(cue => `${cue.kind}: ${cue.text}`)
      .join('\n');

    view.removeChildren();
    view.add(
      <Rect width={plan.width} height={plan.height} fill={'#171717'} layout direction={'column'} gap={28} padding={48}>
        <Txt
          fill={'#f5f5f5'}
          fontFamily={'sans-serif'}
          fontSize={38}
          text={`SHOT ${shot.index}\n${shot.scene}`}
          textWrap
        />
        <Txt
          fill={'#b5b5b5'}
          fontFamily={'monospace'}
          fontSize={24}
          text={`input: ${shotAssetPath(shot.index)}\nintent: ${shot.intent}`}
          textWrap
        />
        {shot.caption ? (
          <Txt fill={'#ffffff'} fontFamily={'sans-serif'} fontSize={46} text={shot.caption} textWrap />
        ) : null}
        {activeAudio ? (
          <Txt fill={'#d4d4d4'} fontFamily={'monospace'} fontSize={20} text={activeAudio} textWrap />
        ) : null}
      </Rect>,
    );

    yield* waitFor(shot.duration_seconds);
    cursor = shot.end_seconds;
  }

  if (cursor < plan.duration_seconds) {
    yield* waitFor(plan.duration_seconds - cursor);
  }
});
