from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model

app = FastAPI()


# 감정키워드 모델
class EmotionKeyword(Model):
    id = fields.IntField(pk=True)
    emotion_keyword = fields.CharField(max_length=50)
    emotion_type = fields.CharEnumField(
        max_length=20, enum_type=["positive", "negative", "neutral"]
    )  # ENUM 타입으로 수정

    class Meta:
        table = "emotion_keyword"


# FastAPI 시작 시 DB 초기화 및 연결
@app.on_event("startup")
async def init_db():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()


# FastAPI 종료 시 DB 연결 닫기
@app.on_event("shutdown")
async def close_db():
    await Tortoise.close_connections()


# 감정 키워드 생성
@app.post("/emotion-keywords/")
async def create_emotion_keyword(emotion_keyword: str, emotion_type: str):
    # emotion_type 유효성 검사
    if emotion_type not in ["positive", "negative", "neutral"]:
        return {"error": "emotion_type must be one of: positive, negative, neutral"}

    emotion_keyword_obj = await EmotionKeyword.create(
        emotion_keyword=emotion_keyword, emotion_type=emotion_type
    )
    return {
        "id": emotion_keyword_obj.id,
        "emotion_keyword": emotion_keyword_obj.emotion_keyword,
        "emotion_type": emotion_keyword_obj.emotion_type,
    }


# 모든 감정 키워드 조회
@app.get("/emotion-keywords/")
async def get_emotion_keywords():
    keywords = await EmotionKeyword.all()
    return [
        {
            "id": k.id,
            "emotion_keyword": k.emotion_keyword,
            "emotion_type": k.emotion_type,
        }
        for k in keywords
    ]


# 특정 감정 타입의 키워드 조회
@app.get("/emotion-keywords/type/{emotion_type}")
async def get_emotion_keywords_by_type(emotion_type: str):
    if emotion_type not in ["positive", "negative", "neutral"]:
        return {"error": "emotion_type must be one of: positive, negative, neutral"}

    keywords = await EmotionKeyword.filter(emotion_type=emotion_type).all()
    return [
        {
            "id": k.id,
            "emotion_keyword": k.emotion_keyword,
            "emotion_type": k.emotion_type,
        }
        for k in keywords
    ]


# 감정 키워드 수정
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


# 감정 키워드 삭제
@app.delete("/emotion-keywords/{keyword_id}")
async def delete_emotion_keyword(keyword_id: int):
    keyword_obj = await EmotionKeyword.get_or_none(id=keyword_id)
    if not keyword_obj:
        return {"error": "Emotion keyword not found"}

    await keyword_obj.delete()
    return {"message": "Emotion keyword deleted successfully"}
