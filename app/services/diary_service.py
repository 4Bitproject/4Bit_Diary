from typing import List, Optional
from app.models.diaries import Diary, Diary_Pydantic, DiaryIn_Pydantic, EmotionalState

class DiaryService:
    async def create(self, user_id: int, title: str, content: str, emotional_state: EmotionalState, ai_summary: Optional[str] = None):
        diary = await Diary.create(
            user_id=user_id,
            title=title,
            content=content,
            emotional_state=emotional_state,
            ai_summary=ai_summary
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
