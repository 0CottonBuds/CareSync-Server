import sqlite3

from env import DB_PATH
from helpers.error import Result
from models.user import User
from database.generate import generate_unique_id

class UserDatabase:

    @staticmethod
    def get_user_info(id: str):
        conn = sqlite3.connect(DB_PATH)
        try: 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (id, ))
            user = cursor.fetchone()
            conn.close()
        except: 
            conn.close()
            return (Result.INTERNAL_ERROR, "Internal error occurred in the server", 400)

        if user == None:
            return (Result.ERROR, "User Not Found", 404)

        user =  User(user_id=user[0], first_name=user[1], last_name=user[2], sex=user[3], birthday=user[4])

        return (Result.SUCCESS, user) 

    @staticmethod
    def create_user(first_name:str, last_name:str, sex:str, birthday:str, username:str, password:str):
        conn = sqlite3.connect(DB_PATH)
        try:
            cursor = conn.cursor()

            response = generate_unique_id(cursor, "user_id", "users")

            if response[0] & (Result.ERROR | Result.INTERNAL_ERROR):
                conn.close() 
                return response
            
            user_id = response[1]
    
            cursor.execute("INSERT INTO users (user_id, first_name, last_name, sex, birthday) VALUES (?, ?, ?, ?, ?)", (user_id, first_name, last_name, sex, birthday))
            cursor.execute("INSERT INTO credentials (user_id, username, password) VALUES (?, ?, ?)", (user_id, username, password))
            conn.commit()
            conn.close()

            print(f"Successfully Created User: {user_id}")
            print(f"FIrst name: {first_name}")
            print(f"Last name: {last_name}")
            print(f"Sex: {sex}")
            print(f"Birthday: {birthday}")
            
            return [Result.SUCCESS, user_id]
        
        except sqlite3.Error as e:
            conn.close()
            return[Result.INTERNAL_ERROR, f"Error when interacting with databse: {e}", 400]

        except Exception as e:
            conn.close()
            return[Result.INTERNAL_ERROR, f"Internal server error {e}", 400]
