from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from helpers.error import handle_error, Result
from database.credentials import login, check_if_username_exists 
from database.user import UserDatabase 


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

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_user(data: LoginRequest):
    response = login(data.username, data.password)
    handle_error(response)

    return {"message": "successfully logged in", "sessionToken" : "testToken", "userId": response[1]}

@router.post("/signup")
async def signup_user(user: SignupRequest):
    response = check_if_username_exists(user.username)
    handle_error(response)
    if(response[0] & Result.FOUND):
        raise HTTPException(status_code=400, detail="Username already exists") 

    response = UserDatabase.create_user(user.first_name, user.last_name, user.sex, user.birthday, user.username, user.password)
    handle_error(response)

    return {"message": "successfully signed up User"}

@router.get("/username-exist")
async def does_username_exist(username: str):
    response = check_if_username_exists(username)
    handle_error(response)
    if(response[0] & Result.SUCCESS):
        raise HTTPException(status_code=400, detail="Username already exists") 
 
@router.get("/validate-session-token")
async def validate_session_token(session_token: str):
    return {"message": "not yet implemented", "isValid": session_token == "testToken"}


