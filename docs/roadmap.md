# Roadmap

## v0.1 - Offline Audio MVP

- Load a local audio file
- Shift pitch up or down
- Export a converted audio file
- Provide a command line interface

## v0.2 - Simple Desktop UI

- Select input and output files
- Adjust pitch with a slider
- Show conversion status

## v0.3 - Batch Conversion

- Convert multiple files in a folder
- Save outputs to a chosen directory
- Show conversion progress in the desktop interface

## v0.4 - Optional Model Backends

- Let users configure their own local model files
- Do not bundle unauthorized voice models

## v0.5 - Effect Presets

- Add clean, deep, bright, robot, and radio presets
- Support presets in the command line interface
- Support presets in the desktop interface

## v0.6 - Demo Workflow

- Generate a synthetic demo audio file
- Export demo outputs for every preset
- Document a quick demo command for new users

## v0.7 - Conversion History

- Record recent conversions in `outputs/history.jsonl`
- Add `ovc history`
- Ignore generated outputs in Git

## v0.8 - User Defaults

- Save default output directory, preset, and semitones
- Add `ovc config show`, `set`, `path`, and `reset`
- Let `ovc shift` auto-generate output paths
- Load and save defaults from the desktop interface

## v0.9 - Batch Error Reports

- Continue batch conversion when one file fails
- Report success and failure counts
- Show failed files in the desktop interface

## v0.10 - Audio Playback

- Add `ovc play`
- Add desktop `Play Input`
- Add desktop `Play Output`

## v0.11 - Batch Reports

- Write `report.csv` after batch conversion
- Include success/failure status for every file
- Include output path, error, preset, and semitones

## v0.12 - Logging

- Write application logs to `outputs/logs/app.log`
- Log conversion results and errors
- Add `ovc config log-path`

## v0.13 - Project Quality

- Add Ruff lint configuration
- Add GitHub Actions CI
- Add contributing guide
- Clean development installation docs

## v0.14 - Release Preparation

- Add changelog
- Add release checklist
- Add pull request template
- Add GitHub issue templates

## v1.0 - Stable Local Tool

- Improve docs
- Add tests for common workflows
- Package releases for non-developer users
