from fastapi import FastAPI,Depends,Request
# from config import *
import time
from helper.helper_funtions import *
from routes.auth import router as auth_router 
from routes.bankNote import router as todo_router 
import torch
print(torch.cuda.is_available()) 


# Create a new client and connect to the server
app = FastAPI()


app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(todo_router, prefix="/api/banknote", tags=["BankNote"], dependencies=[Depends(get_token_headers)],responses={12:{ "status":status.HTTP_404_NOT_FOUND}})
# app.include_router(todo_router, prefix="/api/todo", tags=["todo"],dependencies=[Depends(get_token_headers)],responses={404:{"des":"Not Found"}})

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
@app.get("/")
async def root():
    return {"message": "Welcome to the PI!"}


