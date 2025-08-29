import os

from dotenv import load_dotenv

SECRET_KEY = "your-very-secret-key-that-should-be-kept-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            # NOTE: "app.models.user"로 경로가 올바르게 지정되어 있어야 합니다.
            "models": [
                "app.models.user",
                "app.models.token_blacklist",
                "app.models.diary",
            ],
            "default_connection": "default",
        },
    },
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
