# app/db/__init__.py

TORTOISE_ORM = {
    "connections": {
        "default": {"default": "sqlite://:memory:"}
    },
    "apps": {
        "models": {
            "models": [

                "app.models.diaries",

            ],
            "default_connection": "default",
        },
    },
}
