import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.diaries import EmotionalState


@pytest.mark.asyncio
async def test_crud_diary():
    client = TestClient(app)

    # ✅ 1. CREATE
    payload_create = {
        "user_id": 1,
        "title": "테스트 일기",
        "content": "오늘은 좋은 날",
        "emotional_state": EmotionalState.HAPPY.value,
        "ai_summary": None,
    }
    response = client.post("/diaries/", json=payload_create)
    assert response.status_code == 200
    diary = response.json()
    diary_id = diary["id"]
    assert diary["title"] == "테스트 일기"

    # ✅ 2. READ
    response = client.get(f"/diaries/{diary_id}")
    assert response.status_code == 200
    diary = response.json()
    assert diary["title"] == "테스트 일기"

    # ✅ 3. UPDATE
    payload_update = {
        "title": "수정된 일기",
        "content": "오늘은 좋은 날이었음",
        "emotional_state": EmotionalState.SAD.value,
        "ai_summary": "AI 요약",
    }
    response = client.put(f"/diaries/{diary_id}", json=payload_update)
    assert response.status_code == 200
    diary = response.json()
    assert diary["title"] == "수정된 일기"
    assert diary["emotional_state"] == "sad"

    # ✅ 4. DELETE
    response = client.delete(f"/diaries/{diary_id}")
    assert response.status_code == 200

    # ✅ 5. READ AFTER DELETE
    response = client.get(f"/diaries/{diary_id}")
    assert response.status_code == 404
