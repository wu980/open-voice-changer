from pathlib import Path

import pytest

from open_voice_changer import batch
from open_voice_changer.batch import build_output_path, convert_batch, find_audio_files, is_audio_file


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
    output = build_output_path("input/song.mp3", tmp_path, preset="radio", semitones=4)

    assert output == tmp_path / "song-radio-+4.wav"


def test_convert_batch_continues_after_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    good = tmp_path / "good.wav"
    bad = tmp_path / "bad.wav"
    good.write_text("fake audio")
    bad.write_text("fake audio")

    def fake_convert_pitch(input_path, output_path, semitones, sample_rate=None, preset="clean"):
        if Path(input_path).name == "bad.wav":
            raise ValueError("cannot decode audio")
        Path(output_path).write_text("converted")
        return Path(output_path)

    monkeypatch.setattr(batch, "convert_pitch", fake_convert_pitch)

    result = convert_batch(
        input_files=[good, bad],
        output_dir=tmp_path / "outputs",
        semitones=0,
    )

    assert result.total_count == 2
    assert result.success_count == 1
    assert result.failure_count == 1
    assert result.succeeded[0].output_path is not None
    assert result.failed[0].input_path == bad
    assert result.failed[0].error == "cannot decode audio"
