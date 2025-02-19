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
    time_to_take: List[str] 

class DeleteMedicationRequest(BaseModel):
    user_id: str
    medication_id: str
 
router = APIRouter(prefix="/users/medication", tags=["Medication"])

@router.post("/add-medication")
async def add_medication(medication: AddMedicationRequest):
    response = MedicationDatabase.add_user_medication(medication.user_id, medication.medication_name, medication.time_to_take)
    handle_error(response)

    return {"message": "Successfully added new medication", 'medication_id': response[1]}

@router.post("/edit-medication")
async def edit_medication(edit_request: EditMedicationRequest):
    response = MedicationDatabase.edit_user_medication(edit_request.user_id, edit_request.medication_id, edit_request.medication_name, edit_request.time_to_take)
    handle_error(response)

    return {"message": "Successfully edited medicatoin!", "medication_id": response[1]}

@router.post("/delete-medicationn")
async def api_delete_medication(delete_request: DeleteMedicationRequest):
    response = MedicationDatabase.delete_user_medication(delete_request.user_id, delete_request.medication_id)
    handle_error(response)

    return {"message": "Successfully deleted medication", "medication_id": response[1]}

@router.get("/get-medication/{user_id}")
async def api_get_user_medication(user_id: str):
    response = MedicationDatabase.get_user_medication(user_id)
    handle_error(response)

    return {"message": "User Medication Found", "medications": response[1]}


