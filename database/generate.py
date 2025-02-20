import traceback
import sqlite3
import random
import string

from env import DB_PATH
from helpers.error import Result
from sqlite3 import Cursor, Connection
 

def generate_unique_id(cursor: Cursor | None, column: str, table: str):
    conn: Connection | None = None
    if cursor == None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

    try:
        id = ""
        while True:
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cursor.execute(f"SELECT {column} FROM {table} WHERE {column} = ?", (id,))
            if not cursor.fetchone():  # If no existing user_id found, return it
                if conn is not None:
                    conn.close()
                return [Result.SUCCESS, id]
    except Exception as e:
        if conn is not None:
            conn.close()
        print(traceback.format_exc())
        return [Result.INTERNAL_ERROR, f"Error while creating unique id {e}", 400]

# this is special as records are separeted between tables
def generate_unique_record_id(cursor: Cursor | None):
    conn: Connection | None = None
    if cursor == None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

    try:
        id = ""
        while True:
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cursor.execute(f"SELECT record_id FROM medication_records WHERE record_id = ?", (id,))
            medication = cursor.fetchall()
            cursor.execute(f"SELECT record_id FROM blood_preassure_records WHERE record_id = ?", (id,))
            blood_pressure = cursor.fetchall()
            cursor.execute(f"SELECT record_id FROM blood_sugar_records WHERE record_id = ?", (id,))
            blood_sugar = cursor.fetchall()

            if not medication and not blood_pressure and not blood_pressure:  # If no existing user_id found, return it
                if conn is not None:
                    conn.close()
                return [Result.SUCCESS, id]
    except Exception as e:
        if conn is not None:
            conn.close()
        print(traceback.format_exc())
        return [Result.INTERNAL_ERROR, f"Error while creating unique id {e}", 400]



# same as generate_unique_id but has 32 length and only ascii upercase and ascii lowercase
def generate_session_token(cursor: Cursor | None = None):
    conn: Connection | None = None
    if cursor == None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

    try:
        token = ""
        while True:
            token = ''.join(random.choices(string.ascii_letters, k=32))
            cursor.execute(f"SELECT token FROM session_tokens WHERE token = ?", (token,))
            if not cursor.fetchone():  # If no existing user_id found, return it
                if conn is not None:
                    conn.close()
                return [Result.SUCCESS, token]
    except Exception as e:
        if conn is not None:
            conn.close()
        print(traceback.format_exc())
        return [Result.INTERNAL_ERROR, f"Error while creating session token {e}", 400]


