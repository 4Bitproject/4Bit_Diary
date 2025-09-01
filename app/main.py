# app/main.py

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# 라우터 파일에서 라우터를 직접 임포트합니다.
from .api.v1.auth import router as auth_router
from .api.v1.diary import router as diary_router
from .core.config import TORTOISE_ORM

app = FastAPI(title="4Bit_Diary API")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

# 라우터들을 한 번에 등록하고 접두사를 한 번만 적용합니다.
app.include_router(auth_router)
app.include_router(diary_router)
