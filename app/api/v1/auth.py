from datetime import timedelta

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from ...core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from ...models.user import User
from ...schemas.user import UserIn, UserResponse
from ...services.auth_service import (
    delete_user_service,
    is_token_revoked,
    login_user_service,
    logout_user_service,
    register_user_service,
    update_user_profile_service,
)
from ...utils.security import (
    create_access_token,
    get_user_from_token,
    verify_token,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class UpdateProfileRequest(BaseModel):
    new_data: dict


@router.post("/register", tags=["auth"])
async def register(user_in: UserIn):
    result = await register_user_service(user_in.dict())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/login", tags=["auth"])
async def login(user_in: UserIn):
    result = await login_user_service(user_in.dict())
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/logout", status_code=status.HTTP_200_OK, tags=["auth"])
async def logout(token: str = Query(...)):
    return await logout_user_service(token)


@router.get("/profile", response_model=UserResponse, tags=["auth"])
async def get_user_profile(token: str = Query(...)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    jti = payload.get("jti")
    if await is_token_revoked(jti):
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="인증 실패")

    return {
        "id": str(user.id),
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }


@router.put("/profile", tags=["auth"])
async def update_profile(request: UpdateProfileRequest, token: str = Query(...)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    jti = payload.get("jti")
    if await is_token_revoked(jti):
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="인증 실패")

    result = await update_user_profile_service(user.id, request.new_data)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.delete("/profile", tags=["auth"])
async def delete_profile(token: str = Query(...)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    jti = payload.get("jti")
    if await is_token_revoked(jti):
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="인증 실패")

    result = await delete_user_service(user.id)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.post("/refresh", tags=["auth"])
async def refresh_token(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        if not jti or await is_token_revoked(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이미 로그아웃된 토큰이거나 잘못된 토큰 형식입니다.",
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 리프레시 토큰입니다.",
            )

        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="사용자를 찾을 수 없습니다.",
            )

        new_access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 리프레시 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str):
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 실패"
        )
    return user
