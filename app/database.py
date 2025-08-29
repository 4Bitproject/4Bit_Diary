from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "postgres://fastapi_user:your_secure_password_123@localhost:5432/fastapi_db"},
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


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
