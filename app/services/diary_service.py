from typing import List
from tortoise.expressions import Q
from models.diary import Diary, DiaryTag, Diary_Pydantic, DiaryIn_Pydantic
from models.tag import Tag  # Tag 모델이 있다고 가정

async def create_diary(user_id: int, data):
    diary_obj = await Diary.create(
        user_id=user_id,
        title=data.title,
        content=data.content,
        emotional_state=data.emotional_state
    )

    # 태그 처리
    if data.tags:
        for tag_name in data.tags:
            tag_obj, _ = await Tag.get_or_create(name=tag_name)
            await DiaryTag.create(diary=diary_obj, tag=tag_obj)

    return await Diary_Pydantic.from_tortoise_orm(diary_obj)

async def update_diary(diary_id: int, data):
    diary_obj = await Diary.get(id=diary_id)
    diary_obj.title = data.title or diary_obj.title
    diary_obj.content = data.content or diary_obj.content
    diary_obj.emotional_state = data.emotional_state or diary_obj.emotional_state
    await diary_obj.save()

    if data.tags is not None:
        # 기존 태그 삭제
        await DiaryTag.filter(diary=diary_obj).delete()
        # 새 태그 생성
        for tag_name in data.tags:
            tag_obj, _ = await Tag.get_or_create(name=tag_name)
            await DiaryTag.create(diary=diary_obj, tag=tag_obj)

    return await Diary_Pydantic.from_tortoise_orm(diary_obj)

async def delete_diary(diary_id: int):
    diary_obj = await Diary.get(id=diary_id)
    await diary_obj.delete()
    return {"message": "Diary deleted"}

async def get_diary(diary_id: int):
    diary_obj = await Diary_Pydantic.from_queryset_single(Diary.get(id=diary_id))
    return diary_obj

async def list_diaries(user_id: int, filters: dict):
    query = Q(user_id=user_id)

    if filters.get("keyword"):
        query &= Q(title__icontains=filters["keyword"]) | Q(content__icontains=filters["keyword"])
    if filters.get("emotional_state"):
        query &= Q(emotional_state=filters["emotional_state"])
    if filters.get("tags"):
        query &= Q(diary_tags__tag__name__in=filters["tags"])

    diaries = await Diary_Pydantic.from_queryset(Diary.filter(query).distinct())
    return diaries
