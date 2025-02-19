from pydantic import BaseModel

class Medication(BaseModel):
    medication_id: str
    user_id: str
    medication_name: str
    time_to_take: list[str]


