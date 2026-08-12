from pathlib import Path

import pytest

from open_voice_changer.config import (
    AppConfig,
    build_default_output_path,
    build_output_filename,
    load_config,
    save_config,
    update_config,
)


def test_load_config_returns_defaults_for_missing_file(tmp_path: Path) -> None:
    assert load_config(tmp_path / "missing.json") == AppConfig()


def test_save_and_load_config_round_trip(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config = AppConfig(default_output_dir="rendered", default_preset="deep", default_semitones=-3)

    save_config(config, config_path)

    assert load_config(config_path) == config


def test_update_config_validates_unknown_fields(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        update_config({"unknown": "value"}, tmp_path / "config.json")


def test_update_config_validates_preset(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        update_config({"default_preset": "alien"}, tmp_path / "config.json")


def test_build_output_filename_includes_preset_and_semitones() -> None:
    assert build_output_filename("voice.wav", "deep", -3) == "voice-deep--3.wav"
    assert build_output_filename("voice.wav", "bright", 2.5) == "voice-bright-+2p5.wav"


def test_build_default_output_path_avoids_overwrite(tmp_path: Path) -> None:
    existing = tmp_path / "voice-deep--3.wav"
    existing.write_text("already here")

    output = build_default_output_path("voice.wav", tmp_path, "deep", -3)

    assert output == tmp_path / "voice-deep--3-1.wav"
