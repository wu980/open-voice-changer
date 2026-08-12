from __future__ import annotations

import logging
from pathlib import Path

DEFAULT_LOG_PATH = Path("outputs") / "logs" / "app.log"
LOGGER_NAME = "open_voice_changer"


def get_logger(log_path: str | Path = DEFAULT_LOG_PATH) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not _has_file_handler(logger, path):
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
        logger.addHandler(handler)

    return logger


def log_path() -> Path:
    return DEFAULT_LOG_PATH


def _has_file_handler(logger: logging.Logger, path: Path) -> bool:
    resolved = path.resolve()
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            if Path(handler.baseFilename).resolve() == resolved:
                return True
    return False
