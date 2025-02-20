from fastapi import UploadFile, HTTPException,File, Depends, Form
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import List

from helpers.error import handle_error
from database.records import MedicationRecordDatabase, BloodPreassureRecordDatabase, BloodSugarRecordDatabase

router = APIRouter(prefix="/records", tags=["Records"])

class AddRecordRequest(BaseModel):
    user_id: str
    type: str
    values: List[str]

# Function to parse JSON from form data
def parse_add_request(
    user_id: str = Form(...),
    type: str = Form(...),
    values: str = Form(...)
):
    import json
    return AddRecordRequest(user_id=user_id, type=type, values=json.loads(values)["values"])

@router.post("/add-record/")
async def add_record(
    add_request: AddRecordRequest = Depends(parse_add_request),  
    images: List[UploadFile] = File(...) 
):

    blob_images: list[bytes] = [await image.read() for image in images]

    response: list

    date_now = datetime.today()
    date = date_now.strftime('%Y-%m-%d')
    time = date_now.strftime('%H-%M')
    
    if add_request.type == "medication":
        medication_id = add_request.values[0]
        response = MedicationRecordDatabase.add_record(add_request.user_id, medication_id, blob_images, date, time)
    elif add_request.type == "blood_preassure":
        systol = add_request.values[0]
        diastol = add_request.values[1]
        response = BloodPreassureRecordDatabase.add_record(add_request.user_id, systol, diastol, blob_images, date, time)
    elif add_request.type == "blood_sugar":
        blood_glucose = add_request.values[0]
        measurement_unit = add_request.values[1]
        response = BloodSugarRecordDatabase.add_record(add_request.user_id, blood_glucose, measurement_unit, blob_images, date, time)
    else:
        raise HTTPException(status_code=403, details="Forbidden")

    handle_error(response)

    return {"message": "Successfully added record"}

