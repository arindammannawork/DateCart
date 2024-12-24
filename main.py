from fastapi import FastAPI
from config import *
from helper.helper_funtions import *
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router 



# Create a new client and connect to the server



app = FastAPI()
# Allow CORS for Swagger testing if needed

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])



@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}


# @app.get("/")
# async def root():
#     try:
#         user= db.users.find_one({"email": "arindam@gmail.com"})
#         user=convert_objectid(user)
#         print(type(user))
#         return {"message": "fds","email":user}
#     except Exception as e:
#          print(f"error {e}")
#          return {"message": f"Error in fetching data {e}"}


# @app.post("/api/auth/login")
# def get_user(response):
#     print(json.dumps(response))
#     return {"message": "Logged in successfully"}

# @app.get("/data")
# def get_data(num:str=None):
#         return {"n":num}