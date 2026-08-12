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
4. Update or create release notes under `docs/`.
5. Commit the release prep changes.
6. Push to GitHub.
7. Confirm GitHub Actions passes.
8. Create a GitHub release with the matching tag.

Tag example:

```text
v0.1.0
```
