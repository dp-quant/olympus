"""
Celery settings for the project.
"""

from kombu import Exchange
from kombu import Queue

from .env import env


CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")

FLOWER_BROKER_API = env.str("FLOWER_BROKER_API")

CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
CELERY_TASK_DEFAULT_ROUTING_KEY = "default"

CELERY_TASK_ROUTES = {
    "default": {
        "queue": "default",
        "routing_key": "default",
    },
    r"(\w+)\.tasks\.emails": {
        "queue": "emails",
        "routing_key": "emails",
    },
    r"(\w+)\.tasks\.messages": {
        "queue": "messages",
        "routing_key": "messages",
    },
}
