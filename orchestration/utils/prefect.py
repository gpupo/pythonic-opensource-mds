from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator


class Resource(BaseModel):
    root: Dict[str, Any]


class PrefectEvent(BaseModel):
    occurred: datetime
    event: str
    resource: Resource
    related: List[Any] = []
    payload: Dict[str, Any]
    id: UUID
    follows: Optional[UUID] = None
    received: datetime

    @field_validator("occurred", "received", mode="before")
    @classmethod
    def validate_datetime(cls, v):
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(v)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid datetime format: {v}")
