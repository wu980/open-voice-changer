from pathlib import Path
from dataclasses import asdict

import click

from open_voice_changer.audio import convert_pitch
from open_voice_changer.batch import convert_directory
from open_voice_changer.config import (
    DEFAULT_CONFIG_PATH,
    build_default_output_path,
    default_config,
    load_config,
    save_config,
    update_config,
)
from open_voice_changer.demo import create_demo_outputs
from open_voice_changer.effects import preset_names
from open_voice_changer.history import read_history, record_history
from open_voice_changer.player import open_audio
from open_voice_changer.reports import write_batch_report


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
    required=False,
    type=click.Path(dir_okay=False, path_type=Path),
)
@click.option(
    "--semitones",
    "-s",
    default=None,
    type=float,
    help="Pitch shift amount. Uses config default when omitted.",
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
    default=None,
    type=click.Choice(preset_names(), case_sensitive=False),
    help="Voice effect preset. Uses config default when omitted.",
)
def shift(
    input_file: Path,
    output_file: Path | None,
    semitones: float | None,
    sample_rate: int | None,
    preset: str | None,
) -> None:
    """Shift the pitch of INPUT_FILE and save OUTPUT_FILE."""
    config = load_config()
    actual_semitones = config.default_semitones if semitones is None else semitones
    actual_preset = config.default_preset if preset is None else preset
    actual_output_file = output_file or build_default_output_path(
        input_path=input_file,
        output_dir=config.default_output_dir,
        preset=actual_preset,
        semitones=actual_semitones,
        avoid_overwrite=config.avoid_overwrite,
    )

    result = convert_pitch(
        input_path=input_file,
        output_path=actual_output_file,
        semitones=actual_semitones,
        sample_rate=sample_rate,
        preset=actual_preset,
    )
    record_history(
        mode="single",
        input_path=input_file,
        output_path=result,
        semitones=actual_semitones,
        preset=actual_preset,
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
    default=None,
    type=float,
    help="Pitch shift amount for every audio file. Uses config default when omitted.",
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
    default=None,
    type=click.Choice(preset_names(), case_sensitive=False),
    help="Voice effect preset for every audio file. Uses config default when omitted.",
)
def batch(
    input_dir: Path,
    output_dir: Path,
    semitones: float | None,
    sample_rate: int | None,
    preset: str | None,
) -> None:
    """Convert all supported audio files in INPUT_DIR."""
    config = load_config()
    actual_semitones = config.default_semitones if semitones is None else semitones
    actual_preset = config.default_preset if preset is None else preset

    def show_progress(index: int, total: int, result) -> None:
        if result.succeeded:
            click.echo(f"[{index}/{total}] Saved: {result.output_path}")
        else:
            click.echo(f"[{index}/{total}] Failed: {result.input_path} ({result.error})")

    result = convert_directory(
        input_dir=input_dir,
        output_dir=output_dir,
        semitones=actual_semitones,
        sample_rate=sample_rate,
        preset=actual_preset,
        avoid_overwrite=config.avoid_overwrite,
        on_progress=show_progress,
    )
    record_history(
        mode="batch",
        input_path=input_dir,
        output_path=output_dir,
        semitones=actual_semitones,
        preset=actual_preset,
    )
    click.echo(
        f"Batch finished: {result.success_count} succeeded, "
        f"{result.failure_count} failed, {result.total_count} total."
    )
    report_path = write_batch_report(
        result=result,
        output_dir=output_dir,
        preset=actual_preset,
        semitones=actual_semitones,
    )
    click.echo(f"Report saved: {report_path}")


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


@main.command("play")
@click.argument(
    "audio_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def play(audio_file: Path) -> None:
    """Open an audio file in the system player."""
    result = open_audio(audio_file)
    click.echo(f"Opened audio: {result}")


@main.group("config")
def config() -> None:
    """Show and update user defaults."""


@config.command("show")
def config_show() -> None:
    """Show current user defaults."""
    current = load_config()
    for key, value in asdict(current).items():
        click.echo(f"{key}: {value}")


@config.command("path")
def config_path() -> None:
    """Show the config file path."""
    click.echo(DEFAULT_CONFIG_PATH)


@config.command("reset")
def config_reset() -> None:
    """Reset user defaults."""
    path = save_config(default_config())
    click.echo(f"Reset config: {path}")


@config.command("set")
@click.argument("field")
@click.argument("value")
def config_set(field: str, value: str) -> None:
    """Set one config field."""
    parsed_value: str | float | bool = value
    if field == "default_semitones":
        parsed_value = float(value)
    elif field == "avoid_overwrite":
        parsed_value = value

    current = update_config({field: parsed_value})
    click.echo(f"Updated {field}: {getattr(current, field)}")


if __name__ == "__main__":
    main()
