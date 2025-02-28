"""Tests for healthcheck app."""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from olympus.core.logger import get_logger


logger = get_logger(__name__)


@pytest.fixture
def api_client() -> APIClient:
    """Return an API client for testing.

    Returns:
        APIClient: The API client to use for testing.
    """
    return APIClient()


@pytest.mark.parametrize(
    "view_name,expected_data",
    [
        ("health_check", {"is_service_online": True}),
    ],
)
def test_simple_health_check(api_client, view_name, expected_data):
    """Test the basic health check endpoint that doesn't require mocking.

    Args:
        api_client: The API client to use for testing.
        view_name: The name of the view to test.
        expected_data: The expected data to return from the view.
    """
    url = reverse(view_name)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.parametrize(
    "mock_return,expected_status,expected_data",
    [
        ((1,), status.HTTP_200_OK, {"is_db_online": True}),
        ((0,), status.HTTP_503_SERVICE_UNAVAILABLE, {"is_db_online": False}),
    ],
)
def test_db_health_check_results(api_client, mock_return, expected_status, expected_data):
    """Test DB health check with different query results.

    Args:
        api_client: The API client to use for testing.
        mock_return: The return value from the mock cursor.
        expected_status: The expected status code.
        expected_data: The expected data to return from the view.
    """
    with patch("olympus.healthcheck.views.connection") as mock_connection:
        # Setup mock cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_return
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        url = reverse("db_health_check")
        response = api_client.get(url)

        assert response.status_code == expected_status
        assert response.data == expected_data
        mock_cursor.execute.assert_called_once_with("SELECT 1")


def test_db_health_check_exception(api_client):
    """Test DB health check when an exception occurs.

    Args:
        api_client: The API client to use for testing.
    """
    with patch("olympus.healthcheck.views.connection") as mock_connection:
        mock_connection.cursor.side_effect = logger.error("DB connection error")

        url = reverse("db_health_check")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.data == {"is_db_online": False}


@pytest.mark.parametrize(
    "connection_success,expected_status,expected_data",
    [
        (True, status.HTTP_200_OK, {"is_broker_online": True}),
        (False, status.HTTP_503_SERVICE_UNAVAILABLE, {"is_broker_online": False}),
    ],
)
def test_broker_health_check(api_client, connection_success, expected_status, expected_data):
    """Test broker health check with success and failure scenarios.

    Args:
        api_client: The API client to use for testing.
        connection_success: Whether the connection is successful.
        expected_status: The expected status code.
        expected_data: The expected data to return from the view.
    """
    with patch("olympus.healthcheck.views.Connection") as mock_connection:
        if connection_success:
            mock_conn_instance = MagicMock()
            mock_connection.return_value.__enter__.return_value = mock_conn_instance
        else:
            mock_connection.return_value.__enter__.side_effect = logger.error("Broker connection error")

        url = reverse("broker_health_check")
        response = api_client.get(url)

        assert response.status_code == expected_status
        assert response.data == expected_data

        if connection_success:
            mock_conn_instance.connect.assert_called_once()
