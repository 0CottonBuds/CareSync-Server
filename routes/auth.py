from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from helpers.error import handle_error, Result
from database.user import UserDatabase 
from database.credentials import login, check_if_username_exists
from database.session_token import create_session_token, validate_session_token


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

class TokenValidationRequest(BaseModel):
    token: str
    user_id: str

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_user(login_request: LoginRequest):
    response = login(login_request.username, login_request.password)
    handle_error(response)
    user_id = response[1]

    response2 = create_session_token(user_id) 
    handle_error(response2)
    token = response2[1]

    return {"message": "successfully logged in", "sessionToken" : token, "userId": user_id}

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
 
@router.post("/validate-session-token")
async def api_validate_session_token(validation_request: TokenValidationRequest):
    response = validate_session_token(validation_request.token, validation_request.user_id) 
    handle_error(response)

    return {"message": "Session token is valid", "isValid": True}


