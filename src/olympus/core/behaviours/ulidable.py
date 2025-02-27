"""ULIDable Model Mixin.

Behaviour for ULID primary key.
"""

from django.db import models

from olympus.core.db.fields import ULIDPrimaryKeyField


class ULIDable(models.Model):
    """Behaviour for ULID primary key."""

    id = ULIDPrimaryKeyField(primary_key=True)

    class Meta:
        """Meta class for the model."""

        abstract = True
