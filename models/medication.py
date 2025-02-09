import datetime
from pydantic import BaseModel

class Medication(BaseModel):
    medication_id: str
    user_id: str
    medication_name: str

class MedicationTargetTime(BaseModel):
    medication_id: str
    target_time: datetime.time



