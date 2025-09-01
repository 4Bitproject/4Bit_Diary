import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from app.core.config import TORTOISE_ORM
from app.main import app
from app.utils.security import get_current_user


# 의존성 오버라이드
def dummy_get_current_user():
    return {"id": 1}


app.dependency_overrides[get_current_user] = dummy_get_current_user


# 테스트용 DB 초기화 및 스키마 생성 픽스처
@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    # 실제 프로젝트의 ORM 설정(Tortoise ORM)을 사용합니다.
    # 단, DB URL은 테스트용 인메모리 SQLite로 변경합니다.
    test_db_config = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": {
            "models": {
                "models": TORTOISE_ORM["apps"]["models"]["models"],
                "default_connection": "default",
            }
        },
    }

    await Tortoise.init(config=test_db_config)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


# 테스트 클라이언트 픽스처
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
