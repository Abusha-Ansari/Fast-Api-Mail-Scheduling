from pydantic import BaseModel
from typing import Dict


class SchedulePayload(BaseModel):
    time: str  # ISO format string
    url: str   # e.g., /send
    emailData: Dict[str, str]
