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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
