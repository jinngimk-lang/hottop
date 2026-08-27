from pathlib import Path

import pytest

from hottop.audio_cosyvoice3 import CosyVoice3Error
from hottop.audio_cosyvoice3 import _write_pcm16_wav as write_cosy_wav
from hottop.audio_qwen3_tts import Qwen3TTSError
from hottop.audio_qwen3_tts import _write_pcm16_wav as write_qwen_wav


@pytest.mark.parametrize(
    ("writer", "error_type"),
    [
        (write_qwen_wav, Qwen3TTSError),
        (write_cosy_wav, CosyVoice3Error),
    ],
)
def test_neural_tts_rejects_signal_that_quantizes_to_digital_silence(
    tmp_path: Path,
    writer,
    error_type,
):
    output = tmp_path / "dialogue.wav"

    with pytest.raises(error_type, match="silent audio"):
        writer(output, [1e-12, -1e-12, 1e-12], 24000)

    assert not output.exists()
