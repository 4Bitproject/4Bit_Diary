from datetime import datetime
from typing import Optional

from app.models.diary import Diary
from app.schemas.diary import DiaryOut


class SearchService:
    async def search_diary(
        self,
        user_id: int,
        query: str,
        search_type: str = "all",
        target_date: Optional[datetime] = None,
    ) -> list[DiaryOut]:
        """
        일기 검색 (제목, 내용, 태그)
        """
        base_query = Diary.filter(user_id=user_id).prefetch_related("tags")

        results = []

        if search_type == "title":
            results = await base_query.filter(title__icontains=query)
        elif search_type == "content":
            results = await base_query.filter(content__icontains=query)
        elif search_type == "tag":
            results = await base_query.filter(tags__name__icontains=query)
        elif search_type == "date":
            if not target_date:
                return []
            start_of_day = target_date.replace(hour=0, minute=0, second=0)
            end_of_day = target_date.replace(hour=23, minute=59, second=59)
            results = await base_query.filter(
                created_at__gte=start_of_day, created_at__lte=end_of_day
            )

        return [DiaryOut.model_validate(diary) for diary in results]
