from pathlib import Path

import pytest

from open_voice_changer import player
from open_voice_changer.player import open_audio


def test_open_audio_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        open_audio(tmp_path / "missing.wav")


def test_open_audio_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(IsADirectoryError):
        open_audio(tmp_path)


def test_open_audio_uses_windows_startfile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    audio = tmp_path / "voice.wav"
    audio.write_text("fake audio")
    opened: list[Path] = []

    monkeypatch.setattr(player.platform, "system", lambda: "Windows")
    monkeypatch.setattr(player.os, "startfile", lambda path: opened.append(Path(path)), raising=False)

    result = open_audio(audio)

    assert result == audio
    assert opened == [audio]
