from fastapi import FastAPI, HTTPException
from models.user import User
from database.auth import login, check_if_username_exists, create_credentials
from database.user import get_user_info, create_user
from database.medication import get_user_medication

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    sex: str
    birthday: str
    username: str
    password: str
 
app = FastAPI()
@app.get("/")
async def api_home():
    return {"Message:": "API working corectly"}

@app.post("/auth/login")
async def api_login(data: LoginRequest):
    response = login(data.username, data.password)

    if response[0] == "success":
        return {"message": "successfully logged in", "sessionToken" : "testToken", "userId": response[1]}
    else:
        raise HTTPException(status_code=400, detail=response[1]) 

@app.get("/auth/validate-session-token")
async def api_validate_session_token(session_token: str):
    return {"message": "not yet implemented", "isValid": session_token == "testToken"}

@app.post("/auth/signup")
async def api_signup(user: SignupRequest):

    response = check_if_username_exists(user.username)
    if(response[0] == "success"):
        raise HTTPException(status_code=400, detail="username already exists") 
    
    response = create_user(user.first_name, user.last_name, user.sex, user.birthday)
    if(response[0] == "error"):
        raise HTTPException(status_code=response[2], detail=response[1] + " while creating user") 

    user_id = response[1]
    
    response = create_credentials(user_id, user.username, user.password)
    if(response[0] == "error"):
        raise HTTPException(status_code=response[2], detail=response[1] + " while creating credentials") 

    if response[0] == "success":
        return {"message": "successfully signed up"}
    else:
        raise HTTPException(status_code=response[2], detail=response[1])


@app.get("/user/get-info/{user_id}")
async def api_get_user_info(user_id: str):
    response = get_user_info(user_id)

    if response[0] == "success":
        return {"message": "user foind", "user": response[1]} 
    else:
        raise HTTPException(status_code=response[2], detail=response[1]) 


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