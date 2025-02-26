import logging
import sys

import orjson
from django.conf import settings
from loguru import logger


logger.remove()


def json_formatter(record):
    """
    Custom JSON formatter for Loguru
    """
    log_record = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "name": record["name"],
        "function": record["function"],
        "line": record["line"],
        "path": record["file"].path,
    }

    # Add exception info if present
    if record["exception"]:
        log_record["exception"] = record["exception"]

    # Add extra context if present
    if record["extra"]:
        log_record["extra"] = record["extra"]

    return orjson.dumps(log_record)


# Add console handler with JSON formatting
logger.add(
    sys.stderr,
    format=json_formatter,
    level=settings.LOG_LEVEL,
    serialize=False,  # We're already serializing in our formatter
    backtrace=True,
    diagnose=True,
)
if settings.LOGTAIL_ENABLED and settings.LOGTAIL_TOKEN:
    try:
        from logtail.handler import LogtailHandler

        logtail_handler = LogtailHandler(source_token=settings.LOGTAIL_TOKEN)
        logger.add(
            logtail_handler,
            level=settings.LOG_LEVEL,
            format=json_formatter,
            serialize=False,
            backtrace=True,
            diagnose=True,
        )
    except ImportError:
        logger.warning("Logtail package not installed. Skipping Logtail integration.")


class InterceptHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.formatter = logging.Formatter("%(message)s")
        self.level = logging.NOTSET

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where this was logged
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# Configure Django logging to use our Loguru setup
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# Replace all existing handlers with our InterceptHandler
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True
