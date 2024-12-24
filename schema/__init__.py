from pydantic import BaseModel,EmailStr

class user_model(BaseModel):
    username: str | None
    fullName: str | None
    email: EmailStr
    password: str