import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.security import get_current_user


# **1. 의존성 오버라이드 (가상 사용자)**
# 테스트를 위해 get_current_user 함수를 임시로 가짜 사용자를 반환하도록 오버라이드합니다.
# 이렇게 해야 토큰 없이도 API 테스트가 가능합니다.
def dummy_get_current_user():
    return {"id": 1}

app.dependency_overrides[get_current_user] = dummy_get_current_user

# **2. 테스트 클라이언트 생성**
# pytest 픽스처를 사용하여 테스트 클라이언트를 생성합니다.
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# **3. 통합 테스트 시나리오**
# 테스트 함수는 test_로 시작해야 pytest가 인식합니다.
def test_full_diary_lifecycle(client):
    # 테스트에 사용할 유저 정보 (auth 테스트와 동일하게)
    test_user = {
        "email": "test_user@example.com",
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
        "emotional_state": "happy",
        # "tags": ["통합", "테스트"], # <-- 이 줄을 제거하거나 주석 처리합니다.
        # "ai_summary": None,  # <-- 이 줄은 이미 제거된 상태
    }
    # Authorization 헤더에 Bearer 토큰을 추가합니다.
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/v1/diary/create", json=create_data, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == create_data["title"]

    # ----------------------------------------------------
    # 단계 2: 모든 일기 조회 (READ ALL)
    # ----------------------------------------------------
    response = client.get("/api/v1/diary/inquiry")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

    # ----------------------------------------------------
    # 단계 3: 특정 일기 조회 (READ ONE)
    # ----------------------------------------------------
    response = client.get(f"/api/v1/diary/{diary_id}")
    assert response.status_code == 200
    read_diary = response.json()
    assert read_diary["id"] == diary_id
    assert read_diary["title"] == "테스트 통합 일기"

    # ----------------------------------------------------
    # 단계 4: 일기 수정 (UPDATE)
    # ----------------------------------------------------
    update_data = {
        "title": "수정된 제목",
        "content": "내용이 수정되었습니다.",
        "emotional_state": "calm"
    }
    response = client.put(f"/api/v1/diary/{diary_id}", json=update_data)
    assert response.status_code == 200
    updated_diary = response.json()
    assert updated_diary["title"] == "수정된 제목"
    assert updated_diary["emotional_state"] == "calm"

    # ----------------------------------------------------
    # 단계 5: 일기 삭제 (DELETE)
    # ----------------------------------------------------
    response = client.delete(f"/api/v1/diary/{diary_id}")
    assert response.status_code == 204

    # 삭제 후 다시 조회하여 존재하지 않는지 확인합니다.
    response = client.get(f"/api/v1/diary/{diary_id}")
    assert response.status_code == 404 # Not Found