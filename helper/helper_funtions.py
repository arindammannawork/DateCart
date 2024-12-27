from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException,status,Header,Depends
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
# from config import *
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials








def convert_objectid(doc):
    if doc:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)







def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=os.getenv("ACCESS_TOKEN_EXPIRE_HOURS"))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,os.getenv("SECRET_KEY") , algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


# Define HTTPBearer for JWT Token
security = HTTPBearer()

# Dependency to extract and verify the token
def get_token_headers(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract the token
    return verify_jwt_token(token)
    
def verify_jwt_token(jwt_token):
    try:
        if not jwt_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="jwt_token header missing")
        # if not jwt_token.startswith("Bearer "):
        #     print(jwt_token)
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid jwt_token header format",token=jwt_token)
        # token=jwt_token.split(" ")[1]  # Extract the token after "Bearer "
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail= f"Invalid token {e}") from e
    

