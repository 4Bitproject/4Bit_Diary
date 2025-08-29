from datetime import datetime

from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"

class DiaryCreate(BaseModel):
    title: str
    content: str
    emotional_state: str
    tags: List[str]  # 태그 필드를 추가하여 리스트 형식의 문자열을 허용합니다.


class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    emotional_state: EmotionalState | None = None


class DiaryOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    emotional_state: EmotionalState
    ai_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime