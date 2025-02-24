from datetime import date, timedelta, datetime
from fastapi import APIRouter
from pydantic import BaseModel
from calendar import month_name
from typing import Optional

from helpers.error import handle_error
from models.medication import Medication
from database.medication import MedicationDatabase
from database.records import MedicationRecordDatabase, MedicationRecord
from helpers.datetime import convert_str_time_to_minutes, convert_minutes_to_str_time

router = APIRouter(prefix="/analytics/medication", tags=["Medication Analytics"])

class MedicationMonthAnalyticsRequest(BaseModel):
    user_id: str
    year: str
    month: str

class MedicationDayAnalytics(BaseModel):
    date: str
    medication_id: str
    medication_name: str
    times_skipped: Optional[list[str]] = [] 
    times_late: Optional[list[str]] = [] 
    times_early: Optional[list[str]] = []
    times_taken: Optional[list[str]] = [] 
    times_extra: Optional[list[str]] =[]

@router.post("/month")
async def get_medication_analytics_by_month(request: MedicationMonthAnalyticsRequest):
    response = MedicationRecordDatabase.get_records_by_month(request.user_id, request.month, request.year, False)
    handle_error(response) 
    records: list[MedicationRecord] = response[1] 

    response = MedicationDatabase.get_user_medication(request.user_id)
    handle_error(response)    
    medications: list[Medication] = response[1] 

    analytics = {}

    curr_date = date(int(request.year), int(request.month), 1)
    while curr_date.month == int(request.month):
        curr_date_str = curr_date.strftime('%Y-%m-%d')

        if curr_date > datetime.today().date():
            print("Exceeded current date: ", curr_date.strftime('%Y-%m-%d'))
            analytics.update({curr_date_str : []})
            curr_date += timedelta(days=1)
            continue
        print("Current Date: ", curr_date.strftime("%Y-%m-%d"))


        curr_day_records = [record for record in records if record.date == curr_date_str]

        records_for_each_medication: dict[list[MedicationRecord]]= {}
        
        for time in curr_day_records:
            if time.medication_id not in records_for_each_medication.keys():
                records_for_each_medication[time.medication_id] = [time]
            else:
                records_for_each_medication[time.medication_id].append(time)
        

        curr_day_analytics = []
        for medication in medications:
            date_added = datetime.strptime(medication.date_added, "%Y-%m-%d").date()

            if(date_added > curr_date):
                continue
        
            curr_medication_analytics: MedicationDayAnalytics = MedicationDayAnalytics(date=curr_date_str, medication_id=medication.medication_id, medication_name=medication.medication_name)
            if medication.medication_id not in records_for_each_medication.keys():
                curr_medication_analytics.times_skipped.extend(medication.time_to_take)
            else:
                times_to_take: list[int] = [convert_str_time_to_minutes(time) for time in medication.time_to_take]
                times_to_take.sort()
                times_taken: list[int] = [convert_str_time_to_minutes(record.time) for record in records_for_each_medication[medication.medication_id]]
                times_taken.sort()

                tolerance = 30 #min
                while len(times_taken) > 0 and len(times_to_take) > 0:
                    curr_time_to_take = times_to_take.pop()
                    curr_time_taken = times_taken.pop()
                    curr_time_taken_str = convert_minutes_to_str_time(curr_time_taken)

                    if curr_time_to_take - tolerance > curr_time_taken:
                        curr_medication_analytics.times_early.append(str(curr_time_taken_str))
                    elif curr_time_to_take + tolerance < curr_time_taken:
                        curr_medication_analytics.times_late.append(str(curr_time_taken_str))
                    else:
                        curr_medication_analytics.times_taken.append(str(curr_time_taken_str))
                
                for time in times_to_take:
                    curr_medication_analytics.times_skipped.append(convert_minutes_to_str_time(time))
                for time in times_taken:
                    curr_medication_analytics.times_extra.append(convert_minutes_to_str_time(time))


            curr_day_analytics.append(curr_medication_analytics) # Note: Dictionary{medication_id, analytics}

        analytics.update({curr_date_str : curr_day_analytics})
        curr_date += timedelta(days=1)


    return {"message": f"Analytics for month: {month_name[int(request.month)]}, {request.year}", "records": analytics}