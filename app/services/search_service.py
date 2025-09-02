from datetime import date, datetime
from typing import List, Optional

from app.models.diary import Diary


async def search_diary(
    user_id: int,
    search_type: str,
    query: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Diary]:
    """
    일기 검색 (제목,태그,날짜)
    """
    base_query = Diary.filter(user_id=user_id).prefetch_related("tags")

    if search_type == "title":
        if query and query.strip():  # 검색어가 있을 때만 필터링
            results = await base_query.filter(title__icontains=query).order_by(
                "-created_at"
            )
        else:
            results = await base_query.order_by("-created_at")  # 전체 반환

    elif search_type == "tag":
        if query and query.strip():  # 검색어가 있을 때만 필터링
            results = (
                await base_query.filter(tags__name__icontains=query)
                .distinct()
                .order_by("-created_at")
            )
        else:
            results = await base_query.order_by("-created_at")  # 전체 반환

    elif search_type == "date":
        if not start_date:
            return []

        # 시작 날짜만 있으면 그 날 하루 검색
        if not end_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(start_date, datetime.max.time())
        else:
            # 범위 검색
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())

        results = await base_query.filter(
            created_at__gte=start_datetime, created_at__lte=end_datetime
        ).order_by("-created_at")

    else:
        return []

    return results
