from pathlib import Path

import numpy as np

from open_voice_changer.audio import convert_pitch, save_audio
from open_voice_changer.effects import preset_names


def generate_demo_audio(
    output_path: str | Path,
    sample_rate: int = 22050,
    duration_seconds: float = 2.0,
) -> Path:
    """Generate a short synthetic demo voice-like tone."""
    output = Path(output_path)
    time = np.linspace(
        0,
        duration_seconds,
        int(sample_rate * duration_seconds),
        endpoint=False,
        dtype=np.float32,
    )

    envelope = np.minimum(time * 6, 1.0) * np.minimum((duration_seconds - time) * 6, 1.0)
    vibrato = 1 + 0.025 * np.sin(2 * np.pi * 5 * time)
    fundamental = 180 * vibrato

    phase = 2 * np.pi * np.cumsum(fundamental) / sample_rate
    samples = (
        0.55 * np.sin(phase)
        + 0.25 * np.sin(2 * phase)
        + 0.12 * np.sin(3 * phase)
    )
    samples = (samples * envelope).astype(np.float32)

    save_audio(output, samples, sample_rate)
    return output


def create_demo_outputs(
    output_dir: str | Path = Path("outputs") / "demo",
    sample_rate: int = 22050,
) -> list[Path]:
    """Create demo input audio and one output file for every preset."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    input_file = generate_demo_audio(destination / "demo-input.wav", sample_rate=sample_rate)
    results = [input_file]

    preset_semitones = {
        "clean": 0,
        "deep": -4,
        "bright": 3,
        "robot": 0,
        "radio": 0,
    }

    for preset in preset_names():
        output_file = destination / f"demo-{preset}.wav"
        result = convert_pitch(
            input_path=input_file,
            output_path=output_file,
            semitones=preset_semitones[preset],
            sample_rate=sample_rate,
            preset=preset,
        )
        results.append(result)

    return results
