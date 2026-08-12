from collections.abc import Callable, Iterable
from pathlib import Path

from open_voice_changer.audio import convert_pitch

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}


def is_audio_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in AUDIO_EXTENSIONS


def find_audio_files(input_dir: str | Path) -> list[Path]:
    directory = Path(input_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {directory}")

    return sorted(path for path in directory.iterdir() if path.is_file() and is_audio_file(path))


def build_output_path(input_file: str | Path, output_dir: str | Path, suffix: str = "-converted") -> Path:
    source = Path(input_file)
    return Path(output_dir) / f"{source.stem}{suffix}.wav"


def convert_batch(
    input_files: Iterable[str | Path],
    output_dir: str | Path,
    semitones: float,
    sample_rate: int | None = None,
    on_progress: Callable[[int, int, Path], None] | None = None,
) -> list[Path]:
    files = [Path(path) for path in input_files]
    if not files:
        raise ValueError("No audio files to convert.")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    results: list[Path] = []
    total = len(files)

    for index, input_file in enumerate(files, start=1):
        output_file = build_output_path(input_file, destination)
        result = convert_pitch(
            input_path=input_file,
            output_path=output_file,
            semitones=semitones,
            sample_rate=sample_rate,
        )
        results.append(result)

        if on_progress is not None:
            on_progress(index, total, result)

    return results


def convert_directory(
    input_dir: str | Path,
    output_dir: str | Path,
    semitones: float,
    sample_rate: int | None = None,
    on_progress: Callable[[int, int, Path], None] | None = None,
) -> list[Path]:
    files = find_audio_files(input_dir)
    return convert_batch(
        input_files=files,
        output_dir=output_dir,
        semitones=semitones,
        sample_rate=sample_rate,
        on_progress=on_progress,
    )
