from pathlib import Path

import click

from open_voice_changer.audio import convert_pitch
from open_voice_changer.batch import convert_directory
from open_voice_changer.demo import create_demo_outputs
from open_voice_changer.effects import preset_names
from open_voice_changer.history import read_history, record_history


@click.group()
def main() -> None:
    """Open Voice Changer command line tools."""


@main.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.argument(
    "output_file",
    type=click.Path(dir_okay=False, path_type=Path),
)
@click.option(
    "--semitones",
    "-s",
    default=0.0,
    show_default=True,
    type=float,
    help="Pitch shift amount. Positive is higher, negative is lower.",
)
@click.option(
    "--sample-rate",
    "-r",
    default=None,
    type=int,
    help="Optional target sample rate, for example 44100.",
)
@click.option(
    "--preset",
    "-p",
    default="clean",
    show_default=True,
    type=click.Choice(preset_names(), case_sensitive=False),
    help="Voice effect preset.",
)
def shift(
    input_file: Path,
    output_file: Path,
    semitones: float,
    sample_rate: int | None,
    preset: str,
) -> None:
    """Shift the pitch of INPUT_FILE and save OUTPUT_FILE."""
    result = convert_pitch(
        input_path=input_file,
        output_path=output_file,
        semitones=semitones,
        sample_rate=sample_rate,
        preset=preset,
    )
    record_history(
        mode="single",
        input_path=input_file,
        output_path=result,
        semitones=semitones,
        preset=preset,
    )
    click.echo(f"Saved converted audio: {result}")


@main.command("batch")
@click.argument(
    "input_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.argument(
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "--semitones",
    "-s",
    default=0.0,
    show_default=True,
    type=float,
    help="Pitch shift amount for every audio file.",
)
@click.option(
    "--sample-rate",
    "-r",
    default=None,
    type=int,
    help="Optional target sample rate, for example 44100.",
)
@click.option(
    "--preset",
    "-p",
    default="clean",
    show_default=True,
    type=click.Choice(preset_names(), case_sensitive=False),
    help="Voice effect preset for every audio file.",
)
def batch(
    input_dir: Path,
    output_dir: Path,
    semitones: float,
    sample_rate: int | None,
    preset: str,
) -> None:
    """Convert all supported audio files in INPUT_DIR."""

    def show_progress(index: int, total: int, result: Path) -> None:
        click.echo(f"[{index}/{total}] Saved: {result}")

    results = convert_directory(
        input_dir=input_dir,
        output_dir=output_dir,
        semitones=semitones,
        sample_rate=sample_rate,
        preset=preset,
        on_progress=show_progress,
    )
    record_history(
        mode="batch",
        input_path=input_dir,
        output_path=output_dir,
        semitones=semitones,
        preset=preset,
    )
    click.echo(f"Converted {len(results)} file(s).")


@main.command("demo")
@click.option(
    "--output-dir",
    "-o",
    default=Path("outputs") / "demo",
    show_default=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory for generated demo audio files.",
)
def demo(output_dir: Path) -> None:
    """Generate demo audio and example outputs for every preset."""
    results = create_demo_outputs(output_dir=output_dir)
    record_history(
        mode="demo",
        input_path=results[0],
        output_path=output_dir,
        semitones=0,
        preset="all",
    )
    click.echo("Generated demo files:")
    for result in results:
        click.echo(f"- {result}")


@main.command("history")
@click.option(
    "--limit",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of recent history entries to show.",
)
def history(limit: int) -> None:
    """Show recent conversion history."""
    entries = read_history(limit=limit)
    if not entries:
        click.echo("No history yet.")
        return

    for entry in entries:
        click.echo(
            f"{entry.created_at} | {entry.mode} | preset={entry.preset} | "
            f"semitones={entry.semitones:g} | {entry.output_path}"
        )


if __name__ == "__main__":
    main()
