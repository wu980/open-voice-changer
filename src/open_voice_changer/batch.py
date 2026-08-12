from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from open_voice_changer.audio import convert_pitch
from open_voice_changer.config import build_default_output_path
from open_voice_changer.logging_utils import get_logger

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}


@dataclass(frozen=True)
class BatchItemResult:
    input_path: Path
    output_path: Path | None
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class BatchResult:
    items: list[BatchItemResult]

    @property
    def succeeded(self) -> list[BatchItemResult]:
        return [item for item in self.items if item.succeeded]

    @property
    def failed(self) -> list[BatchItemResult]:
        return [item for item in self.items if not item.succeeded]

    @property
    def success_count(self) -> int:
        return len(self.succeeded)

    @property
    def failure_count(self) -> int:
        return len(self.failed)

    @property
    def total_count(self) -> int:
        return len(self.items)


def is_audio_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in AUDIO_EXTENSIONS


def find_audio_files(input_dir: str | Path) -> list[Path]:
    directory = Path(input_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {directory}")

    return sorted(path for path in directory.iterdir() if path.is_file() and is_audio_file(path))


def build_output_path(
    input_file: str | Path,
    output_dir: str | Path,
    preset: str = "clean",
    semitones: float = 0.0,
    avoid_overwrite: bool = True,
) -> Path:
    return build_default_output_path(
        input_path=input_file,
        output_dir=output_dir,
        preset=preset,
        semitones=semitones,
        avoid_overwrite=avoid_overwrite,
    )


def convert_batch(
    input_files: Iterable[str | Path],
    output_dir: str | Path,
    semitones: float,
    sample_rate: int | None = None,
    preset: str = "clean",
    avoid_overwrite: bool = True,
    on_progress: Callable[[int, int, BatchItemResult], None] | None = None,
) -> BatchResult:
    logger = get_logger()
    files = [Path(path) for path in input_files]
    if not files:
        raise ValueError("No audio files to convert.")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    results: list[BatchItemResult] = []
    total = len(files)

    for index, input_file in enumerate(files, start=1):
        try:
            output_file = build_output_path(
                input_file=input_file,
                output_dir=destination,
                preset=preset,
                semitones=semitones,
                avoid_overwrite=avoid_overwrite,
            )
            result_path = convert_pitch(
                input_path=input_file,
                output_path=output_file,
                semitones=semitones,
                sample_rate=sample_rate,
                preset=preset,
            )
            result = BatchItemResult(input_path=input_file, output_path=result_path)
            logger.info("Batch item converted: input=%s output=%s", input_file, result_path)
        except Exception as exc:
            result = BatchItemResult(input_path=input_file, output_path=None, error=str(exc))
            logger.exception("Batch item failed: input=%s", input_file)

        results.append(result)

        if on_progress is not None:
            on_progress(index, total, result)

    return BatchResult(results)


def convert_directory(
    input_dir: str | Path,
    output_dir: str | Path,
    semitones: float,
    sample_rate: int | None = None,
    preset: str = "clean",
    avoid_overwrite: bool = True,
    on_progress: Callable[[int, int, BatchItemResult], None] | None = None,
) -> BatchResult:
    files = find_audio_files(input_dir)
    return convert_batch(
        input_files=files,
        output_dir=output_dir,
        semitones=semitones,
        sample_rate=sample_rate,
        preset=preset,
        avoid_overwrite=avoid_overwrite,
        on_progress=on_progress,
    )
