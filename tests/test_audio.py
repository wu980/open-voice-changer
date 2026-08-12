import numpy as np

from open_voice_changer.audio import pitch_shift


def test_pitch_shift_keeps_audio_non_empty() -> None:
    sample_rate = 22050
    duration_seconds = 0.25
    time = np.linspace(
        0,
        duration_seconds,
        int(sample_rate * duration_seconds),
        endpoint=False,
    )
    samples = np.sin(2 * np.pi * 440 * time).astype(np.float32)

    shifted = pitch_shift(samples, sample_rate, semitones=2)

    assert shifted.size > 0
    assert shifted.dtype == np.float32
