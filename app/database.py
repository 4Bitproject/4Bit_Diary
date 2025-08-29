import os

from tortoise import Tortoise


DATABASE_URL = os.getenv("DATABASE_URL", "postgres://fastapi_user:fastapi_password@db:5432/fastapi_db")

TORTOISE_ORM = {
    "connections": {"default": "postgres://fastapi_user:your_secure_password_123@127.0.0.1:5432/fastapi_db"},
    "apps": {
        "models": {
            "models": [
                "app.models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
