"""Application Logger."""

import logging
import sys

import loguru
import orjson
from django.conf import settings


logger = loguru.logger
logger.remove()


def serialize(record: "loguru.Record") -> str:
    """Serialize Rules for the record.

    Args:
        record: Loguru record.

    Returns:
        Serialized record.
    """
    log_record = {
        "timestamp": record["time"].timestamp(),
        "time": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "name": record["name"],
        "function": record["function"],
        "line": record["line"],
        "path": record["file"].path,
    }

    # Add exception info if present
    if record["exception"]:
        log_record["exception"] = f"{record['exception'].type}: {record['exception'].value}"

    # Add extra context if present
    if record["extra"]:
        log_record["extra"] = record["extra"]

    return orjson.dumps(log_record).decode("utf-8")


def sink(message: "loguru.Message") -> None:
    """Custom JSON formatter for Loguru.

    Args:
        message: Loguru message.
    """
    print(serialize(message.record), file=sys.stdout)


# Add console handler with JSON formatting
logger.add(
    sink,
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
            level=settings.LOG_LEVEL.upper(),
            format="{message}",
            serialize=False,
            backtrace=True,
            diagnose=True,
        )
    except ImportError:
        logger.warning("Logtail package not installed. Skipping Logtail integration.")


def get_logger(name: str) -> "loguru.Logger":
    """Get a logger.

    Args:
        name: The name of the logger.

    Returns:
        The logger.
    """
    return logger.bind(name=name)


class InterceptHandler(logging.Handler):
    """InterceptHandler for Django logging."""

    def __init__(self):
        """Initialize the InterceptHandler."""
        super().__init__()
        self.logger = get_logger(__name__)
        self.formatter = None
        self.level = settings.LOG_LEVEL.upper()

    def emit(self, record):
        """Emit the record.

        Args:
            record: Record.
        """
        try:
            level = self.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            # frame = frame.f_back  # noqa
            depth += 1

        self.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True
