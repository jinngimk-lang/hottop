import type {HottopVideoPlan} from './plan';

const plan: HottopVideoPlan = {
  schema_version: 'hottop.video-plan.v1',
  width: 720,
  height: 1280,
  fps: 24,
  duration_seconds: 1,
  shots: [
    {
      index: 1,
      start_seconds: 0,
      end_seconds: 1,
      duration_seconds: 1,
      scene: 'Run npm run render -- --plan <hottop-video-plan.json> to load a production plan.',
      caption: null,
      intent: 'placeholder',
    },
  ],
  audio_cues: [],
};

export default plan;
