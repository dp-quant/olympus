"""Health check URLs."""

from django.urls import path

from .views import DBHealthCheckView
from .views import HealthCheckView
from .views import RabbitMQHealthCheckView


urlpatterns = [
    path("", HealthCheckView.as_view(), name="health_check"),
    path("db/", DBHealthCheckView.as_view(), name="db_health_check"),
    path("broker/", RabbitMQHealthCheckView.as_view(), name="broker_health_check"),
]
