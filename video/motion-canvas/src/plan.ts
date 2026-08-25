export type HottopVideoShot = {
  index: number;
  start_seconds: number;
  end_seconds: number;
  duration_seconds: number;
  scene: string;
  caption: string | null;
  intent: string;
};

export type HottopAudioCue = {
  kind: 'dialogue' | 'foley' | 'sfx' | 'bgm';
  start_seconds: number;
  duration_seconds: number | null;
  text: string;
  character: string | null;
};

export type HottopVideoPlan = {
  schema_version: 'hottop.video-plan.v1';
  width: number;
  height: number;
  fps: number;
  duration_seconds: number;
  shots: HottopVideoShot[];
  audio_cues: HottopAudioCue[];
};
