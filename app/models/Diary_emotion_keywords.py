from fastapi import FastAPI, HTTPException
from tortoise import Tortoise, fields
from tortoise.models import Model
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()


# Pydantic 모델들 (요청/응답 검증용)
class DiaryCreate(BaseModel):
    user_id: int
    title: Optional[str] = None
    content: str = ""
    emotional_summary: Optional[str] = None
    emotional_state: str = "neutral"


class DiaryEmotionKeywordCreate(BaseModel):
    diary_id: int
    emotion_keyword_id: int


# 감정키워드 모델
class EmotionKeyword(Model):
    id = fields.IntField(pk=True)
    emotion_keyword = fields.CharField(max_length=50)
    emotion_type = fields.CharField(max_length=20)  # CharEnumField 대신 CharField 사용

    class Meta:
        table = "emotion_keyword"


# 일기감정 모델
class DiaryEmotion(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    diary_id = fields.IntField(null=True)  # auto_increment로 생성되는 경우를 위해
    title = fields.CharField(max_length=255, null=True)
    content = fields.TextField()
    emotional_summary = fields.CharField(max_length=255, null=True)
    emotional_state = fields.CharField(max_length=255)
    created_date = fields.DatetimeField(auto_now_add=True)
    revised_date = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "diarys"


# 일기-감정키워드 연결 테이블 (Many-to-Many)
class DiaryEmotionKeyword(Model):
    id = fields.IntField(pk=True)  # 기본키 추가
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
async def create_diary(diary_data: DiaryCreate):
    try:
        diary = await DiaryEmotion.create(
            user_id=diary_data.user_id,
            title=diary_data.title,
            content=diary_data.content,
            emotional_summary=diary_data.emotional_summary,
            emotional_state=diary_data.emotional_state,
            diary_id=None  # 자동으로 생성되도록
        )

        # diary_id를 id로 업데이트 (필요한 경우)
        diary.diary_id = diary.id
        await diary.save()

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create diary: {str(e)}")


# 특정 사용자의 일기 조회
@app.get("/diarys/user/{user_id}")
async def get_user_diaries(user_id: int):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user diaries: {str(e)}")


# 특정 일기 조회 (id로 조회하도록 수정)
@app.get("/diarys/{diary_id}")
async def get_diary(diary_id: int):
    try:
        diary = await DiaryEmotion.get_or_none(id=diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")

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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get diary: {str(e)}")


# 일기-감정키워드 연결 생성
@app.post("/diary-emotion-keywords/")
async def create_diary_emotion_keyword(keyword_data: DiaryEmotionKeywordCreate):
    try:
        # 일기와 감정키워드가 존재하는지 확인
        diary = await DiaryEmotion.get_or_none(id=keyword_data.diary_id)
        emotion_keyword = await EmotionKeyword.get_or_none(id=keyword_data.emotion_keyword_id)

        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        if not emotion_keyword:
            raise HTTPException(status_code=404, detail="Emotion keyword not found")

        # 중복 연결 확인
        existing = await DiaryEmotionKeyword.get_or_none(
            diary_id=keyword_data.diary_id,
            emotion_keyword_id=keyword_data.emotion_keyword_id
        )
        if existing:
            raise HTTPException(status_code=400, detail="Relationship already exists")

        keyword_relation = await DiaryEmotionKeyword.create(
            diary_id=keyword_data.diary_id,
            emotion_keyword_id=keyword_data.emotion_keyword_id
        )
        return {
            "id": keyword_relation.id,
            "diary_id": keyword_relation.diary_id,
            "emotion_keyword_id": keyword_relation.emotion_keyword_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create relationship: {str(e)}")


# 특정 일기의 감정키워드 조회
@app.get("/diary-emotion-keywords/{diary_id}")
async def get_diary_emotion_keywords(diary_id: int):
    try:
        # 일기가 존재하는지 확인
        diary = await DiaryEmotion.get_or_none(id=diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")

        relations = await DiaryEmotionKeyword.filter(diary_id=diary_id).all()
        keyword_ids = [rel.emotion_keyword_id for rel in relations]

        if not keyword_ids:
            return []

        keywords = await EmotionKeyword.filter(id__in=keyword_ids).all()
        return [{
            "id": keyword.id,
            "emotion_keyword": keyword.emotion_keyword,
            "emotion_type": keyword.emotion_type
        } for keyword in keywords]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emotion keywords: {str(e)}")


# 감정키워드 생성 (테스트용)
@app.post("/emotion-keywords/")
async def create_emotion_keyword(emotion_keyword: str, emotion_type: str):
    try:
        keyword = await EmotionKeyword.create(
            emotion_keyword=emotion_keyword,
            emotion_type=emotion_type
        )
        return {
            "id": keyword.id,
            "emotion_keyword": keyword.emotion_keyword,
            "emotion_type": keyword.emotion_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create emotion keyword: {str(e)}")


# 모든 감정키워드 조회
@app.get("/emotion-keywords/")
async def get_all_emotion_keywords():
    try:
        keywords = await EmotionKeyword.all()
        return [{
            "id": keyword.id,
            "emotion_keyword": keyword.emotion_keyword,
            "emotion_type": keyword.emotion_type
        } for keyword in keywords]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get emotion keywords: {str(e)}")


# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Diary Emotion API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)