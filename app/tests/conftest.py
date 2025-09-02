import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from app.core.config import TORTOISE_ORM
from app.main import app


# 각 테스트마다 새로운 DB 초기화
@pytest.fixture(autouse=True)
async def initialize_db():
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
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
