# ruff: noqa
from pathlib import Path

import pytest

from hottop.audio_cosyvoice3 import CosyVoice3Error, _write_pcm16_wav as write_cosy_wav
from hottop.audio_qwen3_tts import Qwen3TTSError, _write_pcm16_wav as write_qwen_wav


@pytest.mark.parametrize(
    ("writer", "error_type"),
    [
        (write_qwen_wav, Qwen3TTSError),
        (write_cosy_wav, CosyVoice3Error),
    ],
)
def test_neural_tts_rejects_silent_nonempty_waveform_before_wav_creation(
    writer, error_type, tmp_path: Path
):
    output = tmp_path / "dialogue.wav"

    with pytest.raises(error_type, match="silent"):
        writer(output, [0.0] * 2400, 24000)

    assert not output.exists()
