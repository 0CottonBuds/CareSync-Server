from calendar import month_name
from fastapi import APIRouter
from pydantic import BaseModel
import sys

from helpers.error import handle_error
from database.records import BloodSugarRecordDatabase 
from helpers.measurement_unit import convert_blood_glucose_unit

router = APIRouter(prefix="/analytics/blood-sugar", tags=["Blood Sugar Analytics"])

class BloodSugarWeekAnalyticsRequest(BaseModel):
    user_id: str
    date: str # records will be this date and 6 dates before that
    measurement_unit: str

class BloodSugarMonthAnalyticsRequest(BaseModel):
    user_id: str
    year: str
    month: str
    measurement_unit: str

@router.post("/week")
async def get_analytics_for_week(request: BloodSugarWeekAnalyticsRequest):
    response = BloodSugarRecordDatabase.get_records_for_week(request.user_id, request.date)
    handle_error(response)

    blood_sugar_records_with_date : dict= response[1]

    average_blood_glucose = 0
    max_blood_glucose = 0
    min_blood_glucose = sys.maxsize

    sum_blood_glucose = 0

    num_records = 0


    for date, records in blood_sugar_records_with_date.items():
        
        for record in records:
            curr_blood_glucose = float(record.blood_glucose) if record.measurement_unit == request.measurement_unit else convert_blood_glucose_unit(float(record.blood_glucose), request.measurement_unit)
            record.blood_glucose = curr_blood_glucose
            record.measurement_unit = request.measurement_unit

            max_blood_glucose = curr_blood_glucose if curr_blood_glucose > max_blood_glucose else max_blood_glucose
            min_blood_glucose = curr_blood_glucose if curr_blood_glucose < min_blood_glucose else min_blood_glucose

            sum_blood_glucose += float(curr_blood_glucose)
            
            num_records += 1
        
    average_blood_glucose = sum_blood_glucose // num_records

    print(blood_sugar_records_with_date)
    
    return {
                "message": f"Week analytics ending on {request.date}", 
                "details": {
                    "average" : average_blood_glucose,
                    "Highest" : max_blood_glucose,
                    "Lowest" : min_blood_glucose
                },
                "history": blood_sugar_records_with_date
           }

@router.post("/month")
async def get_analytics_for_month(request: BloodSugarMonthAnalyticsRequest):
    response = BloodSugarRecordDatabase.get_records_for_month(request.user_id, request.year, request.month, request.measurement_unit)
    handle_error(response)

    blood_sugar_records_with_date : dict= response[1]

    average_blood_glucose = 0
    max_blood_glucose = 0
    min_blood_glucose = sys.maxsize

    sum_blood_glucose = 0

    num_records = 0


    for date, records in blood_sugar_records_with_date.items():
        
        for record in records:
            curr_blood_glucose = float(record.blood_glucose) if record.measurement_unit == request.measurement_unit else convert_blood_glucose_unit(float(record.blood_glucose), request.measurement_unit)

            record.blood_glucose = curr_blood_glucose
            record.measurement_unit = request.measurement_unit

            max_blood_glucose = curr_blood_glucose if curr_blood_glucose > max_blood_glucose else max_blood_glucose
            min_blood_glucose = curr_blood_glucose if curr_blood_glucose < min_blood_glucose else min_blood_glucose

            sum_blood_glucose += float(curr_blood_glucose)
            
            num_records += 1
        
    average_blood_glucose = sum_blood_glucose // num_records
    
    return {
                "message": f"analytics for month: {month_name[int(request.month)]}, {request.year}", 
                "details": {
                    "average" : average_blood_glucose,
                    "Highest" : max_blood_glucose,
                    "Lowest" : min_blood_glucose
                },
                "history": blood_sugar_records_with_date
           }
