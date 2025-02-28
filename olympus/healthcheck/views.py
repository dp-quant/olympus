from typing import Any

from django.conf import settings
from django.db import connection
from kombu import Connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from olympus.core.logger import get_logger


logger = get_logger(__name__)


class HealthCheckView(APIView):
    """
    Health check endpoint to verify if the application is running.
    """

    permission_classes = [AllowAny]

    def get(self, *args: Any, **kwargs: Any) -> Response:  # noqa
        """
        Health check endpoint to verify if the application is running.

        Args:
            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A JSON response with a status of "ok" if the application is running.
        """
        return Response({"is_service_online": True}, status=status.HTTP_200_OK)


class DBHealthCheckView(APIView):
    """
    Health check endpoint to verify if the database connection is alive.
    """

    permission_classes = [AllowAny]

    def get(self, *args: Any, **kwargs: Any) -> Response:  # noqa
        """
        Health check endpoint to verify if the database connection is alive.

        Args:
            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A JSON response with a status of "ok" if the database connection is alive.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    return Response({"is_db_online": True}, status=status.HTTP_200_OK)
                else:
                    return Response({"is_db_online": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return Response({"is_db_online": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RabbitMQHealthCheckView(APIView):
    """
    Health check endpoint to verify if RabbitMQ connection is alive.
    """

    permission_classes = [AllowAny]

    def get(self, *args: Any, **kwargs: Any) -> Response:  # noqa
        """
        Health check endpoint to verify if RabbitMQ connection is alive.

        Args:
            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A JSON response with a status of "ok" if the RabbitMQ connection is alive.
        """
        try:
            with Connection(settings.CELERY_BROKER_URL) as connection:
                connection.connect()
                return Response({"is_broker_online": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"RabbitMQ health check failed: {str(e)}")
            return Response({"is_broker_online": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
