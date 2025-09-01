from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class DiaryCreate(BaseModel):
    title: str
    content: str

    emotional_state: str
    tags: Optional[List[str]] = (
        []
    )  # 태그 필드를 추가하여 리스트 형식의 문자열을 허용합니다.


class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    emotional_state: EmotionalState | None = None
    tags: Optional[List[str]] = []


class DiaryOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    emotional_state: EmotionalState
    ai_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DiarySearchParams(BaseModel):
    """일기 검색 파라미터"""

    title: Optional[str] = None  # 제목 검색
    tags: Optional[List[str]] = None  # 태그 검색 (태그 이름 리스트)
    start_date: Optional[date] = None  # 시작 날짜
    end_date: Optional[date] = None  # 종료 날짜
