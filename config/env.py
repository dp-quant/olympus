"""ENV helper for the project settings."""

from enum import Enum

import environ


env = environ.Env()


class OlympusEnv(Enum):
    """Olympus Environment."""

    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
