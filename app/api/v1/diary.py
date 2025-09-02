from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.v1.auth import get_current_user
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryOut, DiaryUpdate
from app.services.diary_service import (
    create_diary_service,
    delete_diary_service,
    get_all_diaries_service,
    get_diary_by_id_service,
    summarize_diary_service,
    update_diary_service,
)
from app.services.search_service import search_diary

router = APIRouter(prefix="/api/v1/diary", tags=["diary"])


# 일기 생성
@router.post("/create", response_model=DiaryOut)
async def create_new_diary(
    diary_data: DiaryCreate,
    current_user: User = Depends(get_current_user),
):
    new_diary_orm = await create_diary_service(current_user, diary_data)

    return DiaryOut.model_validate(new_diary_orm)


# 모든 일기 조회
@router.get("/inquiry", response_model=List[DiaryOut])
async def get_diaries(current_user: User = Depends(get_current_user)):
    return await get_all_diaries_service(current_user.id)


# 일기 검색
@router.get("/search", response_model=List[DiaryOut])
async def search_diaries(
    search_type: str = Query(..., description="검색 타입: title, tag, date"),
    query: Optional[str] = Query(None, description="검색어 (title, tag 검색 시)"),
    start_date: Optional[date] = Query(None, description="시작 날짜 (date 검색 시)"),
    end_date: Optional[date] = Query(
        None, description="종료 날짜 (date 검색 시, 선택사항)"
    ),
    current_user: User = Depends(get_current_user),
):
    diaries = await search_diary(
        user_id=current_user.id,
        search_type=search_type,
        query=query,
        start_date=start_date,
        end_date=end_date,
    )

    return [DiaryOut.model_validate(diary) for diary in diaries]


# 특정 일기 조회
@router.get("/{diary_id}", response_model=DiaryOut)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    """
    diary_id 를 입력하면 조회해 주는 기능
    """
    return await get_diary_by_id_service(diary_id, current_user.id)


# 일기 AI 요약 생성
@router.post("/{diary_id}/summarize", response_model=DiaryOut)
async def summarize_diary(
    diary_id: int, current_user: User = Depends(get_current_user)
):
    """
    일기 AI 요약 생성

    - 일기 내용을 AI로 분석하여 2-3문장으로 요약
    - 이미 요약이 있는 경우 400 에러 반환
    """
    diary = await summarize_diary_service(diary_id, current_user.id)
    return DiaryOut.model_validate(diary)


# 일기 수정
@router.put("/{diary_id}", response_model=DiaryOut)
async def update_diary(
    diary_id: int, data: DiaryUpdate, current_user: User = Depends(get_current_user)
):
    return await update_diary_service(diary_id, data, current_user.id)


# 일기 삭제
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    await delete_diary_service(diary_id, current_user.id)
    return {"message": "일기가 성공적으로 삭제되었습니다."}
