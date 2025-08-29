from typing import List

from fastapi import APIRouter, HTTPException

from app.models.diary import Diary
from app.schemas.diary import (
    DiaryCreate,
    DiaryOut,
    DiaryUpdate,
)
from app.services.diary_service import DiaryService

router = APIRouter(prefix="/diaries", tags=["diaries"])
service = DiaryService()


@router.post("/", response_model=DiaryOut)
async def create_diary(diary_create: DiaryCreate):
    from app.models import User

    user = await User.get_or_none(id=diary_create.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    diary = await Diary.create(**diary_create.model_dump())
    return DiaryOut.model_validate(diary)

router = APIRouter(prefix="/diary", tags=["Diary"])

# 유저 인증 데코레이터 가정: get_current_user
async def get_current_user():
    return 1  # 테스트용, 실제로는 JWT나 세션에서 유저 id 가져오기

@router.post("/", response_model=dict)
async def create_diary_endpoint(data: DiaryCreate, user_id: int = Depends(get_current_user)):
    return await create_diary(user_id, data)

@router.put("/{diary_id}", response_model=dict)
async def update_diary_endpoint(diary_id: int, data: DiaryUpdate):
    return await update_diary(diary_id, data)

@router.delete("/{diary_id}")
async def delete_diary_endpoint(diary_id: int):
    return await delete_diary(diary_id)

@router.get("/{diary_id}", response_model=dict)
async def get_diary_endpoint(diary_id: int):
    return await get_diary(diary_id)

@router.post("/list", response_model=List[dict])
async def list_diaries_endpoint(filters: DiaryFilter, user_id: int = Depends(get_current_user)):
    return await list_diaries(user_id, filters.dict())
