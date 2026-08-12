# open-voice-changer
Local-first open source voice changer for audio files and future real-time voice conversion.
# Open Voice Changer

Open Voice Changer is a local-first open source voice changer.

The first version focuses on offline audio file conversion. Future versions may support a desktop interface, batch conversion, real-time microphone conversion, and optional model backends.

## Current Features

- Load a local audio file
- Shift pitch up or down
- Export a converted audio file
- Run from the command line

## Install for Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Usage

```powershell
ovc shift input.wav outputs\voice-high.wav --semitones 4
ovc shift input.wav outputs\voice-low.wav --semitones -3
```

`--semitones` controls pitch. Positive values sound higher, negative values sound lower.

## Project Goals

- Run locally by default
- Keep the first version simple and understandable
- Avoid bundling unauthorized voice models
- Grow toward real-time voice changing over time

## Safety and Consent

Do not use this project to impersonate real people without consent. Users are responsible for following local laws, platform rules, and model licenses.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md).
