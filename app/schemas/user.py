# app/schemas/user.py

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: str


# 추가적인 스키마들은 여기에 유지하세요.
class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    password: str
    is_active: bool = True
    is_verified: bool = False
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None


class UserInDB(UserSchema):
    hashed_password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    name: Optional[str] = None

class UpdateProfileRequest(BaseModel):
    new_data: UserUpdate