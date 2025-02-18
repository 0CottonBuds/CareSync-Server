from sqlite3 import Cursor, Connection
import sqlite3
from env import DB_PATH
import random
import string

from helpers.error import Result
 

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
        return [Result.INTERNAL_ERROR, f"Error while creating unique id {e}", 400]

