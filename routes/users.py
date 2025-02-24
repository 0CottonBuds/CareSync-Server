from fastapi import APIRouter, HTTPException
from database.user import UserDatabase 
from helpers.error import handle_error
from base64 import b64decode, b64encode
from pydantic import BaseModel

class AddProfilePicRequest(BaseModel):
    user_id: str
    image: str #base 64

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/get-info/{user_id}")
async def api_get_user_info(user_id: str):
    print(user_id)
    response = UserDatabase.get_user_info(user_id)
    handle_error(response)

    return {"message": "user found", "user": response[1]} 


@router.post("/add-profile-pic")
async def api_add_profile_pic(request: AddProfilePicRequest):
    image_blob = b64decode(request.image)

    print("Attempting to add profile picture")
    response = UserDatabase.add_profile_picture(request.user_id, image_blob)
    handle_error(response)

    return {"message": "Successfully added profile picture"}

@router.get("/get-profile-pic/{user_id}")
async def api_get_profile_pic(user_id: str):
    response = UserDatabase.get_profile_picture(user_id)
    handle_error(response)

    image = b64encode(response[1])

    return {"message": "Profile picture","image": image}