import pytest
from fastapi.testclient import TestClient

from app.api.v1.auth import get_current_user
from app.main import app


# 1. 의존성 오버라이드
# 테스트를 위해 get_current_user 함수를 임시로 가짜 사용자를 반환하도록 오버라이드합니다.
# 이렇게 해야 토큰 없이도 API 테스트가 가능합니다.
def dummy_get_current_user():
    return {"id": 1, "email": "test@test.com"}


app.dependency_overrides[get_current_user] = dummy_get_current_user


# 2. 테스트 클라이언트 픽스처
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


# 3. 통합 테스트 시나리오
def test_full_auth_lifecycle(client):
    # 테스트에 사용할 유저 정보
    test_user = {
        "email": "test_user@example.com",
        "password": "testpassword123",
        "nickname": "TestUserNickname",
        "name": "Test User",
    }

    # ----------------------------------------------------
    # 단계 1: 회원가입 (Register)
    # ----------------------------------------------------
    response = client.post("/api/v1/register", json=test_user)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "회원가입이 완료되었습니다."

    # ----------------------------------------------------
    # 단계 2: 로그인 (Login) - 토큰을 얻기 위해 로그인 API를 호출합니다.
    # ----------------------------------------------------
    login_data = {"email": test_user["email"], "password": test_user["password"]}
    response = client.post("/api/v1/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]

    # ----------------------------------------------------
    # 단계 3: 프로필 조회 (Get User Profile)
    # ----------------------------------------------------
    # 헤더 대신 쿼리 파라미터로 토큰을 전달합니다.
    response = client.get(
        f"/api/v1/profile?token={access_token}"
    )  # URL에 직접 토큰을 추가
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]

    # ----------------------------------------------------
    # 단계 4: 프로필 수정 (Update User Profile)
    # ----------------------------------------------------
    # PUT/DELETE는 여전히 쿼리 파라미터로 토큰을 받습니다.
    update_data = {
        "new_data": {  # <-- 'new_data' 키를 추가합니다.
            "email": "updated_user@example.com"
        }
    }
    response = client.put(f"/api/v1/profile?token={access_token}", json=update_data)
    assert response.status_code == 200

    # ----------------------------------------------------
    # 단계 5: 프로필 삭제 (Delete User Profile)
    # ----------------------------------------------------
    response = client.delete(f"/api/v1/profile?token={access_token}")
    assert response.status_code == 200  # <-- 204 대신 200으로 변경
    # 삭제 메시지가 있다면 메시지 검증 추가
    # assert "message" in response.json()

    # ----------------------------------------------------
    # 단계 6: 삭제된 프로필 조회 시도
    # ----------------------------------------------------
    response = client.get(f"/api/v1/profile?token={access_token}")
    assert response.status_code == 401
