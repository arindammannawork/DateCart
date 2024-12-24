from fastapi import APIRouter

from schema import user_model
from helper.helper_funtions import *
from db import db

# Create a router for authentication routes
router = APIRouter()

@router.post("/login")
async def login(login_credentials:user_model ):
    # Authentication logic here
    user=  db.users.find_one({"email":login_credentials.email})
    user=convert_objectid(user)
    if not user:
        return {"message": "Email is not Registered" }
    if not verify_password(login_credentials.password, user["password"]):
        return {"message": "Incorrect password" }

    # Generate JWT token here
    # token = create_access_token(data={"sub": user.email})
    # return {"access_token": token, "token_type": "bearer"}
    return {"message": "Login successful", "email": user}

@router.post("/register")
async def register(register_credentials:user_model):
    # Registration logic here
    user= db.users.find_one({"email":register_credentials.email})
    if user:
        return {"message": "Email already registered" }
    register_credentials.password = get_password_hash( register_credentials.password )

    try:
        db.users.insert_one(dict(register_credentials))
        return {"message": "User registered successfully", "user":register_credentials }
    except Exception as e:
        return {"message": f"Error registering user: {e}"}


@router.post("/verifyuser")
async def verifyuser(email: str, password: str):
    # Registration logic here
    return {"message": "User registered successfully", "email": email}
