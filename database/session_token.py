import sqlite3
import traceback

from datetime import datetime

from env import DB_PATH
from helpers.error import Result
from database.generate import generate_session_token

class SessionTokenDatabase:

    @staticmethod
    def create_session_token(user_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try: 
            response = generate_session_token()
            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                return response
            
            session_token = response[1]

            date_now_string = datetime.today().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO session_tokens (token, user_id, date) VALUES (?, ?, ?)", (session_token, user_id, date_now_string))
            conn.commit()
            conn.close

            return [Result.SUCCESS, session_token]

        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 400]


    @staticmethod
    def validate_session_token(token: str, user_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try: 
            cursor.execute("SELECT date FROM session_tokens WHERE token = ? AND user_id = ? ", (token, user_id))
            session_tokens = cursor.fetchall()
            if len(session_tokens) <= 0:
                return [Result.ERROR, "Cannot find session token", 404]
            
            
            if len(session_tokens) > 1:
                cursor.execute("DELETE FROM session_tokens WHERE user_id = ?", (user_id,))
                return [Result.ERROR, "Session token invalid", 400]
            
            str_session_start_date = session_tokens[0][0] # YYYY-MM-DD
            session_start_date = datetime.strptime(str_session_start_date, "%Y-%m-%d").date()
            date_now = datetime.now().date()

            days_between = (session_start_date - date_now).days
            print("Days between session: ", days_between)

            if days_between >= 3:
                return [Result.ERROR, "Session token expired", 410]

            return [Result.SUCCESS, "Session token valid"]
        except sqlite3.Error as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 500]

        except Exception as e:
            conn.close()
            print(traceback.format_exc())
            return [Result.INTERNAL_ERROR, f"internal server error {e}", 500]


