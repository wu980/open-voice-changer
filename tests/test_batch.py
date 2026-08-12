from pathlib import Path

import pytest

from open_voice_changer.batch import build_output_path, find_audio_files, is_audio_file


def test_is_audio_file_matches_supported_extensions() -> None:
    assert is_audio_file("voice.wav")
    assert is_audio_file("voice.MP3")
    assert is_audio_file("voice.flac")
    assert not is_audio_file("notes.txt")


def test_find_audio_files_returns_sorted_audio_files(tmp_path: Path) -> None:
    (tmp_path / "b.mp3").write_text("fake audio")
    (tmp_path / "a.wav").write_text("fake audio")
    (tmp_path / "notes.txt").write_text("not audio")

    files = find_audio_files(tmp_path)

    assert [path.name for path in files] == ["a.wav", "b.mp3"]


def test_find_audio_files_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        find_audio_files(tmp_path / "missing")


def test_build_output_path_uses_wav_output(tmp_path: Path) -> None:
    output = build_output_path("input/song.mp3", tmp_path)

    assert output == tmp_path / "song-converted.wav"
