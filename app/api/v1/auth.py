from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate):
    try:
        user = await auth_service.register_user(user_data)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login")
async def login(user_data: UserLogin):
    user = await auth_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # TODO: JWT 토큰 생성 및 반환 로직 추가
    return {"message": "Login successful"}

@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}