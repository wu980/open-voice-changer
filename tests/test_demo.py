from pathlib import Path

import soundfile as sf

from open_voice_changer.demo import create_demo_outputs, generate_demo_audio


def test_generate_demo_audio_writes_file(tmp_path: Path) -> None:
    output = generate_demo_audio(tmp_path / "demo.wav", duration_seconds=0.1)

    samples, sample_rate = sf.read(output)

    assert output.exists()
    assert sample_rate == 22050
    assert samples.size > 0


def test_create_demo_outputs_writes_input_and_presets(tmp_path: Path) -> None:
    results = create_demo_outputs(tmp_path)

    assert [path.name for path in results] == [
        "demo-input.wav",
        "demo-clean.wav",
        "demo-deep.wav",
        "demo-bright.wav",
        "demo-robot.wav",
        "demo-radio.wav",
    ]
    assert all(path.exists() for path in results)
