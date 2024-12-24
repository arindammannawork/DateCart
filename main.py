from fastapi import FastAPI,Request,Header,Depends
from config import *
from helper.helper_funtions import *
from routes.auth import router as auth_router 
from routes.todo import router as todo_router 
import fnmatch



# Create a new client and connect to the server



app = FastAPI()
# Allow CORS for Swagger testing if needed

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(todo_router, prefix="/api/todo", tags=["todo"],dependencies=[Depends(get_token_headers)],responses={404:{"des":"Not Found"}})



@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

