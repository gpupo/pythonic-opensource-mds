from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class QueueMessage(BaseModel):
    msg_id: int
    message: Dict[str, Any]
    enqueued_at: datetime
    read_ct: int = 0
    vt: Optional[datetime] = None  # visibility timeout
    queue_name: Optional[str] = None

    model_config = {
        "frozen": True
    }  # Makes instances immutable - new style in Pydantic v2

    @field_validator("vt", "enqueued_at", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        """Convert string datetime to datetime object using a simplified approach"""
        if isinstance(value, str):
            try:
                # Try direct ISO parsing first (most common case)
                return datetime.fromisoformat(value)
            except ValueError:
                # Handle legacy format by normalizing to ISO format
                value = value.replace(" ", "T")

                # Fix timezone format if needed
                if "." in value and (value.rindex("-") > 10 or value.rindex("+") > 10):
                    # Extract parts before the timezone
                    main_part = (
                        value.rsplit("-", 1)[0]
                        if "-" in value[10:]
                        else value.rsplit("+", 1)[0]
                    )
                    # Extract the timezone part
                    tz_part = value[len(main_part) :]

                    # Ensure microseconds have proper precision and format
                    if "." in main_part:
                        dt_part, ms_part = main_part.split(".")
                        ms_part = ms_part[:6].ljust(6, "0")
                        main_part = f"{dt_part}.{ms_part}"

                    # Format timezone properly
                    if len(tz_part) == 2:  # Just hours
                        tz_part = f"{tz_part}:00"

                    return datetime.fromisoformat(f"{main_part}{tz_part}")

                return datetime.fromisoformat(value)
        return value
