from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "postgres://juwon:yourpassword@db:5432/diary_db"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
