from pydantic import BaseModel
from typing import Dict, Any  # Use capitalized Any

class SchedulePayload(BaseModel):
    time: str
    url: str
    emailData: Dict[str, Any]

    model_config = {
        "arbitrary_types_allowed": True
    }
