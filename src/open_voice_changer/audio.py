from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


def load_audio(path: str | Path, sample_rate: int | None = None) -> tuple[np.ndarray, int]:
    """Load an audio file as mono floating-point samples."""
    audio_path = Path(path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Input audio file does not exist: {audio_path}")

    samples, sr = librosa.load(audio_path, sr=sample_rate, mono=True)
    return samples, sr


def pitch_shift(samples: np.ndarray, sample_rate: int, semitones: float) -> np.ndarray:
    """Shift pitch by a number of semitones while keeping duration similar."""
    if samples.size == 0:
        raise ValueError("Input audio is empty.")

    shifted = librosa.effects.pitch_shift(
        y=samples,
        sr=sample_rate,
        n_steps=semitones,
    )
    return np.asarray(shifted, dtype=np.float32)


def save_audio(path: str | Path, samples: np.ndarray, sample_rate: int) -> None:
    """Save samples to an audio file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, samples, sample_rate)


def convert_pitch(
    input_path: str | Path,
    output_path: str | Path,
    semitones: float,
    sample_rate: int | None = None,
) -> Path:
    """Load an audio file, shift pitch, and write the converted file."""
    samples, sr = load_audio(input_path, sample_rate=sample_rate)
    shifted = pitch_shift(samples, sr, semitones)
    save_audio(output_path, shifted, sr)
    return Path(output_path)
