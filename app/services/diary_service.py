from typing import Optional
from tortoise import fields
from app.models.diary import Diary, Diary_Pydantic, EmotionalState


class DiaryService:
    async def create(
        self,
        user_id: int,
        title: str,
        content: str,
        emotional_state: EmotionalState,
        ai_summary: Optional[str] = None,
    ):
        # created_at, updated_at 필드는 Tortoise ORM이 자동으로 채워줍니다.
        diary = await Diary.create(
            user_id=user_id,
            title=title,
            content=content,
            emotional_state=emotional_state,
            ai_summary=ai_summary,
        )
        return await Diary_Pydantic.from_tortoise_orm(diary)

    async def get(self, diary_id: int):
        diary = await Diary.get_or_none(id=diary_id)
        if diary:
            return await Diary_Pydantic.from_tortoise_orm(diary)
        return None

    async def list(self, search: Optional[str] = None, sort_by: str = "created_at"):
        query = Diary.all()
        if search:
            query = query.filter(title__icontains=search)
        query = query.order_by(sort_by)
        return await Diary_Pydantic.from_queryset(query)

    async def update(self, diary_id: int, data: dict):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            return None
        await diary.update_from_dict(data)
        await diary.save()
        return await Diary_Pydantic.from_tortoise_orm(diary)

    async def delete(self, diary_id: int):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            return False
        await diary.delete()
        return True


async def create_diary_service(user_id: int, diary_data: dict):
    try:
        # created_at과 updated_at을 인자로 전달하지 않습니다.
        # Tortoise ORM이 자동으로 처리합니다.
        new_diary = await Diary.create(
            user_id=user_id,
            title=diary_data["title"],
            content=diary_data["content"],
            emotional_state=diary_data["emotional_state"],
        )
        return {"message": "일기 생성 성공", "diary_id": str(new_diary.id)}
    except Exception as e:
        return {"error": f"일기 생성 중 오류 발생: {e}"}


async def get_diaries_service(user_id: int):
    try:
        # created_date를 created_at으로 수정합니다.
        diaries = await Diary.filter(user_id=user_id).order_by("-created_at")
        return [
            {
                "id": d.id,
                "title": d.title,
                "content": d.content,
                "emotional_state": d.emotional_state,
            }
            for d in diaries
        ]
    except Exception as e:
        return {"error": f"일기 조회 중 오류 발생: {e}"}
