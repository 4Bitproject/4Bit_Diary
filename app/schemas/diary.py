from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

EmotionalStateLiteral = Literal[
    "neutral", "happy", "sad", "angry", "anxious", "excited"
]


class DiaryBase(BaseModel):
    title: str
    content: str
    emotional_state: str
    ai_summary: Optional[str] = None


class DiaryCreate(DiaryBase):
    user_id: int


class DiaryUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    emotional_state: Optional[str]
    ai_summary: Optional[str]


class DiaryOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    emotional_state: str
    ai_summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # ORM 객체 바로 변환
