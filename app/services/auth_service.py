from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist, IntegrityError

from ..core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from ..models import User
from ..models.token_blacklist import TokenBlacklist
from ..utils.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)


async def register_user_service(user_data: dict):
    try:
        hashed_password = hash_password(user_data["password"])
        new_user = await User.create(
            email=user_data["email"],
            password=hashed_password,
            nickname=user_data["nickname"],
            name=user_data["name"],
        )
        return {"message": "회원가입이 완료되었습니다.", "user_id": str(new_user.id)}
    except IntegrityError:
        return {"error": "이미 존재하는 이메일입니다."}
    except ValidationError as e:
        return {"error": "유효성 검사 실패", "details": e.errors()}
    except Exception as e:
        return {"error": f"알 수 없는 오류 발생: {e}"}


async def login_user_service(user_data: dict):
    try:
        user = await User.get_or_none(email=user_data["email"])
        if not user or not verify_password(user_data["password"], user.password):
            return {"error": "이메일 또는 비밀번호가 잘못되었습니다."}

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except Exception as e:
        return {"error": f"로그인 중 오류 발생: {e}"}


async def logout_user_service(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if jti:
            await TokenBlacklist.create(
                jti=jti, exp=datetime.fromtimestamp(payload.get("exp"))
            )
            return {"message": "로그아웃 성공"}
        return {"error": "유효하지 않은 토큰입니다."}
    except JWTError:
        return {"error": "유효하지 않은 토큰입니다."}
    except IntegrityError:
        return {"error": "이미 로그아웃된 토큰입니다."}
    except Exception as e:
        return {"error": f"로그아웃 중 오류 발생: {e}"}


async def is_token_revoked(jti: str) -> bool:
    token = await TokenBlacklist.get_or_none(jti=jti)
    return token is not None


async def get_user_profile_service(current_user_id: str) -> dict:
    try:
        user = await User.get(id=current_user_id)
        return {
            "user_id": str(user.id),
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }
    except DoesNotExist:
        return {"error": "사용자를 찾을 수 없습니다."}
    except Exception as e:
        return {"error": f"프로필 조회 중 오류 발생: {e}"}


async def update_user_profile_service(current_user_id: str, new_data: dict) -> dict:
    try:
        user = await User.get(id=current_user_id)

        if "email" in new_data:
            user.email = new_data["email"]

        if "password" in new_data:
            hashed_password = hash_password(new_data["password"])
            user.password = hashed_password

        await user.save()
        return {"message": "프로필이 성공적으로 업데이트되었습니다."}
    except DoesNotExist:
        return {"error": "사용자를 찾을 수 없습니다."}
    except IntegrityError:
        return {"error": "이미 존재하는 이메일입니다."}
    except Exception as e:
        return {"error": f"프로필 업데이트 중 오류 발생: {e}"}


async def delete_user_service(current_user_id: str) -> dict:
    try:
        user = await User.get(id=current_user_id)
        await user.delete()
        return {"message": "사용자가 성공적으로 삭제되었습니다."}
    except DoesNotExist:
        return {"error": "사용자를 찾을 수 없습니다."}
    except Exception as e:
        return {"error": f"사용자 삭제 중 오류 발생: {e}"}
