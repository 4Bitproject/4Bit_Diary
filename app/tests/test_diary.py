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
    # 테스트에 사용할 고유한 ID를 저장할 변수
    global diary_id

    # ----------------------------------------------------
    # 단계 1: 일기 생성 (CREATE)
    # ----------------------------------------------------
    create_data = {
        "title": "테스트 통합 일기",
        "content": "통합 테스트 내용입니다.",
        "emotional_state": "happy",
        "tags": ["통합", "테스트"],
    }
    response = client.post("/api/v1/diary/create", json=create_data)

    assert response.status_code == 200
    created_diary = response.json()
    assert created_diary["title"] == "테스트 통합 일기"
    assert "id" in created_diary

    # 생성된 일기의 ID를 저장하여 다음 단계에서 사용합니다.
    diary_id = created_diary["id"]

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
        "emotional_state": "calm",
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
    assert response.status_code == 404  # Not Found
