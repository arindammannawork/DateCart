from fastapi import FastAPI
from config import *
from helper.helper_funtions import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# uri = "mongodb+srv://arindammannawork:SW-B4izi.X4Z$6e@cluster0.rh5ki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db=client.datenote
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app = FastAPI()


@app.get("/")
async def root():
    try:
        user= db.users.find_one({"email": "arindam@gmail.com"})
        user=convert_objectid(user)
        print(type(user))
        return {"message": "fds","email":user}
    except Exception as e:
         print(f"error {e}")
         return {"message": f"Error in fetching data {e}"}


@app.get("/user/{userId}")
def get_user(userId: int):
    return {"userId": userId, "name": f"User {userId}"}

@app.get("/data")
def get_data(num:str=None):
        return {"n":num}