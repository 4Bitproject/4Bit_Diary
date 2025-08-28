# app/main.py

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .api.v1 import auth, diary
from .core.config import TORTOISE_ORM

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(diary.router, prefix="/api/v1")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
