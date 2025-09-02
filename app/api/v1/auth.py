from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.utils.security import http_bearer

from ...core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from ...models.user import User
from ...schemas.user import UserIn, UserLogin, UserResponse, UserUpdate
from ...services.auth_service import (
    delete_user_service,
    login_user_service,
    logout_user_service,
    register_user_service,
    update_user_profile_service,
)
from ...utils.security import (
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/api/v1", tags=["auth"])


class UpdateProfileRequest(BaseModel):
    new_data: UserUpdate


@router.post("/register", tags=["auth"])
async def register(user_in: UserIn):
    result = await register_user_service(user_in.model_dump())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/login", tags=["auth"])
async def login(user_in: UserLogin):
    result = await login_user_service(user_in.model_dump())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/logout", status_code=status.HTTP_200_OK, tags=["auth"])
async def logout(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await logout_user_service(credentials.credentials)


@router.get("/profile", response_model=UserResponse, tags=["auth"])
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }


@router.put("/profile", tags=["auth"])
async def update_profile(
    request: UpdateProfileRequest, current_user: User = Depends(get_current_user)
):
    result = await update_user_profile_service(current_user.id, request.new_data)
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


@router.post("/refresh", tags=["auth"])
async def refresh_token(current_user: User = Depends(get_current_user)):
    # 현재 사용자로부터 새로운 액세스 토큰 생성
    new_access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": new_access_token, "token_type": "bearer"}
