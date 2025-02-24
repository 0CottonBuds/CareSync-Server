from fastapi import UploadFile, HTTPException,File, Depends, Form
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from typing import List
import base64

from helpers.error import handle_error
from database.records import MedicationRecordDatabase, BloodPreassureRecordDatabase, BloodSugarRecordDatabase

router = APIRouter(prefix="/records", tags=["Records"])

class AddRecordRequest(BaseModel):
    user_id: str
    type: str
    values: List[str]
    date: Optional[str] = None
    images: Optional[List[str]] = None

class Image(BaseModel):
    # type: str
    base64: str

# Function to parse JSON from form data
def parse_add_request(
    user_id: str = Form(...),
    type: str = Form(...),
    values: str = Form(...),
    date: str | None = Form(...)
):
    import json
    print("parsing input")
    return AddRecordRequest(user_id=user_id, type=type, values=json.loads(values)["values"], date=date)

@router.post("/add-record")
async def add_record(
    add_request: AddRecordRequest 
):
    print("adding record")

    blob_images: list[bytes] = [base64.b64decode(image) for image in add_request.images]

    response: list

    if add_request.date == "" or add_request.date == "None":
        date_now = datetime.today()
        date = date_now.strftime('%Y-%m-%d')
        time = date_now.strftime('%H:%M')
    else:
        date = add_request.date

        date_now = datetime.today()
        time = date_now.strftime('%H:%M')        

    if add_request.type == "medication":
        medication_id = add_request.values[0]
        response = MedicationRecordDatabase.add_record(add_request.user_id, medication_id, blob_images, date, time)
    elif add_request.type == "blood_preassure":
        systol = add_request.values[0]
        diastol = add_request.values[1]
        if(systol == "" or diastol == ""):
            raise HTTPException(status_code=403, detail="Input values are invalid")
        response = BloodPreassureRecordDatabase.add_record(add_request.user_id, systol, diastol, blob_images, date, time)
    elif add_request.type == "blood_sugar":
        blood_glucose = add_request.values[0]
        measurement_unit = add_request.values[1]
        if(blood_glucose == "" or measurement_unit == ""):
            raise HTTPException(status_code=403, detail="Input values are invalid")
        response = BloodSugarRecordDatabase.add_record(add_request.user_id, blood_glucose, measurement_unit, blob_images, date, time)
    else:
        raise HTTPException(status_code=403, details="Forbidden")

    print(response)
    handle_error(response)

    return {"message": "Successfully added record"}

