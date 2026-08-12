# Contributing

Thanks for your interest in Open Voice Changer.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Checks

Run these before opening a pull request:

```powershell
python -m ruff check .
python -m pytest
```

## Project Scope

Good contributions:

- Offline audio conversion improvements
- Presets and local DSP effects
- UI usability improvements
- Tests and documentation
- Local model backend experiments that do not bundle unauthorized models

Out of scope:

- Uploading voice models that imitate real people without consent
- Adding copyrighted training data
- Promoting unauthorized impersonation

## Commit Style

Use short, clear commit messages:

```text
Add batch conversion reports
Fix config default loading
Improve desktop error message
```
