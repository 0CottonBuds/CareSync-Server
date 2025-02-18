from fastapi import APIRouter, HTTPException
from database.user import UserDatabase 
from helpers.error import handle_error

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/get-info/{user_id}")
async def api_get_user_info(user_id: str):
    response = UserDatabase.get_user_info(user_id)
    handle_error(response)

    return {"message": "user found", "user": response[1]} 

