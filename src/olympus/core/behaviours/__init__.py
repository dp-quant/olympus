"""The list of the behaviour`s mixins for models."""

from .timable import Timable
from .ulidable import ULIDable
from .tenantable import Tenantable

__all__ = (
    "Timable",
    "ULIDable",
    "Tenantable",
)
