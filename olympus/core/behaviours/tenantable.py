"""Tenantable Model Mixin.

Behaviour for tenant field.
"""

from django.db import models


class Tenantable(models.Model):
    """
    A mixin that adds a tenant field to a model.
    """

    tenant = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
