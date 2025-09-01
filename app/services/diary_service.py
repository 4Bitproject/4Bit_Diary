from typing import List

from fastapi import HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User
from app.models.diary import Diary
from app.models.tag import Tag
from app.schemas.diary import DiaryCreate, DiaryUpdate
from app.services.ai_service import GeminiService

# Pydantic 모델 정의
# 이 파일에서 모든 모델 관련 작업을 처리합니다.
Diary_Pydantic = pydantic_model_creator(Diary, name="Diary")
DiaryIn_Pydantic = pydantic_model_creator(Diary, name="DiaryIn", exclude_readonly=True)


async def create_diary_service(user: User, diary_data: DiaryCreate):
    try:
        # 1. tags를 제외하고 Diary 인스턴스를 먼저 생성합니다.
        new_diary = await Diary.create(
            user=user,
            title=diary_data.title,
            content=diary_data.content,
            emotional_state=diary_data.emotional_state,  # ai_summary 필드도 추가
        )

        # 태그 처리
        if diary_data.tags:
            for tag_name in diary_data.tags:
                # 태그가 없으면 생성, 있으면 가져오기
                tag, _ = await Tag.get_or_create(name=tag_name)
                await new_diary.tags.add(tag)

        # 태그 관계 포함해서 반환
        await new_diary.fetch_related("tags")

        return new_diary
    except Exception as e:

        print(f"일기 생성 중 오류 발생: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="일기 생성 중 알 수 없는 오류가 발생했습니다.",
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
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    return await Diary_Pydantic.from_tortoise_orm(diary)


async def update_diary_service(
    diary_id: int, diary_data: DiaryUpdate, user_id: int
) -> Diary_Pydantic:
    """
    일기를 수정합니다.
    """
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )

    # `exclude_unset=True`를 사용해 제공된 필드만 업데이트합니다.
    await diary.update_from_dict(diary_data.model_dump(exclude_unset=True)).save()

    return await Diary_Pydantic.from_tortoise_orm(diary)


async def summarize_diary_service(diary_id: int, user_id: int) -> Diary:
    """
    일기 AI 요약 서비스
    """
    # 일기 조회 및 권한 확인
    diary = await Diary.filter(id=diary_id, user_id=user_id).first()

    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다."
        )

    # 이미 요약이 있는 경우 확인
    if diary.ai_summary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 요약이 존재합니다."
        )

    try:
        # Gemini 서비스로 요약 생성
        gemini_service = GeminiService()
        summary = await gemini_service.summarize_diary(diary.content)

        # 요약 저장
        diary.ai_summary = summary
        await diary.save()

        return diary

    except Exception as e:
        print(f"요약 생성 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI 요약 생성에 실패했습니다.",
        )


async def delete_diary_service(diary_id: int, user_id: int):
    """
    일기를 삭제합니다.
    """
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    await diary.delete()
