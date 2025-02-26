"""
Emails settings for the project.
"""

from .env import env


MAINTAINER_EMAIL = env.str("MAINTAINER_EMAIL")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")

SENDGRID_API_KEY = env.str("SENDGRID_API_KEY")
