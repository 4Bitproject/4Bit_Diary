# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException, status

from ...models.user import User
from ...schemas.user import UserIn, UserLogin, UserResponse
from ...services.auth_service import (
    delete_user_service,
    login_user_service,
    register_user_service,
    update_user_profile_service,
)
from ...utils.security import get_user_from_token

router = APIRouter()


async def get_current_user(token: str):
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 실패"
        )
    return user


@router.post("/register", tags=["auth"])
async def register(user_in: UserIn):
    result = await register_user_service(user_in.dict())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/login", tags=["auth"])
async def login(user_in: UserLogin):
    result = await login_user_service(user_in.dict())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/logout", tags=["auth"])
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "로그아웃 성공"}


@router.get("/profile", response_model=UserResponse, tags=["auth"])
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }


@router.put("/profile", tags=["auth"])
async def update_profile(
    new_data: dict, current_user: User = Depends(get_current_user)
):
    result = await update_user_profile_service(current_user.id, new_data)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.delete("/profile", tags=["auth"])
async def delete_profile(current_user: User = Depends(get_current_user)):
    result = await delete_user_service(current_user.id)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result
