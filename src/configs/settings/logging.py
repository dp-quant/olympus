"""
Logging settings using Loguru
"""

from .env import env


LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
LOGTAIL_ENABLED = env.bool("LOGTAIL_ENABLED", False)
LOGTAIL_TOKEN = env.str("LOGTAIL_TOKEN", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "logging.Formatter",
            "format": "%(message)s",
        },
    },
    "handlers": {
        "loguru": {
            "class": "olympus.utils.logger.InterceptHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["loguru"],
        "level": "INFO",
    },
}
