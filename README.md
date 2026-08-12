# Open Voice Changer

Open Voice Changer is a local-first open source voice changer.

The first version focuses on offline audio file conversion. Future versions may support a desktop interface, batch conversion, real-time microphone conversion, and optional model backends.

## Current Features

- Load a local audio file
- Shift pitch up or down
- Export a converted audio file
- Run from the command line
- Run from a simple desktop interface

## Install for Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Usage

Quick demo:

```powershell
ovc demo
```

This creates a synthetic demo input and preset examples in `outputs\demo`.

Recent conversions are saved to `outputs\history.jsonl`.

Desktop interface:

```powershell
ovc-ui
```

In the desktop interface, turn on `Batch folder mode` to convert every supported audio file in a folder.

The desktop interface also shows conversion progress and can open the output folder after conversion.

Available presets:

- `clean`
- `deep`
- `bright`
- `robot`
- `radio`

Command line:

```powershell
ovc shift input.wav outputs\voice-high.wav --semitones 4 --preset bright
ovc shift input.wav outputs\voice-low.wav --semitones -3 --preset deep
ovc batch samples outputs --semitones 4 --preset radio
ovc history
```

`--semitones` controls pitch. Positive values sound higher, negative values sound lower.

Supported batch input formats:

- `.wav`
- `.mp3`
- `.flac`
- `.ogg`
- `.m4a`

Generated audio files in `outputs\` are ignored by Git.

## Project Goals

- Run locally by default
- Keep the first version simple and understandable
- Avoid bundling unauthorized voice models
- Grow toward real-time voice changing over time

## Safety and Consent

Do not use this project to impersonate real people without consent. Users are responsible for following local laws, platform rules, and model licenses.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md).
