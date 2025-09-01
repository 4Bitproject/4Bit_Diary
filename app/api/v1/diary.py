from typing import List

from fastapi import APIRouter, Depends, status

from app.api.v1.auth import get_current_user
from app.models.diary import Diary_Pydantic as DiaryOut
from app.models.diary import DiaryIn_Pydantic as DiaryIn
from app.models.user import User
from app.schemas.diary import DiaryUpdate
from app.services.diary_service import (
    create_diary_service,
    delete_diary_service,
    get_all_diaries_service,
    get_diary_by_id_service,
    update_diary_service,
)

router = APIRouter(prefix="/api/v1/diary", tags=["diary"])


# 일기 생성
@router.post("/create", response_model=DiaryOut)
async def create_new_diary(
    diary_in: DiaryIn, current_user: User = Depends(get_current_user)
):
    # 서비스 함수에 Pydantic 모델과 User 객체를 직접 전달합니다.
    new_diary = await create_diary_service(current_user, diary_in)
    return await DiaryOut.from_tortoise_orm(new_diary)


# 모든 일기 조회
@router.get("/inquiry", response_model=List[DiaryOut])
async def get_diaries(current_user: User = Depends(get_current_user)):
    return await get_all_diaries_service(current_user.id)


# 특정 일기 조회
@router.get("/{diary_id}", response_model=DiaryOut)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    return await get_diary_by_id_service(diary_id, current_user.id)


# 일기 수정
@router.put("/{diary_id}", response_model=DiaryOut)
async def update_diary(
    diary_id: int, data: DiaryUpdate, current_user: User = Depends(get_current_user)
):
    return await update_diary_service(diary_id, data, current_user.id)


# 일기 삭제
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    await delete_diary_service(diary_id, current_user.id)
    return {"message": "일기가 성공적으로 삭제되었습니다."}
