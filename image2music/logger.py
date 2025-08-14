import logging
import os
from typing import Optional

# ====== COLORS ======
COLORS = {
    'DEBUG': '\033[36m',       # Cyan
    'INFO': '\033[32m',        # Green
    'WARNING': '\033[33m',     # Yellow
    'ERROR': '\033[31m',       # Red
    'CRITICAL': '\033[1;31m',  # Bold Red
}
RESET = "\033[0m"

class ShortColorFormatter(logging.Formatter):
    """Custom logging formatter with color-coded level names."""
    def format(self, record):
        color = COLORS.get(record.levelname, '')
        msg = super().format(record)
        return f"{color}{msg}{RESET}"

def get_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.DEBUG
) -> logging.Logger:
    """
    Create a logger with both console and optional file output.

    Args:
        name (str): Logger name.
        log_file (str, optional): Path to file for log output.
        level (int): Logging level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if logger already exists
    if logger.hasHandlers():
        return logger

    # Console handler with colors
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(ShortColorFormatter("[%(levelname)s] %(message)s"))
    logger.addHandler(ch)

    # File handler without colors
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
        logger.addHandler(fh)

    return logger

