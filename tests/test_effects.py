import numpy as np
import pytest

from open_voice_changer.effects import apply_preset, preset_names, validate_preset


def test_preset_names_include_expected_presets() -> None:
    assert preset_names() == ["clean", "deep", "bright", "robot", "radio"]


def test_validate_preset_accepts_case_insensitive_names() -> None:
    assert validate_preset("Deep") == "deep"


def test_validate_preset_rejects_unknown_name() -> None:
    with pytest.raises(ValueError):
        validate_preset("alien")


@pytest.mark.parametrize("preset", preset_names())
def test_apply_preset_returns_audio_for_every_preset(preset: str) -> None:
    sample_rate = 22050
    samples = np.linspace(-0.5, 0.5, sample_rate // 10, dtype=np.float32)

    processed = apply_preset(samples, sample_rate, preset=preset)

    assert processed.size == samples.size
    assert processed.dtype == np.float32
    assert np.max(np.abs(processed)) <= 1.0
