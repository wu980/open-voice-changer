from pathlib import Path
import os
import platform
import subprocess


def open_audio(path: str | Path) -> Path:
    audio_path = Path(path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file does not exist: {audio_path}")
    if audio_path.is_dir():
        raise IsADirectoryError(f"Expected an audio file, got directory: {audio_path}")

    system = platform.system()
    if system == "Windows":
        os.startfile(audio_path)
    elif system == "Darwin":
        subprocess.Popen(["open", str(audio_path)])
    else:
        subprocess.Popen(["xdg-open", str(audio_path)])

    return audio_path
