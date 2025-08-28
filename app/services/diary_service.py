# app/services/diary_service.py


from ..models.diary import Diary


async def create_diary_service(user_id: str, diary_data: dict):
    try:
        new_diary = await Diary.create(
            user_id=user_id,
            title=diary_data["title"],
            content=diary_data["content"],
            emotional_state=diary_data["emotional_state"],
        )
        return {"message": "일기 생성 성공", "diary_id": str(new_diary.diary_id)}
    except Exception as e:
        return {"error": f"일기 생성 중 오류 발생: {e}"}


async def get_diaries_service(user_id: str):
    try:
        diaries = await Diary.filter(user_id=user_id).order_by("-created_date")
        return [
            {
                "id": d.diary_id,
                "title": d.title,
                "content": d.content,
                "emotional_state": d.emotional_state,
            }
            for d in diaries
        ]
    except Exception as e:
        return {"error": f"일기 조회 중 오류 발생: {e}"}
