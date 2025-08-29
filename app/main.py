from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .api.v1 import auth, diary

# from tortoise.connections import connections # 이 줄은 삭제합니다
from .core.config import TORTOISE_ORM

app = FastAPI(title="4Bit_Diary API")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(diary.router, prefix="/api/v1")
