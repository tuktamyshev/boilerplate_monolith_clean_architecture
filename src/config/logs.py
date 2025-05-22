import logging
import logging.config
import os

from config import BASE_DIR

LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "console": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
        },
        "filters": {
            "webserver": {"()": "logging.Filter", "name": "webserver"},
            "post": {"()": "logging.Filter", "name": "post"},
            "scheduled_tasks": {"()": "logging.Filter", "name": "scheduled_tasks"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "webserver": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/webserver.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "DEBUG",
                "filters": ["webserver"],
            },
            "post": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/post.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "DEBUG",
                "filters": ["post"],
            },
            "scheduled_tasks": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{LOG_DIR}/scheduled_tasks.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "default",
                "level": "DEBUG",
                "filters": ["scheduled_tasks"],
            },
        },
        "loggers": {
            "webserver": {
                "level": "DEBUG",
                "handlers": ["webserver", "console"],
            },
            "post": {
                "level": "DEBUG",
                "handlers": ["post", "console"],
            },
            "scheduled_tasks": {
                "level": "DEBUG",
                "handlers": ["scheduled_tasks", "console"],
            },
        },
    }

    logging.config.dictConfig(logging_config)
