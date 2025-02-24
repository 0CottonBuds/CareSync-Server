
from datetime import datetime, timedelta, date
from pydantic import BaseModel
from typing import Optional
import traceback
import sqlite3 

from helpers.measurement_unit import convert_blood_glucose_unit
from env import DB_PATH
from helpers.error import Result
from database.generate import generate_unique_record_id 


class MedicationRecord(BaseModel):
    record_id: Optional[str] = None
    user_id: Optional[str] = None
    medication_id: str
    date: str
    time: str
    attachmends: Optional[list[bytes]] = None


class MedicationRecordDatabase:
    @staticmethod 
    def add_record(user_id: str, medication_id: str, images: list, date, time):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM medication WHERE user_id = ? AND medication_id = ?", (user_id, medication_id))
            if len(cursor.fetchall()) <= 0:
                return [Result.ERROR, "Medication not found", 404]
            
            response = generate_unique_record_id(cursor)
            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                return response

            record_id = response[1]
            attachment1 = images[0] if len(images) >= 1 else None
            attachment2 = images[1] if len(images) >= 2 else None
            attachment3 = images[2] if len(images) >= 3 else None
            cursor.execute("INSERT INTO medication_records (record_id, user_id, medication_id, date, time, attachment1, attachment2, attachment3) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (record_id, user_id, medication_id, date, time, attachment1, attachment2, attachment3))
            
            conn.commit()
            conn.close()

            return [Result.SUCCESS, record_id]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

    @staticmethod
    def get_records_by_month(user_id:str, month: str, year:str, with_images = False):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try: 
            if with_images:
                cursor.execute("SELECT record_id, medication_id, date, time, attachment1, attachment2, attachment3 time FROM medication_records WHERE user_id = ? AND date LIKE ?", (user_id, f"{year}-{month}%"))
            else:
                cursor.execute("SELECT record_id, medication_id, date, time FROM medication_records WHERE user_id = ? AND date LIKE ?", (user_id, f"{year}-{month}%"))
            raw_records = cursor.fetchall()

            medication_records: list[MedicationRecord] = []
            for record in raw_records:
                curr_record_id = record[0]
                curr_medication_id = record[1]
                curr_date = record[2]
                curr_time = record[3]

                curr_medication_record = MedicationRecord(user_id=user_id, record_id=curr_record_id, medication_id=curr_medication_id, date=curr_date, time=curr_time)
                medication_records.append(curr_medication_record)

            conn.close()
            return [Result.SUCCESS, medication_records] 
        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

class BloodPreassureRecord(BaseModel):
    record_id: Optional[str] = None
    user_id: Optional[str] = None
    systol: str
    diastol: str
    date: str
    time: str
    attachmends: Optional[list[bytes]] = None


class BloodPreassureRecordDatabase:
    @staticmethod 
    def add_record(user_id: str, systol: str, diastol, images: list, date, time):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            response = generate_unique_record_id(cursor)
            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                return response

            record_id = response[1]
            attachment1 = images[0] if len(images) >= 1 else None
            attachment2 = images[1] if len(images) >= 2 else None
            attachment3 = images[2] if len(images) >= 3 else None
            cursor.execute("INSERT INTO blood_preassure_records (record_id, user_id, systol, diastol, date, time, attachment1, attachment2, attachment3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (record_id, user_id, systol, diastol, date, time, attachment1, attachment2, attachment3))
            
            conn.commit()
            conn.close()

            return [Result.SUCCESS, record_id]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]
    
    @staticmethod
    def get_records_for_week(user_id: str, end_date_str: str):
        '''returns 7 dates starting from date param'''

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            start_date = datetime.strptime(end_date_str, "%Y-%m-%d") - timedelta(days=6)
            start_date_str = start_date.strftime("%Y-%m-%d")

            cursor.execute("SELECT record_id, systol, diastol, date, time  FROM blood_preassure_records WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date ASC", (user_id ,start_date_str, end_date_str))
            raw_records = cursor.fetchall()

            blood_pressure_record : list[BloodPreassureRecord] = []
            for raw_record in raw_records:
                curr_record_id = raw_record[0]
                curr_systol = raw_record[1]
                curr_diastol = raw_record[2]
                curr_date = raw_record[3]
                curr_time = raw_record[4]

                curr_blood_pressure_Record = BloodPreassureRecord(record_id=curr_record_id, systol=curr_systol, diastol=curr_diastol, date=curr_date, time=curr_time)

                blood_pressure_record.append(curr_blood_pressure_Record)


            blood_pressure_record : list[BloodPreassureRecord] = sorted(blood_pressure_record, key=lambda record: record.date)

            blood_preassure_record_with_date : dict[list[BloodPreassureRecord]] = {}

            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            curr_date = start_date
            while not curr_date >= end_date:
                curr_date_str = curr_date.strftime("%Y-%m-%d")

                curr_date_records = [record for record in blood_pressure_record if record.date == curr_date_str]

                blood_preassure_record_with_date.update({curr_date_str: curr_date_records})

                curr_date = curr_date + timedelta(days=1)


            return [Result.SUCCESS, blood_preassure_record_with_date]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]
    
    def get_records_for_month(user_id: str, year: str, month:str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT record_id, systol, diastol , date, time FROM blood_preassure_records WHERE user_id = ? AND date LIKE ?", (user_id, f"{year}-{month}%"))
            raw_records = cursor.fetchall()

            blood_pressure_record : list[BloodPreassureRecord] = []
            for raw_record in raw_records:
                curr_record_id = raw_record[0]
                curr_systol = raw_record[1]
                curr_diastol = raw_record[2]
                curr_date = raw_record[3]
                curr_time = raw_record[4]

                curr_blood_pressure_Record = BloodPreassureRecord(record_id=curr_record_id, systol=curr_systol, diastol=curr_diastol, date=curr_date, time=curr_time)

                blood_pressure_record.append(curr_blood_pressure_Record)


            blood_pressure_record : list[BloodPreassureRecord] = sorted(blood_pressure_record, key=lambda record: record.date)

            blood_preassure_record_with_date : dict[list[BloodPreassureRecord]] = {}

            curr_date = date(int(year), int(month), 1)
            while curr_date.month == int(month):
                curr_date_str = curr_date.strftime("%Y-%m-%d")

                curr_date_records = [record for record in blood_pressure_record if record.date == curr_date_str]

                blood_preassure_record_with_date.update({curr_date_str: curr_date_records})

                curr_date = curr_date + timedelta(days=1)


            return [Result.SUCCESS, blood_preassure_record_with_date]


        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

class BloodSugarRecord(BaseModel):
    record_id: Optional[str] = None
    user_id: Optional[str] = None
    blood_glucose: str
    measurement_unit: str
    date: str
    time: str
    attachmends: Optional[list[bytes]] = None


class BloodSugarRecordDatabase:
    @staticmethod 
    def add_record(user_id: str, blood_glucose: str, blood_sugar: str, images: list, date, time):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            response = generate_unique_record_id(cursor)
            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                return response

            record_id = response[1]
            attachment1 = images[0] if len(images) >= 1 else None
            attachment2 = images[1] if len(images) >= 2 else None
            attachment3 = images[2] if len(images) >= 3 else None
            cursor.execute("INSERT INTO blood_sugar_records (record_id, user_id, blood_glucose, measurement_unit, date, time, attachment1, attachment2, attachment3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (record_id, user_id, blood_glucose, blood_sugar, date, time, attachment1, attachment2, attachment3))
            
            conn.commit()
            conn.close()

            return [Result.SUCCESS, record_id]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

    @staticmethod
    def get_records_for_week(user_id: str, end_date_str: str):
        '''returns 7 dates starting from date param'''

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            start_date = datetime.strptime(end_date_str, "%Y-%m-%d") - timedelta(days=6)
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            end_date_str_ = end_date.strftime("%Y-%m-%d") # for some reasons the first date is not included here

            cursor.execute("SELECT record_id, blood_glucose, measurement_unit, date, time  FROM blood_sugar_records WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date ASC", (user_id ,start_date_str, end_date_str_))
            raw_records = cursor.fetchall()

            blood_sugar_record : list[BloodSugarRecord] = []
            for raw_record in raw_records:
                curr_record_id = raw_record[0]
                curr_blood_glucose = raw_record[1]
                curr_measurement_unit = raw_record[2]
                curr_date = raw_record[3]
                curr_time = raw_record[4]

                curr_blood_pressure_Record = BloodSugarRecord(record_id=curr_record_id, blood_glucose=curr_blood_glucose, measurement_unit=curr_measurement_unit, date=curr_date, time=curr_time)

                blood_sugar_record.append(curr_blood_pressure_Record)


            blood_sugar_record : list[BloodSugarRecord] = sorted(blood_sugar_record, key=lambda record: record.date)

            blood_sugar_record_with_date : dict[list[BloodSugarRecord]] = {}

            curr_date = start_date
            while not curr_date >= end_date:
                curr_date_str = curr_date.strftime("%Y-%m-%d")

                curr_date_records = [record for record in blood_sugar_record if record.date == curr_date_str]

                blood_sugar_record_with_date.update({curr_date_str: curr_date_records})

                curr_date = curr_date + timedelta(days=1)


            return [Result.SUCCESS, blood_sugar_record_with_date]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]
    
    
    def get_records_for_month(user_id: str, year: str, month:str, measurement_unit: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT record_id, blood_glucose, measurement_unit, date, time FROM blood_sugar_records WHERE user_id = ? AND date LIKE ?", (user_id, f"{year}-{month}%"))
            raw_records = cursor.fetchall()

            blood_sugar_records : list[BloodSugarRecord] = []
            for raw_record in raw_records:
                curr_record_id = raw_record[0]
                curr_blood_glucose = raw_record[1]
                curr_measurement_unit = raw_record[2]
                curr_date = raw_record[3]
                curr_time = raw_record[4]

                curr_blood_glucose = str(convert_blood_glucose_unit(float(curr_blood_glucose), measurement_unit) if curr_measurement_unit.lower() != measurement_unit.lower() else curr_blood_glucose)
                curr_measurement_unit = measurement_unit

                curr_blood_pressure_Record = BloodSugarRecord(record_id=curr_record_id, blood_glucose=curr_blood_glucose, measurement_unit=curr_measurement_unit, date=curr_date, time=curr_time)

                blood_sugar_records.append(curr_blood_pressure_Record)


            blood_sugar_records : list[BloodSugarRecord] = sorted(blood_sugar_records, key=lambda record: record.date)

            blood_sugar_records_with_date : dict[list[BloodSugarRecord]] = {}

            curr_date = date(int(year), int(month), 1)
            while curr_date.month == int(month):
                curr_date_str = curr_date.strftime("%Y-%m-%d")

                curr_date_records = [record for record in blood_sugar_records if record.date == curr_date_str]

                blood_sugar_records_with_date.update({curr_date_str: curr_date_records})

                curr_date = curr_date + timedelta(days=1)


            return [Result.SUCCESS, blood_sugar_records_with_date]


        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

 