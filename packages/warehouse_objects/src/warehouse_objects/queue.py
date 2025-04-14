from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class QueueMessage(BaseModel):
    msg_id: int
    message: Dict[str, Any]
    enqueued_at: datetime
    read_ct: int = 0
    vt: Optional[datetime] = None  # visibility timeout
    queue_name: Optional[str] = None
    class Config:
        frozen = True  # Makes instances immutable
