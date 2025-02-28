"""Gunicorn configuration file."""

import logging
import sys
import typing
from multiprocessing import cpu_count

import environ
import json_log_formatter


env: environ.Env = environ.Env()

bind: str = "unix:/srv/run/application/gunicorn.sock"
backlog: int = 2048

workers: int = env.int("GUNICORN_WORKERS", cpu_count() * 2 - 1)
worker_class: str = "sync"
timeout: int = env.int("GUNICORN_TIMEOUT", 300)
max_requests: int = env.int("GUNICORN_MAX_REQUESTS", 1500)
graceful_timeout: int = env.int("GUNICORN_GRACEFUL_TIMEOUT", 30)


daemon: bool = False

pidfile: str = "/srv/run/application/gunicorn.pid"

umask: int = 0
user: str = env.str("DOCKER_USER")
group: str = env.str("DOCKER_GROUP")
tmp_upload_dir: typing.Any = None

reload: bool = env.bool("GUNICORN_RELOAD", default=False)
reload_engine: str = "poll"


accesslog: str = "-"
errorlog: str = "-"


class JsonRequestFormatter(json_log_formatter.JSONFormatter):
    """Custom JSON log formatter for Gunicorn."""

    def json_record(
        self,
        message: str,
        extra: dict[str, str | int | float],
        record: logging.LogRecord,
    ) -> dict[str, str | int | float]:
        """Return a JSON log record.

        Args:
            message (str): The message to log.
            extra (dict[str, str | int | float]): The extra data to log.
            record (logging.LogRecord): The log record.

        Returns:
            dict[str, str | int | float]: The JSON log record.
        """
        payload: dict[str, str | int | float] = super().json_record(message, extra, record)
        payload["service"] = env.str("SERVICE_NAME", "---")
        payload["source"] = "gunicorn"
        payload["level"] = record.levelname

        payload.pop("color_message", None)

        return payload


# Ensure the two named loggers that Gunicorn uses are configured to use a custom
# JSON formatter.
logconfig_dict = {
    "version": 1,
    "formatters": {
        "json": {
            "()": JsonRequestFormatter,
        }
    },
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json",
        }
    },
    "root": {"level": "INFO", "handlers": []},
    "loggers": {
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["json"],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["json"],
            "propagate": False,
        },
    },
}
