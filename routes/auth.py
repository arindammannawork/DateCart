from fastapi import APIRouter, Request,HTTPException,Header,Depends,status
from typing import Annotated
from schema import User_model
from helper.helper_funtions import *
from db import db

# Create a router for authentication routes
router = APIRouter()

@router.post("/login")
async def login(login_credentials:User_model ):
    # Authentication logic here
    user=  db.users.find_one({"email":login_credentials.email})
    user=convert_objectid(user)
    if not user:
        return {"message": "Email is not Registered","status_code":status.HTTP_404_NOT_FOUND }
    if not verify_password(login_credentials.password, user["password"]):
        return {"message": "Incorrect password","status_code":status.HTTP_400_BAD_REQUEST }

    # Generate JWT token here
    token = create_access_token(data={"email": user["email"],})
    # return {"access_token": token, "token_type": "bearer"}
    return {"message": "Login successful", "token": f"Bearer {token}" ,"status_code":status.HTTP_200_OK}

@router.post("/register")
async def register(register_credentials:User_model):
    # Registration logic here
    user= db.users.find_one({"email":register_credentials.email})
    if user:
        return {"message": "Email already registered","status_code":status.HTTP_400_BAD_REQUEST }
    register_credentials.password = get_password_hash( register_credentials.password )

    try:
        db.users.insert_one(dict(register_credentials))
        # Generate JWT token here
        token = create_access_token(data={"email": register_credentials.email})
        return {"message": "User registered successfully","token": f"Barear {token}", "user":register_credentials,"status_code":status.HTTP_201_CREATED }
    except Exception as e:
        return {"message": f"Error registering user: {e}","status_code":status.HTTP_500_INTERNAL_SERVER_ERROR}


@router.get("/verifyuser")
async def verify_user(payload:dict=Depends(get_token_headers)):
    return {"message": "User verified successfully","payload":payload ,"status_code":status.HTTP_200_OK}
