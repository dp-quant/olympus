"""
ENV helper for the project.
"""

from enum import Enum

import environ


env = environ.Env()


class OlympusEnv(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
