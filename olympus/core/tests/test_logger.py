"""Tests for the application logger."""

import json
import logging
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from loguru import logger as loguru_logger

from olympus.core.logger import InterceptHandler
from olympus.core.logger import serialize
from olympus.core.logger import sink


@pytest.fixture
def sample_record():
    """Create a sample loguru record for testing."""
    return {
        "time": MagicMock(timestamp=lambda: 1609459200.0, isoformat=lambda: "2021-01-01T00:00:00"),
        "level": MagicMock(name="INFO"),
        "message": "Test message",
        "name": "test_logger",
        "function": "test_function",
        "line": 42,
        "file": MagicMock(path="/path/to/file.py"),
        "exception": None,
        "extra": {"user_id": 123},
    }


@pytest.fixture
def sample_record_with_exception():
    """Create a sample loguru record with exception for testing."""
    record = {
        "time": MagicMock(timestamp=lambda: 1609459200.0, isoformat=lambda: "2021-01-01T00:00:00"),
        "level": MagicMock(name="ERROR"),
        "message": "Test error message",
        "name": "test_logger",
        "function": "test_function",
        "line": 42,
        "file": MagicMock(path="/path/to/file.py"),
        "exception": {"type": "ValueError", "value": "Test error", "traceback": "..."},
        "extra": {},
    }
    return record


def test_serialize(sample_record):
    """Test the serialize function."""
    serialized = serialize(sample_record)
    data = json.loads(serialized)

    assert data["timestamp"] == 1609459200.0
    assert data["time"] == "2021-01-01T00:00:00"
    assert data["level"] == "INFO"
    assert data["message"] == "Test message"
    assert data["name"] == "test_logger"
    assert data["function"] == "test_function"
    assert data["line"] == 42
    assert data["path"] == "/path/to/file.py"
    assert "extra" in data
    assert data["extra"]["user_id"] == 123


def test_serialize_with_exception(sample_record_with_exception):
    """Test the serialize function with exception data."""
    serialized = serialize(sample_record_with_exception)
    data = json.loads(serialized)

    assert data["level"] == "ERROR"
    assert "exception" in data
    assert data["exception"]["type"] == "ValueError"
    assert data["exception"]["value"] == "Test error"


@patch("sys.stdout")
def test_sink(mock_stdout, sample_record):
    """Test the sink function."""
    message = MagicMock()
    message.record = sample_record

    sink(message)

    # Verify that serialize was called and the result was printed to stdout
    expected_output = serialize(sample_record)
    mock_stdout.write.assert_called_once_with(expected_output + "\n")


def test_intercept_handler():
    """Test the InterceptHandler."""
    handler = InterceptHandler()

    # Test basic properties
    assert isinstance(handler, logging.Handler)

    # Test emit method with a standard logging record
    with patch.object(loguru_logger, "opt", return_value=loguru_logger) as mock_opt:
        with patch.object(loguru_logger, "log") as mock_log:
            record = logging.LogRecord(
                name="test_logger",
                level=logging.INFO,
                pathname="/path/to/file.py",
                lineno=42,
                msg="Test message",
                args=(),
                exc_info=None,
            )

            handler.emit(record)

            # Verify that logger.opt was called with the right parameters
            mock_opt.assert_called_once()
            assert "depth" in mock_opt.call_args[1]
            assert "exception" in mock_opt.call_args[1]
            assert mock_opt.call_args[1]["exception"] is None

            # Verify that log was called with the right level and message
            mock_log.assert_called_once_with("INFO", "Test message")


@pytest.mark.django_db
def test_django_logging_integration():
    """Test that Django logging is properly integrated with Loguru."""
    # Get the Django logger
    django_logger = logging.getLogger("django")

    # Check that it has no handlers (they should be removed in our logger setup)
    assert len(django_logger.handlers) == 0

    # Check that propagate is True
    assert django_logger.propagate is True

    # Test that logging through Django logger goes to Loguru
    with patch.object(loguru_logger, "opt", return_value=loguru_logger) as mock_opt:
        with patch.object(loguru_logger, "log") as mock_log:
            django_logger.info("Test Django log message")

            # Verify that logger.log was called
            mock_log.assert_called()


@pytest.mark.django_db
def test_logtail_integration(settings):
    """Test Logtail integration."""
    # Test with Logtail enabled
    with patch("olympus.core.logger.LogtailHandler") as mock_handler:
        with patch.object(loguru_logger, "add") as mock_add:
            # Enable Logtail
            settings.LOGTAIL_ENABLED = True
            settings.LOGTAIL_TOKEN = "test_token"

            # Re-import to trigger the Logtail setup
            from importlib import reload

            from olympus.core import logger

            reload(logger)

            # Verify that LogtailHandler was created with the right token
            mock_handler.assert_called_once_with(source_token="test_token")

            # Verify that logger.add was called for the Logtail handler
            assert mock_add.call_count >= 1


@pytest.mark.django_db
def test_logtail_import_error(settings):
    """Test handling of Logtail import error."""
    # Test with Logtail enabled but import error
    with patch("olympus.core.logger.LogtailHandler", side_effect=ImportError):
        with patch.object(loguru_logger, "warning") as mock_warning:
            # Enable Logtail
            settings.LOGTAIL_ENABLED = True
            settings.LOGTAIL_TOKEN = "test_token"

            # Re-import to trigger the Logtail setup
            from importlib import reload

            from olympus.core import logger

            reload(logger)

            # Verify that a warning was logged
            mock_warning.assert_called_once_with("Logtail package not installed. Skipping Logtail integration.")
