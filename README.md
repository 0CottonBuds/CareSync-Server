# CareSync-Server

Care Sync is a collaboration project between BSMT of NU MOA and me BSCS of NU Manila

# Instructions

### NOTE: please set your ip to a static ip of 192.168.100.68 for this to work on the mobile app. Not doing this step ill make the app unable to communicate to the server. If you dont want to change your IP to a static IP you then need to recompile the Mobile app and change the IP address there.

1. install python
2. create venv and activate it `python -m venv venv`
3. install dependencies with `pip install -r requirements.txt`
4. run the server with `fastapi run main.py --host 0.0.0.0 --port 8000 --reload`
5. Done!

at this point if there is no errors the server should be working. If you encountered errors dont hesitate to reach out to me

Note: I suggest that when you demonstrate your app modify the Cotton Buds account directly on the sqlite database as it is already populated with data and will be much easier to present
