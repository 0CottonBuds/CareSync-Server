from fastapi import HTTPException

class Result:
    SUCCESS = 1
    ERROR = 2
    INTERNAL_ERROR = 4
    FOUND = 8
    NOT_FOUND = 16

def handle_error(response: list, prefix: str = "", suffix: str = ""):
    result = response[0] 
    if(result & Result.ERROR):
        raise HTTPException(status_code=response[2], detail=prefix + response[1] + suffix) 
    elif(result & Result.INTERNAL_ERROR):
        print(f"Internal Error occurred in server: {response[1]}")
        raise HTTPException(status_code=400, detail="Internal Server Error!") 


