from calendar import month_name
from fastapi import APIRouter
from pydantic import BaseModel
import sys

from helpers.error import handle_error
from database.records import BloodPreassureRecordDatabase

router = APIRouter(prefix="/analytics/blood-pressure", tags=["Blood Pressure Analytics"])

class BloodPressureWeekAnalyticsRequest(BaseModel):
    user_id: str
    date: str # records will be this date and 6 dates before that

class BloodPressureMonthAnalyticsRequest(BaseModel):
    user_id: str
    year: str
    month: str


@router.post("/week")
async def get_analytics_for_week(request: BloodPressureWeekAnalyticsRequest):
    response = BloodPreassureRecordDatabase.get_records_for_week(request.user_id, request.date)
    handle_error(response)

    blood_pressure_records_with_date : dict= response[1]

    average_systol = 0
    average_diastol = 0

    max_systol = 0
    max_diastol = 0

    min_systol = sys.maxsize 
    min_diastol = sys.maxsize

    sum_systol = 0
    sum_diastol = 0

    num_records = 0


    for date, records in blood_pressure_records_with_date.items():
        
        for record in records:
            max_systol = int(record.systol) if int(record.systol) > max_systol else max_systol
            max_diastol = int(record.diastol) if int(record.diastol) > max_diastol else max_diastol

            min_systol = int(record.systol) if int(record.systol) < min_systol else min_systol
            min_diastol = int(record.diastol) if int(record.diastol) < min_diastol else min_diastol

            sum_systol += int(record.systol)
            sum_diastol += int(record.diastol)
            
            num_records += 1
        
    average_systol = sum_systol // num_records
    average_diastol = sum_diastol // num_records
    
    return {
                "message": f"Week analytics ending on {request.date}", 
                "details": {
                    "average: " : {
                        "systol": str(average_systol),
                        "diastol": str(average_diastol) 
                    },
                    "Highest: " : {
                        "systol": str(max_systol),
                        "diastol": str(max_diastol) 
                    },
                    "Lowest: " : {
                        "systol": str(min_systol),
                        "diastol": str(min_diastol) 
                    }
                },
                "history": blood_pressure_records_with_date
           }

@router.post("/month")
async def get_analytics_for_month(request: BloodPressureMonthAnalyticsRequest):
    response = BloodPreassureRecordDatabase.get_records_for_month(request.user_id, request.year, request.month)
    handle_error(response)

    blood_pressure_records_with_date : dict= response[1]

    average_systol = 0
    average_diastol = 0

    max_systol = 0
    max_diastol = 0

    min_systol = sys.maxsize 
    min_diastol = sys.maxsize

    sum_systol = 0
    sum_diastol = 0

    num_records = 0


    for date, records in blood_pressure_records_with_date.items():
        
        for record in records:
            max_systol = int(record.systol) if int(record.systol) > max_systol else max_systol
            max_diastol = int(record.diastol) if int(record.diastol) > max_diastol else max_diastol

            min_systol = int(record.systol) if int(record.systol) < min_systol else min_systol
            min_diastol = int(record.diastol) if int(record.diastol) < min_diastol else min_diastol

            sum_systol += int(record.systol)
            sum_diastol += int(record.diastol)
            
            num_records += 1
        
    average_systol = sum_systol // num_records
    average_diastol = sum_diastol // num_records
    
    return {
                "message": f"analytics for month: {month_name[int(request.month)]}, {request.year}", 
                "details": {
                    "average: " : {
                        "systol": str(average_systol),
                        "diastol": str(average_diastol) 
                    },
                    "Highest: " : {
                        "systol": str(max_systol),
                        "diastol": str(max_diastol) 
                    },
                    "Lowest: " : {
                        "systol": str(min_systol),
                        "diastol": str(min_diastol) 
                    }
                },
                "history": blood_pressure_records_with_date
           }
