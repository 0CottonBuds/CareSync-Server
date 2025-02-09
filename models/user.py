import datetime
from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    sex: str
    birtday: datetime.date
    username: str
    password: str

    
