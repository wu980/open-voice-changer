from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

DEFAULT_HISTORY_PATH = Path("outputs") / "history.jsonl"


@dataclass(frozen=True)
class HistoryEntry:
    mode: str
    input_path: str
    output_path: str
    semitones: float
    preset: str
    created_at: str


def create_history_entry(
    mode: str,
    input_path: str | Path,
    output_path: str | Path,
    semitones: float,
    preset: str,
) -> HistoryEntry:
    return HistoryEntry(
        mode=mode,
        input_path=str(input_path),
        output_path=str(output_path),
        semitones=float(semitones),
        preset=preset,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def append_history(entry: HistoryEntry, history_path: str | Path = DEFAULT_HISTORY_PATH) -> None:
    path = Path(history_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def record_history(
    mode: str,
    input_path: str | Path,
    output_path: str | Path,
    semitones: float,
    preset: str,
    history_path: str | Path = DEFAULT_HISTORY_PATH,
) -> HistoryEntry:
    entry = create_history_entry(
        mode=mode,
        input_path=input_path,
        output_path=output_path,
        semitones=semitones,
        preset=preset,
    )
    append_history(entry, history_path=history_path)
    return entry


def read_history(history_path: str | Path = DEFAULT_HISTORY_PATH, limit: int = 10) -> list[HistoryEntry]:
    path = Path(history_path)
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[HistoryEntry] = []

    for line in lines[-limit:]:
        if not line.strip():
            continue
        data = json.loads(line)
        entries.append(HistoryEntry(**data))

    return entries
