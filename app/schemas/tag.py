from typing import List, Optional

from pydantic import BaseModel


# 태그 수정 요청 (PATCH /api/tags/{id}/)
class TagPatchRequest(BaseModel):
    name: Optional[str] = None


# 태그 목록용 응답 (GET /api/tags/)
class TagInList(BaseModel):
    tag_id: int
    name: str
    usage_count: int


# 최근 일기 정보 (특정 태그 조회용)
class RecentDiary(BaseModel):
    diary_id: int
    title: str
    created_at: str


# 특정 태그 조회 응답 (GET /api/tags/{id}/)
class TagDetailData(BaseModel):
    tag_id: int
    name: str
    usage_count: int
    recent_diaries: List[RecentDiary]


# API 응답 래퍼
class TagListResponse(BaseModel):
    data: dict


class TagDetailResponse(BaseModel):
    data: TagDetailData


# DELETE 응답용
class TagDeleteResponse(BaseModel):
    message: str
