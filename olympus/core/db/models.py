"""Olympus Base Models."""

from django.db import models

from olympus.core.behaviours import Tenantable
from olympus.core.behaviours import Timable
from olympus.core.behaviours import ULIDable


class CRMBaseModel(ULIDable, Timable, Tenantable, models.Model):
    """Base model for all models."""

    class Meta:
        """Meta class for the model."""

        abstract = True
