# app/db/__init__.py

TORTOISE_ORM = {
    "connections": {"default": {"default": "sqlite://:memory:"}},
    "apps": {
        "models": {
            "models": [
                "app.models.diary",
            ],
            "default_connection": "default",
        },
    },
}
