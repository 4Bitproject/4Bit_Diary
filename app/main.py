# app/main.py

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from tortoise.contrib.fastapi import register_tortoise

# 라우터 파일에서 라우터를 직접 임포트합니다.
from .api.v1.auth import router as auth_router
from .api.v1.diary import router as diary_router
from .core.config import TORTOISE_ORM

# HTTPBearer 보안 스키마 정의
security = HTTPBearer()

app = FastAPI(
    title="4Bit_Diary API",
    description="4Bit Diary API with JWT Authentication",
    version="1.0.0",
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

# 라우터들을 한 번에 등록하고 접두사를 한 번만 적용합니다.
app.include_router(auth_router)
app.include_router(diary_router)
