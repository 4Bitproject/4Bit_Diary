# app/db/__init__.py

TORTOISE_ORM = {
    "connections": {"default": {"default": "sqlite://:memory:"}},
    "apps": {
        "models": {
            "models": [
                "app.models.diary",
                "app.models.tag",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
