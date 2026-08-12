from pathlib import Path

from open_voice_changer.logging_utils import get_logger


def test_get_logger_writes_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    logger = get_logger(log_file)

    logger.info("hello logs")

    assert log_file.exists()
    assert "hello logs" in log_file.read_text(encoding="utf-8")


def test_get_logger_does_not_duplicate_file_handlers(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    logger = get_logger(log_file)
    before = len(logger.handlers)

    get_logger(log_file)

    assert len(logger.handlers) == before
