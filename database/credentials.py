from models.user import User
from env import DB_PATH
import sqlite3

from helpers.error import Result


def login(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
    rows = cursor.fetchall()
    conn.close()
    if len(rows) <= 0:
        return (Result.ERROR, "Username was not found", 404)
    
    if password != rows[0][1]:
        return (Result.ERROR, "Wrong password", 400)

    return (Result.SUCCESS, rows[0][2])

def check_if_username_exists(username: str):

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        return [Result.INTERNAL_ERROR, f"Error has occurred when checking if username exists: {e}", 400]

    if len(rows) <= 0 :
        return [Result.NOT_FOUND, "username not found", 404]

    return [Result.FOUND, "username found"]

