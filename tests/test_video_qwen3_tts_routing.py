from pathlib import Path

from hottop.video_execution import _runtime_audio_commands
from hottop.video_production import AudioCue, VideoProductionConfig, VideoProductionPlan


def _config(model_dir: Path) -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "qwen3-local-test",
            "style_profile": "cinematic",
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 2.0,
            "shot_policy": {
                "min_shot_seconds": 1.0,
                "max_shot_seconds": 3.0,
            },
            "audio": {
                "bgm_style": "original synthetic score",
                "foley_style": "procedural",
                "voice_backend": "qwen3-customvoice",
                "voice_language": "zh",
                "qwen3_custom_voice": {
                    "model_dir": str(model_dir),
                    "default_speaker": "Vivian",
                    "speaker_map": {
                        "young-cow": "Dylan",
                        "mother-cow": "Vivian",
                    },
                    "language": "Chinese",
                    "device": "cuda:0",
                    "dtype": "bfloat16",
                    "attn_implementation": "flash_attention_2",
                },
            },
            "text": {},
            "moviepy": {},
            "ffmpeg": {},
        }
    )


def _plan() -> VideoProductionPlan:
    return VideoProductionPlan.model_validate(
        {
            "config_name": "qwen3-local-test",
            "topic_id": "cow",
            "topic_title": "cow",
            "subject_name": "InkClawAgent",
            "style_profile": "cinematic",
            "roughness_score": 20,
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 2.0,
            "output_format": "mp4",
            "in_asset_cta_policy": "no-destination",
            "shots": [
                {
                    "index": 1,
                    "start_seconds": 0.0,
                    "end_seconds": 2.0,
                    "duration_seconds": 2.0,
                    "scene": "scene",
                    "intent": "intent",
                    "continuity_instruction": "same world",
                    "generation_prompt": "prompt",
                    "negative_prompt": "none",
                }
            ],
            "audio_cues": [
                AudioCue(
                    kind="dialogue",
                    start_seconds=0.0,
                    duration_seconds=0.8,
                    text="妈——！",
                    character="young-cow",
                    delivery="brief panicked call for help",
                ),
                AudioCue(
                    kind="dialogue",
                    start_seconds=1.0,
                    duration_seconds=0.8,
                    text="傻孩子，用 InkClawAgent。",
                    character="mother-cow",
                    delivery="calm deadpan maternal Mandarin",
                ),
            ],
        }
    )


def test_qwen3_video_routing_maps_character_and_delivery_to_local_custom_voice(tmp_path: Path) -> None:
    model_dir = tmp_path / "qwen3-model"
    model_dir.mkdir()
    config = _config(model_dir)

    commands = _runtime_audio_commands(
        _plan(),
        config,
        project_root=tmp_path,
        audio_dir=tmp_path / "audio",
    )

    assert len(commands) == 2
    first, second = commands
    assert first.program.endswith("python") or "python" in first.program.lower()
    assert first.args[:2] == ["-m", "hottop.audio_qwen3_tts"]
    assert first.args[first.args.index("--speaker") + 1] == "Dylan"
    assert second.args[second.args.index("--speaker") + 1] == "Vivian"
    assert first.args[first.args.index("--instruct") + 1] == "brief panicked call for help"
    assert second.args[second.args.index("--instruct") + 1] == "calm deadpan maternal Mandarin"
    assert first.args[first.args.index("--model-dir") + 1] == str(model_dir.resolve())
    assert first.args[first.args.index("--output") + 1].endswith("dialogue-001.wav")
