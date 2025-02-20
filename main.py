from fastapi import FastAPI 
import socket

from routes import users, auth, medication, records, medication_analytics, blood_preassure_analytics


app = FastAPI()

@app.get("/")
async def api_home():
    return {"Message:": "Welcome to caresync server"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(medication.router)
app.include_router(records.router)
app.include_router(medication_analytics.router)
app.include_router(blood_preassure_analytics.router)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("\tTo connect to Care Sync server use the following address....For Care Sync client please change the api_url of env.js to the url bellow ")
print("\t\tIPAddress:\t " + s.getsockname()[0])
print("\t\tPort:\t\t 8000")
print(f"\t\tURL:\t\t http://{s.getsockname()[0]}:8000")
s.close()