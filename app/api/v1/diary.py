from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from app.services.diary_service import (
    create_diary_service,
    get_diaries_service,
    delete_diary_service,
    update_diary_service,
)

router = APIRouter(prefix="/diaries", tags=["diaries"])

# 사용자 인증 예시 (실제 auth 모듈과 연동 필요)
async def get_current_user_id():
    # 예시: 임시로 고정 user_id 반환
    return "user_1"


# 일기 생성
@router.post("/", response_model=Dict)
async def create_diary(diary_data: Dict, user_id: str = Depends(get_current_user_id)):
    result = await create_diary_service(user_id, diary_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# 일기 목록 조회
@router.get("/", response_model=List[Dict])
async def get_diaries(user_id: str = Depends(get_current_user_id)):
    result = await get_diaries_service(user_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# 일기 삭제
@router.delete("/{diary_id}", response_model=Dict)
async def delete_diary(diary_id: str):
    result = await delete_diary_service(diary_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# 일기 수정
@router.put("/{diary_id}", response_model=Dict)
async def update_diary(diary_id: str, diary_data: Dict):
    result = await update_diary_service(diary_id, diary_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
