from models.medication import Medication
from database.generate_id import generate_unique_id
import sqlite3
import traceback
from env import DB_PATH

from helpers.error import Result, handle_error


class MedicationDatabase:

    @staticmethod
    def get_user_medication(user_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT medication_id, medication_name FROM medication WHERE user_id = ?", (user_id, ))
            medication_data = cursor.fetchall()

            medication_list = []
            for data in medication_data:
                curr_medication_id = data[0]
                curr_medication_name = data[1]
                curr_time_to_take = []

                cursor.execute("SELECT time FROM time_to_take WHERE medication_id = ?", (curr_medication_id, ))
                times = cursor.fetchall()

                for time in times:
                    curr_time_to_take.append(time[0])
                
                curr_medication = Medication(medication_id=curr_medication_id, user_id=user_id, medication_name=curr_medication_name, time_to_take=curr_time_to_take)

                medication_list.append(curr_medication)

            conn.close()

            return [Result.SUCCESS, medication_list]
        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error while interacting with database: {e}"]
        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, str(e)]

    @staticmethod
    def add_user_medication(user_id: str, medication_name: str, time_to_take: list[str]):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            response = generate_unique_id(cursor, "medication_id", "medication")

            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                return response

            medication_id: str= response[1]
            print(response)
            print(medication_id)
            cursor.execute("INSERT INTO medication (user_id, medication_id, medication_name) VALUES (?, ?, ?)", (user_id, medication_id, medication_name))

            for time in time_to_take:
                cursor.execute("INSERT INTO time_to_take (medication_id, time) VALUES (?, ?)", (medication_id, time))

            conn.commit()
            conn.close()
            return [Result.SUCCESS, medication_id]
        
        except Exception as e:
            conn.close()
            return [Result.INTERNAL_ERROR, f'Internal server error {e}', 400]

    def edit_user_medication(user_id: str, medication_id: str, medication_name: str, time_to_take: list[str]):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM medication WHERE medication_id = ? AND user_id = ?", (medication_id, user_id))
            if len(cursor.fetchall())  <= 0:
                return [Result.ERROR, "Medication not found!", 404]

            cursor.execute("UPDATE medication SET medication_name = ? WHERE medication_id = ? AND user_id = ?", (medication_name, medication_id, user_id))
            cursor.execute("DELETE FROM time_to_take WHERE medication_id = ?", (medication_id, ))

            for time in time_to_take:
                cursor.execute("INSERT INTO time_to_take (medication_id, time) VALUES (?, ?)", (medication_id, time))

            conn.commit()
            conn.close()
            return [Result.SUCCESS, medication_id]
        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]

    def delete_user_medication(user_id: str, medication_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try: 
            cursor.execute("SELECT * FROM medication WHERE medication_id = ? AND user_id = ?", (medication_id, user_id))
            if len(cursor.fetchall())  <= 0:
                return [Result.ERROR, "Medication not found!", 404]

            cursor.execute("DELETE FROM medication where medication_id = ? AND user_id = ?", (medication_id, user_id))

            conn.commit()
            conn.close()
            return [Result.SUCCESS, medication_id]
        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]