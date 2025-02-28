"""Django settings for the Olympus project."""

from pathlib import Path

from .env import OlympusEnv
from .env import env


# ------------------------------------------------------------------------------
# Base
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "olympus"

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]


USE_TZ = True

STATIC_URL = "static/"

ENV = env.str("ENV", default=OlympusEnv.LOCAL.value)

SITE_ID = 1

ADMIN_URL = "__backoffice/"
REDIRECT_URL = "/"


# ------------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
]

OLYMPUS_APPS: list[str] = [
    "olympus.core.apps.CoreConfig",
    "olympus.healthcheck.apps.HealthCheckConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OLYMPUS_APPS

# ------------------------------------------------------------------------------
# Celery
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT"),
    }
}

# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------
SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS: list[str] = []

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

if ENV != OlympusEnv.LOCAL.value:
    # Server Ready
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# ------------------------------------------------------------------------------
# Emails and Communication
# ------------------------------------------------------------------------------
MAINTAINER_EMAIL = env.str("MAINTAINER_EMAIL")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")

SENDGRID_API_KEY = env.str("SENDGRID_API_KEY")


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
LOGTAIL_ENABLED = env.bool("LOGTAIL_ENABLED", False)
LOGTAIL_TOKEN = env.str("LOGTAIL_TOKEN", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "logging.Formatter",
            "format": "%(message)s",
        }
    },
    "handlers": {
        "loguru": {
            "class": "olympus.core.logger.InterceptHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["loguru"],
        "level": "INFO",
    },
}


# ------------------------------------------------------------------------------
# Middlewares
# ------------------------------------------------------------------------------
DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

OLYMPUS_MIDDLEWARE: list[str] = []

MIDDLEWARE = DJANGO_MIDDLEWARE + OLYMPUS_MIDDLEWARE


# ------------------------------------------------------------------------------
# Twilio
# ------------------------------------------------------------------------------
TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN")
TWILIO_MESSAGING_SERVICE_SID = env.str("TWILIO_MESSAGING_SERVICE_SID")


# Phone numbers for different countries - EXAMPLES for now
TWILIO_PHONE_NUMBERS = {
    "ua": "+38099245702",
    "us": "+18163061121",
}

DEFAULT_TWILIO_PHONE_NUMBER = TWILIO_PHONE_NUMBERS["us"]


# ------------------------------------------------------------------------------
# Versioning
# ------------------------------------------------------------------------------
VERSION = "0.0.1"


# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]


# ------------------------------------------------------------------------------
# Forms
# ------------------------------------------------------------------------------
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"

# STATICFILES_DIRS = [str(BASE_DIR / "static")]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------------
# REST Framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ------------------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------------------
CORS_URLS_REGEX = r"^/api/.*$"

# ------------------------------------------------------------------------------
# Spectacular
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Olympus API",
    "DESCRIPTION": "Documentation of API endpoints of Olympus",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
}

# ------------------------------------------------------------------------------
# Sentry
# ------------------------------------------------------------------------------
if ENV != OlympusEnv.LOCAL.value:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            LoggingIntegration(
                level=LOG_LEVEL,
                event_level=LOG_LEVEL,
            ),
        ],
        environment=ENV,
        enable_tracing=True,
        send_default_pii=True,
        traces_sample_rate=1.0,
    )
