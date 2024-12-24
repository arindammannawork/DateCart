from pydantic import BaseModel,EmailStr

class user_model(BaseModel):
    fullName: str|None=None
    username: str|None=None
    email: EmailStr
    password: str