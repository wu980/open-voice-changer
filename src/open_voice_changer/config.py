from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from open_voice_changer.effects import validate_preset

DEFAULT_CONFIG_PATH = Path("outputs") / "config.json"


@dataclass(frozen=True)
class AppConfig:
    default_output_dir: str = "outputs"
    default_preset: str = "clean"
    default_semitones: float = 0.0
    last_input_dir: str = "."
    avoid_overwrite: bool = True


CONFIG_FIELDS = set(AppConfig.__dataclass_fields__)


def default_config() -> AppConfig:
    return AppConfig()


def load_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        return default_config()

    data = json.loads(path.read_text(encoding="utf-8"))
    merged = asdict(default_config())
    merged.update({key: value for key, value in data.items() if key in CONFIG_FIELDS})
    return _validate_config_data(merged)


def save_config(config: AppConfig, config_path: str | Path = DEFAULT_CONFIG_PATH) -> Path:
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(config), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def update_config(
    updates: dict[str, Any],
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> AppConfig:
    current = asdict(load_config(config_path))
    unknown = sorted(set(updates) - CONFIG_FIELDS)
    if unknown:
        raise ValueError(f"Unknown config field(s): {', '.join(unknown)}")

    current.update(updates)
    config = _validate_config_data(current)
    save_config(config, config_path)
    return config


def build_output_filename(input_path: str | Path, preset: str, semitones: float) -> str:
    source = Path(input_path)
    preset = validate_preset(preset)
    semitone_text = _format_semitones(semitones)
    return f"{source.stem}-{preset}-{semitone_text}.wav"


def build_default_output_path(
    input_path: str | Path,
    output_dir: str | Path,
    preset: str,
    semitones: float,
    avoid_overwrite: bool = True,
) -> Path:
    output = Path(output_dir) / build_output_filename(input_path, preset, semitones)
    if avoid_overwrite:
        return ensure_unique_path(output)
    return output


def ensure_unique_path(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.exists():
        return candidate

    index = 1
    while True:
        next_candidate = candidate.with_name(f"{candidate.stem}-{index}{candidate.suffix}")
        if not next_candidate.exists():
            return next_candidate
        index += 1


def _validate_config_data(data: dict[str, Any]) -> AppConfig:
    default_output_dir = str(data["default_output_dir"])
    default_preset = validate_preset(str(data["default_preset"]))
    default_semitones = float(data["default_semitones"])
    last_input_dir = str(data["last_input_dir"])
    avoid_overwrite = _parse_bool(data["avoid_overwrite"])

    return AppConfig(
        default_output_dir=default_output_dir,
        default_preset=default_preset,
        default_semitones=default_semitones,
        last_input_dir=last_input_dir,
        avoid_overwrite=avoid_overwrite,
    )


def _format_semitones(semitones: float) -> str:
    value = float(semitones)
    if value.is_integer():
        return f"{int(value):+d}"
    return f"{value:+.1f}".replace(".", "p")


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.lower().strip()
        if lowered in {"true", "1", "yes", "on"}:
            return True
        if lowered in {"false", "0", "no", "off"}:
            return False
    raise ValueError(f"Expected a boolean value, got: {value!r}")
