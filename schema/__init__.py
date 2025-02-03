from pydantic import BaseModel,EmailStr

class User_model(BaseModel):
    fullName: str|None=None
    username: str|None=None
    email: EmailStr
    password: str