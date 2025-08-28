# app/core/config.py


SECRET_KEY = "your-very-secret-key-that-should-be-kept-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

TORTOISE_ORM = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.token_blacklist",
                "app.models.diary",
                "app.models.tag",
            ],
            "default_connection": "default",
        },
    },
}
