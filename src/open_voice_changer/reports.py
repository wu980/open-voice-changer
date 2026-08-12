from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from open_voice_changer.batch import BatchResult
from open_voice_changer.config import ensure_unique_path

REPORT_FIELDS = [
    "created_at",
    "status",
    "input_path",
    "output_path",
    "error",
    "preset",
    "semitones",
]


def build_report_path(output_dir: str | Path, filename: str = "report.csv") -> Path:
    return ensure_unique_path(Path(output_dir) / filename)


def write_batch_report(
    result: BatchResult,
    output_dir: str | Path,
    preset: str,
    semitones: float,
    report_path: str | Path | None = None,
) -> Path:
    path = Path(report_path) if report_path is not None else build_report_path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        for item in result.items:
            writer.writerow(
                {
                    "created_at": created_at,
                    "status": "success" if item.succeeded else "failed",
                    "input_path": str(item.input_path),
                    "output_path": "" if item.output_path is None else str(item.output_path),
                    "error": "" if item.error is None else item.error,
                    "preset": preset,
                    "semitones": f"{float(semitones):g}",
                }
            )

    return path
