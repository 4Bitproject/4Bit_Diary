# app/api/v1/diary.py


from fastapi import APIRouter, Depends, HTTPException, status

# NOTE: .models.models -> .models.user 로 변경
from ...models.user import User
from ...services.diary_service import create_diary_service, get_diaries_service
from ...utils.security import get_user_from_token

router = APIRouter()


async def get_current_user(token: str):
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 실패"
        )
    return user


@router.post("/diaries", tags=["diary"])
async def create_new_diary(
    diary_data: dict, current_user: User = Depends(get_current_user)
):
    result = await create_diary_service(current_user.id, diary_data)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.get("/diaries", tags=["diary"])
async def get_all_diaries(current_user: User = Depends(get_current_user)):
    result = await get_diaries_service(current_user.id)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result
