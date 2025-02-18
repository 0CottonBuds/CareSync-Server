from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from helpers.error import handle_error
from database.medication import MedicationDatabase

class AddMedicationRequest(BaseModel):
    user_id: str
    medication_name: str
    time_to_take: List[str]

class EditMedicationRequest(BaseModel):
    user_id: str
    medication_id: str
    medication_name: str
    time_to_take: str
 
router = APIRouter(prefix="/users/medication", tags=["Medication"])

@router.post("/add-medication")
async def add_medication(medication: AddMedicationRequest):
    response = MedicationDatabase.add_user_medication(medication.user_id, medication.medication_name, medication.time_to_take)
    handle_error(response)

    return {"message": "Successfully added new medication", 'medication_id': response[1]}

@router.post("/edit-medication")
async def edit_medication(medication: EditMedicationRequest):
    response = MedicationDatabase.edit_user_medication()


    pass

@router.post("/remove-medicationn")
async def api_remove_medication():
    pass

@router.get("/get-medication/{user_id}")
async def api_get_user_medication(user_id: str):
    response = MedicationDatabase.get_user_medication(user_id)
    handle_error(response)

    return {"message": "User Medication Found", "medication": response[1]}


