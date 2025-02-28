from typing import Any
from typing import Optional
from typing import Sequence
from typing import cast

from django.db import models
from ulid import ULID


class ULIDField(models.CharField[Any, Any]):
    """
    A field that stores ULIDs (Universally Unique Lexicographically Sortable Identifiers).

    ULIDs are 128-bit identifiers that combine a timestamp with random data,
    providing a unique, sortable identifier that's more compact than UUIDs.
    """

    description = "Universally Unique Lexicographically Sortable Identifier"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 26)
        kwargs.setdefault("editable", False)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: Any) -> Optional[str]:
        """Convert the value to a string before saving to the database.

        Args:
            value: The value to convert.

        Returns:
            The value to save to the database.
        """
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return str(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Optional[ULID]:  # noqa
        """Convert the database value to a ULID object.

        Args:
            value: The value to convert.
            expression: The expression.
            connection: The connection.

        Returns:
            The ULID object.
        """
        if value is None:
            return None
        return cast(ULID, ULID.from_str(value))

    def to_python(self, value: Any) -> Optional[ULID]:
        """Convert the value to a ULID object.

        Args:
            value: The value to convert.

        Returns:
            The ULID object.
        """
        if value is None or isinstance(value, ULID):
            return value
        return cast(ULID, ULID.from_str(str(value)))

    def get_internal_type(self) -> str:
        """Return the internal type of the field.

        Returns:
            The internal type of the field.
        """
        return "CharField"

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        """Return a 4-tuple with enough information to recreate the field.

        Returns:
            A 4-tuple with enough information to recreate the field.
        """
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 26:
            del kwargs["max_length"]
        if kwargs.get("editable") is False:
            del kwargs["editable"]
        return name, path, args, kwargs


class ULIDPrimaryKeyField(ULIDField):
    """
    A primary key field that uses ULIDs.

    This field automatically generates a ULID when a new object is created.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the field.

        Args:
            *args: The arguments.
            **kwargs: The keyword arguments.
        """
        kwargs.setdefault("primary_key", True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: models.Model, add: bool) -> ULID:
        """Generate a new ULID if this is a new object.

        Args:
            model_instance: The model instance.
            add: Whether the object is being added.

        Returns:
            The ULID.
        """
        value = getattr(model_instance, self.attname)
        if value is None or add:
            value = ULID()
            setattr(model_instance, self.attname, value)
        return cast(ULID, value)

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        """Return a 4-tuple with enough information to recreate the field.

        Returns:
            A 4-tuple with enough information to recreate the field.
        """
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("primary_key") is True:
            del kwargs["primary_key"]
        return name, path, args, kwargs
