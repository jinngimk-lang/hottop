import pytest
from pydantic import ValidationError

from hottop.video_production import AudioCue


def test_audio_cue_text_is_canonicalized_before_execution():
    cue = AudioCue(
        kind="dialogue",
        start_seconds=0,
        text="  你好，直接干活。  ",
        character="cow",
    )

    assert cue.text == "你好，直接干活。"


def test_audio_cue_rejects_whitespace_only_text_before_tts():
    with pytest.raises(ValidationError, match="audio cue text must be nonblank"):
        AudioCue(
            kind="dialogue",
            start_seconds=0,
            text="  \t\n  ",
            character="cow",
        )


def test_dialogue_audio_cue_requires_speech_bearing_text():
    with pytest.raises(ValidationError, match="dialogue audio cue must contain a letter or number"):
        AudioCue(
            kind="dialogue",
            start_seconds=0,
            text="……？！",
            character="cow",
        )


def test_non_dialogue_audio_cue_may_use_symbolic_text():
    cue = AudioCue(
        kind="sfx",
        start_seconds=0,
        text="……？！",
    )

    assert cue.text == "……？！"
