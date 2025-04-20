import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlmodel import JSON, Column, Relationship, SQLModel, Session
from sqlmodel import Field as SuperField


def Field(*args, **kwargs) -> Any:
    description = kwargs.get("description")
    if not description:
        return SuperField(*args, **kwargs)

    if "sa_column" not in kwargs and "sa_column_kwargs" not in kwargs:
        kwargs["sa_column_kwargs"] = {"comment": description}

    field = SuperField(*args, **kwargs)
    if "sa_column" in kwargs:
        field.sa_column.comment = description

    return field

__all__ = ["Field", "SQLModel", "JSON", "Column", "Relationship","Session"]