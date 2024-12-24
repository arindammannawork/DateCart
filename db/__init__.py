from config import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db=client.datenote
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)