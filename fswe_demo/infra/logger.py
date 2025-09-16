# myapp/logging_setup.py
from loguru import logger
from rich.logging import RichHandler


def setup_logger() -> None:
    logger.remove()
    logger.add(
        RichHandler(rich_tracebacks=True, markup=True),
        format="[{time:YYYY-MM-DD HH:mm:ss}] {level} {message}",
    )
    return logger
