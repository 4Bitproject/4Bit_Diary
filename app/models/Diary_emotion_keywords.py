from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from datetime import datetime
from typing import List, Optional

app = FastAPI()


# 감정키워드 모델
class EmotionKeyword(Model):
    id = fields.IntField(pk=True)
    emotion_keyword = fields.CharField(max_length=50)  # 스키마에 맞게 수정
    emotion_type = fields.CharEnumField(max_length=20, enum_type=['positive', 'negative', 'neutral'])

    class Meta:
        table = "emotion_keyword"


# 일기감정 모델
class DiaryEmotion(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    diary_id = fields.IntField()
    title = fields.CharField(max_length=255, null=True)  # 제목 추가
    content = fields.TextField()  # 내용 추가
    emotional_summary = fields.CharField(max_length=255, null=True)  # 감정 요약
    emotional_state = fields.CharField(max_length=255)  # 감정 상태
    created_date = fields.DatetimeField(auto_now_add=True)  # 생성일
    revised_date = fields.DatetimeField(auto_now=True)  # 수정일

    class Meta:
        table = "diarys"


# 일기-감정키워드 연결 테이블 (Many-to-Many)
class DiaryEmotionKeyword(Model):
    emotion_keyword_id = fields.IntField()
    diary_id = fields.IntField()

    class Meta:
        table = "diary_emotion_keywords"


# FastAPI 시작 시 DB 초기화 및 연결
@app.on_event("startup")
async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["__main__"]}
    )
    await Tortoise.generate_schemas()


# FastAPI 종료 시 DB 연결 닫기
@app.on_event("shutdown")
async def close_db():
    await Tortoise.close_connections()


# 일기 생성
@app.post("/diarys/")
async def create_diary(
        user_id: int,
        title: Optional[str] = None,
        content: str = "",
        emotional_summary: Optional[str] = None,
        emotional_state: str = "neutral"
):
    diary = await DiaryEmotion.create(
        user_id=user_id,
        title=title,
        content=content,
        emotional_summary=emotional_summary,
        emotional_state=emotional_state
    )
    return {
        "id": diary.id,
        "user_id": diary.user_id,
        "diary_id": diary.diary_id,
        "title": diary.title,
        "content": diary.content,
        "emotional_summary": diary.emotional_summary,
        "emotional_state": diary.emotional_state,
        "created_date": diary.created_date,
        "revised_date": diary.revised_date
    }


# 특정 사용자의 일기 조회
@app.get("/diarys/user/{user_id}")
async def get_user_diaries(user_id: int):
    diaries = await DiaryEmotion.filter(user_id=user_id).all()
    return [{
        "id": diary.id,
        "user_id": diary.user_id,
        "diary_id": diary.diary_id,
        "title": diary.title,
        "content": diary.content,
        "emotional_summary": diary.emotional_summary,
        "emotional_state": diary.emotional_state,
        "created_date": diary.created_date,
        "revised_date": diary.revised_date
    } for diary in diaries]


# 특정 일기 조회
@app.get("/diarys/{diary_id}")
async def get_diary(diary_id: int):
    diary = await DiaryEmotion.get_or_none(diary_id=diary_id)
    if not diary:
        return {"error": "Diary not found"}

    return {
        "id": diary.id,
        "user_id": diary.user_id,
        "diary_id": diary.diary_id,
        "title": diary.title,
        "content": diary.content,
        "emotional_summary": diary.emotional_summary,
        "emotional_state": diary.emotional_state,
        "created_date": diary.created_date,
        "revised_date": diary.revised_date
    }


# 일기-감정키워드 연결 생성
@app.post("/diary-emotion-keywords/")
async def create_diary_emotion_keyword(diary_id: int, emotion_keyword_id: int):
    keyword_relation = await DiaryEmotionKeyword.create(
        diary_id=diary_id,
        emotion_keyword_id=emotion_keyword_id
    )
    return {
        "diary_id": keyword_relation.diary_id,
        "emotion_keyword_id": keyword_relation.emotion_keyword_id
    }


# 특정 일기의 감정키워드 조회
@app.get("/diary-emotion-keywords/{diary_id}")
async def get_diary_emotion_keywords(diary_id: int):
    relations = await DiaryEmotionKeyword.filter(diary_id=diary_id).all()
    keyword_ids = [rel.emotion_keyword_id for rel in relations]

    keywords = await EmotionKeyword.filter(id__in=keyword_ids).all()
    return [{
        "id": keyword.id,
        "emotion_keyword": keyword.emotion_keyword,
        "emotion_type": keyword.emotion_type
    } for keyword in keywords]