from pathlib import Path

from open_voice_changer.history import read_history, record_history


def test_read_history_returns_empty_list_for_missing_file(tmp_path: Path) -> None:
    assert read_history(tmp_path / "missing.jsonl") == []


def test_record_history_appends_entry(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"

    entry = record_history(
        mode="single",
        input_path="input.wav",
        output_path="outputs/result.wav",
        semitones=-3,
        preset="deep",
        history_path=history_path,
    )
    entries = read_history(history_path)

    assert history_path.exists()
    assert entries == [entry]
    assert entries[0].mode == "single"
    assert entries[0].preset == "deep"


def test_read_history_respects_limit(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"

    for index in range(3):
        record_history(
            mode="single",
            input_path=f"input-{index}.wav",
            output_path=f"output-{index}.wav",
            semitones=index,
            preset="clean",
            history_path=history_path,
        )

    entries = read_history(history_path, limit=2)

    assert [entry.output_path for entry in entries] == ["output-1.wav", "output-2.wav"]
