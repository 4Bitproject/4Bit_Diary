import pytest
from tortoise import Tortoise


@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    """
    pytest 세션 시작 시 Tortoise ORM을 초기화하고,
    세션 종료 시 연결을 끊습니다.
    """
    DB_CONFIG = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": {
            "models": {
                "models": ["app.models.diaries"], # 실제 모델 경로를 정확하게 입력해야 합니다.
                "default_connection": "default",
            }
        },
    }
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()

    yield # 테스트가 실행되는 시점

    await Tortoise.close_connections()