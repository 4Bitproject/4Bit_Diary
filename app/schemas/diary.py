from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class DiaryCreate(BaseModel):
    title: str
    content: str
    emotional_state: EmotionalState  # str -> EmotionalState
    tags: Optional[List[str]] = []
    ai_summary: Optional[str] = None

class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    emotional_state: EmotionalState | None = None
    tags: Optional[List[str]] = []


class DiaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    emotional_state: EmotionalState
    ai_summary: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def extract_tag_names(cls, v):
        if hasattr(v, "__iter__") and not isinstance(v, str):
            try:
                tag_list = list(v)
                if tag_list and hasattr(tag_list[0], "name"):
                    return [tag.name for tag in tag_list]
            except Exception:
                # fetch_related 안 된 경우 빈 리스트 반환
                return []
        return v if isinstance(v, list) else []


class DiarySearchParams(BaseModel):
    """일기 검색 파라미터"""

    title: Optional[str] = None  # 제목 검색
    tags: Optional[List[str]] = None  # 태그 검색 (태그 이름 리스트)
    start_date: Optional[date] = None  # 시작 날짜
    end_date: Optional[date] = None  # 종료 날짜
