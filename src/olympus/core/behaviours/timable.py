"""Timable Model Mixin.

Behaviour for created_at and updated_at fields.
"""

from django.db import models


class Timable(models.Model):
    """Behaviour for created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for the model."""

        abstract = True
