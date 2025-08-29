from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"

class DiaryCreate(BaseModel):
    title: str
    content: str
    emotional_state: EmotionalState
    tags: Optional[List[str]] = []

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    emotional_state: Optional[EmotionalState] = None
    tags: Optional[List[str]] = None

class DiaryFilter(BaseModel):
    keyword: Optional[str] = None
    emotional_state: Optional[EmotionalState] = None
    tags: Optional[List[str]] = None
