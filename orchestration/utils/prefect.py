import ast
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


def parse_event_data(**kwargs):
    occurred = kwargs.get("occurred")
    event = kwargs.get("event")
    payload = kwargs.get("payload")
    id_val = kwargs.get("id")
    deployment_parameters = kwargs.get("deployment")

    if isinstance(payload, str):
        payload = ast.literal_eval(payload)
    return PrefectEvent(
        deployment=deployment_parameters,
        occurred=occurred,
        event=event,
        payload=payload,
        id=id_val,
    )


class PrefectEvent(BaseModel):
    occurred: datetime
    event: str
    resource: Optional[Any] = None
    related: List[Any] = []
    payload: Dict[str, Any]
    id: UUID
    follows: Optional[UUID] = None
    received: Optional[datetime] = None
    deployment: Optional[Any] = None

    @computed_field
    def message(self) -> dict:
        return self.payload["message"]
