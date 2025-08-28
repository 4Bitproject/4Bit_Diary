# app/services/user_service.py

from typing import Optional

from fastapi import Depends
from fastapi_users import BaseUserManager

from app.core.config import settings
from app.models.user import UserInDB


# `auth_service`에서 `user_db`를 직접 가져오는 대신, 의존성 주입을 통해 전달받습니다.
class UserManager(BaseUserManager[UserInDB, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_register(self, user: UserInDB, request: Optional[dict] = None):
        print(f"사용자 {user.email}가 등록되었습니다.")


def get_user_manager(user_db=Depends()):
    yield UserManager(user_db)
