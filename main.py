from fastapi import FastAPI
from models.user import User
from database.auth import login, signup
from database.user import get_user_info
from database.medication import get_user_medication

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    sex: str
    birtday: str
    username: str
    password: str
 
app = FastAPI()
@app.get("/")
async def api_home():
    return {"Message:": "API working corectly"}

@app.post("/auth/login")
async def api_login(data: LoginRequest):
    print(data.username)
    print(data.password)
    isSuccess = login(data.username, data.password)

    if isSuccess:
        return {"message": "successfully logged in", "sessionToken" : "testToken", "userId": "TESTID1234"}
    else:
        return {"message": "login unsuccessful"}

@app.get("/auth/validate-session-token")
async def api_validate_session_token(session_token: str):
    return {"message": "not yet implemented", "isValid": session_token == "testToken"}

@app.post("/auth/signup")
async def api_signup(user: SignupRequest):
    isSuccess = signup(user)
    if isSuccess:
        return {"message": "successfully signed up"}
    else:
        return {"message": "signup unsuccessful"}

@app.get("/user/get-info/{user_id}")
async def api_get_user_info(user_id: str):
    user = get_user_info(user_id)

    if user is None:
        return {"message": "user not found"}
    else:
        return {"message": "user foind", "user": user} 

@app.get("/user/medication/get-medication/{user_id}")
async def api_get_user_medication(user_id: str):
    user_medication = get_user_medication(user_id)

    if user_medication == None:
        return {"message": "No Medication Found"}
    else:
        return {"message": "User Medication Found", "medication": user_medication}

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("Connect to")
print("IPAddress: " + s.getsockname()[0])
print("Port: 8000")
s.close()