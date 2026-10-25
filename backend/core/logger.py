"""
MabrAIn — Logging Setup (loguru)
Import `logger` from here instead of using print() or stdlib logging.
"""

import sys
from pathlib import Path
from loguru import logger

from core.config import settings

# Remove default handler
logger.remove()

# Pretty console output
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> — <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

# Rotating file log
log_path = Path(settings.log_dir)
log_path.mkdir(parents=True, exist_ok=True)

logger.add(
    log_path / "mabrain_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="14 days",
    level="INFO",
    encoding="utf-8",
)

__all__ = ["logger"]
