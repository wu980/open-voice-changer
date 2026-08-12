# Release Checklist

Use this checklist before publishing a GitHub release.

## Local Checks

```powershell
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
ovc demo
ovc history
```

## Files To Review

- `README.md`
- `CHANGELOG.md`
- `docs/roadmap.md`
- `docs/model-policy.md`
- `pyproject.toml`

## Release Steps

1. Update the version in `pyproject.toml`.
2. Update the version in `src/open_voice_changer/__init__.py`.
3. Move the changelog section from `Unreleased` to the release date.
4. Commit the release prep changes.
5. Push to GitHub.
6. Confirm GitHub Actions passes.
7. Create a GitHub release with the matching tag.

Tag example:

```text
v0.1.0
```
