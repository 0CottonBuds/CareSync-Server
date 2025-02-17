from models.user import User
from env import DB_PATH
import sqlite3

def login(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
    rows = cursor.fetchall()
    conn.close()
    if len(rows) <= 0:
        return ("error", "Username was not found")
    
    if password != rows[0][1]:
        return ("error", "Wrong password")

    return ("success", rows[0][2])

def check_if_username_exists(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials where username = ?", (username, ))
    rows = cursor.fetchall()
    conn.close()

    if len(rows) <= 0 :
        return ["error", "username not found", 404]

    return ["success", "username found"]

def create_credentials(user_id:str, username:str, password:str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO credentials (user_id, username, password) VALUES (?, ?, ?)", (user_id, username, password))
        conn.commit()
        return ["success", "successfully created"]
    except:
        return ["error", f'Cannot create credentials for user: {user_id}', 400]


