# Open Voice Changer v0.1.0

Open Voice Changer v0.1.0 is the first public release of a local-first open source voice changer.

## Highlights

- Offline audio pitch shifting
- Simple desktop interface
- Batch folder conversion
- Voice presets: `clean`, `deep`, `bright`, `robot`, `radio`
- Demo workflow with `ovc demo`
- Conversion history with `ovc history`
- User defaults with `ovc config`
- Audio playback helper with `ovc play`
- Batch error reporting and CSV reports
- Application logs
- CI, linting, contribution docs, issue templates, and release docs

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
ovc demo
ovc-ui
```

## Safety Notes

This release does not include voice models, model training, or real-time microphone conversion.

Do not use this project to impersonate real people without consent. Users are responsible for following local laws, platform rules, and model licenses.

## Verification

Before release, run:

```powershell
python -m ruff check .
python -m pytest
```
