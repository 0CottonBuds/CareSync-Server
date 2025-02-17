
from models.user import User
from env import DB_PATH
import sqlite3
import random
import string
    

def get_user_info(id: str):
    conn = sqlite3.connect(DB_PATH)
    try: 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (id, ))
        user = cursor.fetchone()
        conn.close()
    except: 
        conn.close()
        return ("error", "Internal error occurred in the server", 400)

    if len(user) <= 0:
        return ("error", "No user found with that id", 404)

    user =  User(user_id=user[0], first_name=user[1], last_name=user[2], sex=user[3], birthday=user[4])
    # print(user)

    return ("success", user) 

def generate_user_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def create_user(first_name: str, last_name: str, sex: str, birthday:str):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()

        user_id = ""
        while True:
            user_id = generate_user_id()
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if not cursor.fetchone():  # If no existing user_id found, return it
                break


        cursor.execute("INSERT INTO users (user_id, first_name, last_name, sex, birthday) VALUES (?, ?, ?, ?, ?)", (user_id, first_name, last_name, sex, birthday))
        conn.commit()
        conn.close()

        print(f"Successfully Created User: {user_id}")
        print(f"FIrst name: {first_name}")
        print(f"Last name: {last_name}")
        print(f"Sex: {sex}")
        print(f"Birthday: {birthday}")
        
        return ["success", user_id]
    
    except Exception as e:
        conn.close()
        return["error", f"Internal server error {e}", 400]
