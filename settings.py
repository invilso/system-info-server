from pathlib import Path
from typing import Literal

BASE_DIR = Path(__file__).resolve().parent

LOGS_DIR = Path.joinpath(BASE_DIR, "logs")

GLOBAL_LOGS_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"

DEFAULT_HOST = '127.0.0.1:12345'

TESTS_DIR = Path.joinpath(BASE_DIR, "tests")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file_info": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": Path.joinpath(LOGS_DIR, "info.log"),
            "mode": "a",
        },
        "file_error": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": Path.joinpath(LOGS_DIR, "error.log"),
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file_info", "file_error"],
            "level": GLOBAL_LOGS_LEVEL,
            "propagate": True,
        }
    },
}
