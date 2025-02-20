from pydantic import BaseModel
from typing import Optional
import traceback
import sqlite3 

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
