"""
Base settings for the project.
"""

from pathlib import Path

from .env import OlympusEnv
from .env import env


BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_URLCONF = "configs.urls"

WSGI_APPLICATION = "configs.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

OLYMPUS_ENV = env.str("ENV", default=OlympusEnv.LOCAL.value)
