from typing import List, Optional
from fastapi import HTTPException, status

from app.models import User
from app.models.diary import Diary, EmotionalState
from app.schemas.diary import DiaryCreate, DiaryUpdate
from tortoise.contrib.pydantic import pydantic_model_creator


# Pydantic 모델 정의
# 이 파일에서 모든 모델 관련 작업을 처리합니다.
Diary_Pydantic = pydantic_model_creator(Diary, name="Diary")
DiaryIn_Pydantic = pydantic_model_creator(Diary, name="DiaryIn", exclude_readonly=True)


async def create_diary_service(user: User, diary_data: DiaryCreate):
    """
    새 일기를 생성합니다. user_id 대신 User 객체를 직접 사용합니다.
    """
    try:
        new_diary = await Diary.create(
            user=user,  # Foreign Key 관계에 따라 User 객체 자체를 할당합니다.
            title=diary_data.title,
            content=diary_data.content,
            emotional_state=diary_data.emotional_state,
        )
        return new_diary
    except Exception as e:
        print(f"일기 생성 중 오류 발생: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="일기 생성 중 알 수 없는 오류가 발생했습니다."
        )



async def get_all_diaries_service(user_id: int) -> List[Diary_Pydantic]:
    """
    사용자의 모든 일기 목록을 조회합니다.
    """
    diaries = await Diary.filter(user_id=user_id).order_by("-created_at")
    return [await Diary_Pydantic.from_tortoise_orm(d) for d in diaries]


async def get_diary_by_id_service(diary_id: int, user_id: int) -> Diary_Pydantic:
    """
    특정 일기를 조회합니다.
    """
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다."
        )
    return await Diary_Pydantic.from_tortoise_orm(diary)


async def update_diary_service(diary_id: int, diary_data: DiaryUpdate, user_id: int) -> Diary_Pydantic:
    """
    일기를 수정합니다.
    """
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다."
        )

    # `exclude_unset=True`를 사용해 제공된 필드만 업데이트합니다.
    await diary.update_from_dict(diary_data.model_dump(exclude_unset=True)).save()

    return await Diary_Pydantic.from_tortoise_orm(diary)


async def delete_diary_service(diary_id: int, user_id: int):
    """
    일기를 삭제합니다.
    """
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다."
        )
    await diary.delete()
