import sys
import os

# 현재 스크립트의 상위 디렉토리(app/)를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 프로젝트 루트 디렉토리(4Bit_Diary/)를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.main import app
from app.models.diary import EmotionalState

def test_full_diary_lifecycle(client):
    # 테스트에 사용할 유저 정보 (auth 테스트와 동일하게)
    test_user = {
        "email": "diary_test_user@example.com",
        "password": "testpassword123",
        "nickname": "TestUserNickname",
        "name": "Test User",
    }

    # 회원가입 및 로그인하여 토큰 얻기 (기존 auth 테스트에서 가져옵니다)
    response = client.post("/api/v1/register", json=test_user)
    assert response.status_code == 200

    login_data = {"email": test_user["email"], "password": test_user["password"]}
    response = client.post("/api/v1/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]

    # ----------------------------------------------------
    # 단계 1: 일기 생성 (CREATE) - 토큰과 함께 요청
    # ----------------------------------------------------
    create_data = {
        "title": "테스트 통합 일기",
        "content": "통합 테스트 내용입니다.",

        "emotional_state": EmotionalState.HAPPY.value,
        "tags": ["통합", "테스트"],
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/v1/diary/create", json=create_data, headers=headers)
    assert response.status_code == 200
    new_diary_json = response.json()
    diary_id = new_diary_json["id"]

    assert new_diary_json["title"] == create_data["title"]
    assert new_diary_json["content"] == create_data["content"]
    assert new_diary_json["emotional_state"] == create_data["emotional_state"]
    assert sorted(new_diary_json["tags"]) == sorted(create_data["tags"])

    # ----------------------------------------------------
    # 단계 2: 모든 일기 조회 (READ ALL)
    # ----------------------------------------------------
    response = client.get("/api/v1/diary/inquiry", headers=headers)
    assert response.status_code == 200
    diaries = response.json()
    assert len(diaries) > 0

    # ----------------------------------------------------
    # 단계 3: 특정 일기 조회 (READ ONE)
    # ----------------------------------------------------
    response = client.get(f"/api/v1/diary/{diary_id}", headers=headers)
    assert response.status_code == 200
    read_diary = response.json()
    assert read_diary["id"] == diary_id
    assert read_diary["title"] == create_data["title"]

    # ----------------------------------------------------
    # 단계 4: 일기 수정 (UPDATE)
    # ----------------------------------------------------
    update_data = {
        "title": "수정된 제목",
        "content": "내용이 수정되었습니다.",
        "emotional_state": EmotionalState.SAD.value,
    }
    response = client.put(f"/api/v1/diary/{diary_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_diary = response.json()
    assert updated_diary["title"] == "수정된 제목"
    assert updated_diary["emotional_state"] == EmotionalState.SAD.value

    # ----------------------------------------------------
    # 단계 5: 일기 삭제 (DELETE)
    # ----------------------------------------------------
    response = client.delete(f"/api/v1/diary/{diary_id}", headers=headers)
    assert response.status_code == 200 # <-- 상태 코드 변경

    # 삭제 후 다시 조회하여 존재하지 않는지 확인합니다.
    response = client.get(f"/api/v1/diary/{diary_id}", headers=headers)
    assert response.status_code == 404 # Not Found