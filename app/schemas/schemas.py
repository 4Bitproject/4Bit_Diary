# schemas.py
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
