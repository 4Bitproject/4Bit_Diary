# schemas.py
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    """
    회원가입 시 사용자로부터 입력받을 정보를 정의합니다.
    """

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    로그인 시 사용자로부터 입력받을 정보를 정의합니다.
    """

    email: EmailStr
    password: str
