from pathlib import Path

import click

from open_voice_changer.audio import convert_pitch


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
def shift(
    input_file: Path,
    output_file: Path,
    semitones: float,
    sample_rate: int | None,
) -> None:
    """Shift the pitch of INPUT_FILE and save OUTPUT_FILE."""
    result = convert_pitch(
        input_path=input_file,
        output_path=output_file,
        semitones=semitones,
        sample_rate=sample_rate,
    )
    click.echo(f"Saved converted audio: {result}")


if __name__ == "__main__":
    main()
