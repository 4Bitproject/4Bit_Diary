# app/services/diary_service.py

from typing import List
from fastapi import HTTPException, status

from app.models import User
from app.models.diary import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryOut
from app.models.tag import Tag


async def create_diary_service(user: User, diary_data: DiaryCreate) -> Diary:
    try:
        # Diary 인스턴스를 먼저 생성합니다.
        new_diary = await Diary.create(
            user=user,
            title=diary_data.title,
            content=diary_data.content,
            emotional_state=diary_data.emotional_state,
            ai_summary=diary_data.ai_summary,
        )

        # 태그가 있으면 태그를 처리합니다.
        if diary_data.tags:
            tag_list = []
            for tag_name in diary_data.tags:
                tag, _ = await Tag.get_or_create(name=tag_name)
                tag_list.append(tag)
            # 생성된 Tag 객체들을 일기에 추가합니다.
            await new_diary.tags.add(*tag_list)

        # 태그 관계를 포함하여 반환
        return await new_diary.fetch_related("tags")

    except Exception as e:
        print(f"일기 생성 중 오류 발생: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="일기 생성 중 알 수 없는 오류가 발생했습니다.",
        )


async def get_all_diaries_service(user_id: int) -> List[DiaryOut]:
    diaries = await Diary.filter(user_id=user_id).order_by("-created_at")
    return [DiaryOut.model_validate(d) for d in diaries]


async def get_diary_by_id_service(diary_id: int, user_id: int) -> DiaryOut:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    return DiaryOut.model_validate(diary)


async def update_diary_service(
    diary_id: int, diary_data: DiaryUpdate, user_id: int
) -> DiaryOut:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    await diary.update_from_dict(diary_data.model_dump(exclude_unset=True)).save()
    return DiaryOut.model_validate(diary)


async def delete_diary_service(diary_id: int, user_id: int):
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    await diary.delete()