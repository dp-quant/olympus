"""
Sentry settings
"""

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .env import env


sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    integrations=[DjangoIntegration(), CeleryIntegration(), LoggingIntegration()],
    send_default_pii=True,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)
