from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EffectPreset:
    name: str
    label: str
    description: str


PRESETS = {
    "clean": EffectPreset("clean", "Clean", "No extra effect."),
    "deep": EffectPreset("deep", "Deep Voice", "Warmer and lower voice tone."),
    "bright": EffectPreset("bright", "Bright Voice", "Clearer and brighter tone."),
    "robot": EffectPreset("robot", "Robot Voice", "Synthetic modulated voice."),
    "radio": EffectPreset("radio", "Radio Voice", "Narrow-band radio style."),
}


def preset_names() -> list[str]:
    return list(PRESETS)


def validate_preset(name: str) -> str:
    preset = name.lower().strip()
    if preset not in PRESETS:
        choices = ", ".join(preset_names())
        raise ValueError(f"Unknown preset '{name}'. Choose one of: {choices}")
    return preset


def apply_preset(samples: np.ndarray, sample_rate: int, preset: str = "clean") -> np.ndarray:
    preset = validate_preset(preset)
    audio = np.asarray(samples, dtype=np.float32)

    if audio.size == 0:
        raise ValueError("Input audio is empty.")

    if preset == "clean":
        return _normalize(audio)
    if preset == "deep":
        return _normalize(_low_pass(audio, alpha=0.18) * 1.15)
    if preset == "bright":
        return _normalize(audio + 0.65 * _high_pass(audio, alpha=0.16))
    if preset == "robot":
        return _normalize(_robot_modulation(audio, sample_rate))
    if preset == "radio":
        filtered = _high_pass(_low_pass(audio, alpha=0.08), alpha=0.04)
        return _normalize(np.tanh(filtered * 2.4))

    raise ValueError(f"Unhandled preset: {preset}")


def _normalize(samples: np.ndarray, peak: float = 0.95) -> np.ndarray:
    max_value = float(np.max(np.abs(samples)))
    if max_value == 0:
        return samples.astype(np.float32)
    return (samples / max_value * peak).astype(np.float32)


def _low_pass(samples: np.ndarray, alpha: float) -> np.ndarray:
    output = np.empty_like(samples, dtype=np.float32)
    output[0] = samples[0]
    for index in range(1, samples.size):
        output[index] = output[index - 1] + alpha * (samples[index] - output[index - 1])
    return output


def _high_pass(samples: np.ndarray, alpha: float) -> np.ndarray:
    low = _low_pass(samples, alpha=alpha)
    return (samples - low).astype(np.float32)


def _robot_modulation(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    time = np.arange(samples.size, dtype=np.float32) / float(sample_rate)
    carrier = np.sign(np.sin(2 * np.pi * 35 * time)).astype(np.float32)
    return samples * carrier
