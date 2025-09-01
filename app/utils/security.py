# app/utils/security.py

import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional

# FastAPI 관련 임포트
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

# .env 파일 등에서 SECRET_KEY와 만료 시간을 가져옵니다.
from ..core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from ..models import User
from ..models.token_blacklist import TokenBlacklist

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 스키마 정의 (FastAPI의 Depends에 사용)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 모든 토큰의 유효성을 검증하는 단일 함수
def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# 토큰의 유효성을 검사하고, 블랙리스트를 확인한 후 사용자 정보를 반환합니다.
async def get_user_from_token(token: str) -> Optional[User]:
    payload = verify_token(token)
    if payload is None:
        return None

    # 블랙리스트에 등록된 토큰인지 확인
    jti = payload.get("jti")
    if jti is None or await TokenBlacklist.get_or_none(jti=jti):
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    try:
        user = await User.get(id=user_id)
        return user
    except DoesNotExist:
        return None


# **새로 추가된 함수**
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
