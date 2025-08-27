from contextlib import asynccontextmanager
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import Tortoise, fields, models


# 1. Enum 클래스 정의
class EmotionType(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

# 2. Pydantic 스키마 정의
class EmotionKeywordBase(BaseModel):
    emotion_keyword: str
    emotion_type: EmotionType

class EmotionKeywordCreate(EmotionKeywordBase):
    pass

class EmotionKeywordUpdate(BaseModel):
    emotion_keyword: Optional[str] = None
    emotion_type: Optional[EmotionType] = None

class EmotionKeywordResponse(EmotionKeywordBase):
    id: int

    class Config:
        from_attributes = True

# 3. 모델 정의
class EmotionKeyword(models.Model):
    id = fields.IntField(pk=True)
    emotion_keyword = fields.CharField(max_length=50)
    emotion_type = fields.CharEnumField(enum_type=EmotionType, max_length=20)

    class Meta:
        table = "emotion_keyword"

# 4. lifespan 컨텍스트 관리자: DB 연결/해제 로직
@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    print("DB 연결 및 스키마 생성 완료")
    yield
    await Tortoise.close_connections()
    print("DB 연결 종료")

# 5. FastAPI 앱 인스턴스
app = FastAPI(lifespan=lifespan)

# 6. API 엔드포인트: Pydantic 스키마와 HTTPException 활용
@app.post("/emotion-keywords/", response_model=EmotionKeywordResponse, status_code=201)
async def create_emotion_keyword(emotion_keyword: EmotionKeywordCreate):
    emotion_keyword_obj = await EmotionKeyword.create(**emotion_keyword.dict())
    return emotion_keyword_obj

@app.get("/emotion-keywords/", response_model=List[EmotionKeywordResponse])
async def get_emotion_keywords():
    keywords = await EmotionKeyword.all()
    return keywords

@app.get("/emotion-keywords/type/{emotion_type}", response_model=List[EmotionKeywordResponse])
async def get_emotion_keywords_by_type(emotion_type: EmotionType):
    keywords = await EmotionKeyword.filter(emotion_type=emotion_type).all()
    return keywords

@app.put("/emotion-keywords/{keyword_id}")
async def update_emotion_keyword(
        keyword_id: int, emotion_keyword: str, emotion_type: str
):
    if emotion_type not in ["positive", "negative", "neutral"]:
        return {"error": "emotion_type must be one of: positive, negative, neutral"}

    keyword_obj = await EmotionKeyword.get_or_none(id=keyword_id)
    if not keyword_obj:
        return {"error": "Emotion keyword not found"}

    keyword_obj.emotion_keyword = emotion_keyword
    keyword_obj.emotion_type = emotion_type
    await keyword_obj.save()

    return {
        "id": keyword_obj.id,
        "emotion_keyword": keyword_obj.emotion_keyword,
        "emotion_type": keyword_obj.emotion_type,
    }