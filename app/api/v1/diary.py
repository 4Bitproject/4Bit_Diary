# app/api/v1/diary.py
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

# NOTE: .models.models -> .models.user 로 변경
from ...models.user import User
from ...services.diary_service import (
    DiaryService,
    create_diary_service,
)
from ...services.search_service import SearchService
from ...utils.security import get_user_from_token

router = APIRouter()


async def get_current_user(token: str):
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 실패"
        )
    return user


@router.post("/diary/create", tags=["diary"])
async def create_new_diary(
    diary_data: dict, current_user: User = Depends(get_current_user)
):
    result = await create_diary_service(current_user.id, diary_data)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return result


@router.get("/diary", tags=["diary"])
async def get_all_diaries(
    current_user: User = Depends(get_current_user),
    search: Optional[str] = None,
    search_type: str = "all",
    target_date: Optional[datetime] = None,
):
    diary_service = DiaryService()
    search_service = SearchService()
    # 검색 파라미터 있으면 검색 결과
    if search or search_type == "date":
        return await search_service.search_diary(
            current_user.id, search, search_type, target_date
        )

    # 파라미터 없으면 전체 목록
    return await diary_service.list(current_user.id)
