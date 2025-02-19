import traceback
import sqlite3

from env import DB_PATH
from helpers.error import Result


class CredentialsDatabase:

    @staticmethod
    def login(username: str, password: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
            rows = cursor.fetchall()
            conn.close()
            if len(rows) <= 0:
                return (Result.ERROR, "Username was not found", 404)
            
            if password != rows[0][1]:
                return (Result.ERROR, "Wrong password", 400)

            return (Result.SUCCESS, rows[0][2])

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]


    @staticmethod
    def check_if_username_exists(username: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
            rows = cursor.fetchall()
            conn.close()

            if len(rows) <= 0 :
                return [Result.NOT_FOUND, "username not found", 404]

            return [Result.FOUND, "username found"]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]
