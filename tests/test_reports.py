from pathlib import Path
import csv

from open_voice_changer.batch import BatchItemResult, BatchResult
from open_voice_changer.reports import build_report_path, write_batch_report


def test_build_report_path_avoids_overwrite(tmp_path: Path) -> None:
    existing = tmp_path / "report.csv"
    existing.write_text("old report")

    report_path = build_report_path(tmp_path)

    assert report_path == tmp_path / "report-1.csv"


def test_write_batch_report_writes_success_and_failure_rows(tmp_path: Path) -> None:
    result = BatchResult(
        [
            BatchItemResult(
                input_path=Path("input/good.wav"),
                output_path=Path("outputs/good.wav"),
            ),
            BatchItemResult(
                input_path=Path("input/bad.wav"),
                output_path=None,
                error="cannot decode audio",
            ),
        ]
    )

    report_path = write_batch_report(
        result=result,
        output_dir=tmp_path,
        preset="radio",
        semitones=4,
    )

    with report_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["status"] == "success"
    assert rows[0]["output_path"] == "outputs\\good.wav" or rows[0]["output_path"] == "outputs/good.wav"
    assert rows[0]["preset"] == "radio"
    assert rows[0]["semitones"] == "4"
    assert rows[1]["status"] == "failed"
    assert rows[1]["output_path"] == ""
    assert rows[1]["error"] == "cannot decode audio"
