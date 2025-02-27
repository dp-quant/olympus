"""Celery configuration."""

import os

from celery import Celery
from environ import Env


env = Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

app = Celery(env.str("PROJECT_NAME", "celery"))
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
