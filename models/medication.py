from pydantic import BaseModel
from typing import Optional

class Medication(BaseModel):
    medication_id: str
    user_id: str
    medication_name: str
    date_added: Optional[str] = None
    time_to_take: list[str]


