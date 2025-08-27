import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise, connections
from tortoise.exceptions import DBConnectionError

from app.api.v1.auth import router as auth_router

DATABASE_URL = "sqlite://db.sqlite3"

@asynccontextmanager
async def lifespan(app: FastAPI):
    attempt = 0
    max_attempts = 10
    retry_interval = 1

    while attempt < max_attempts:
        try:
            await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.models.user"]})
            await Tortoise.generate_schemas()
            print("DB 연결 및 스키마 생성 성공!")
            break
        except DBConnectionError:
            attempt += 1
            if attempt == max_attempts:
                print(f"DB 연결 실패! {max_attempts}번 시도 후 종료.")
                break
            print(f"DB 연결 시도 중... {attempt}/{max_attempts}번")
            await asyncio.sleep(retry_interval)

    yield

    # 이제 연결 상태를 확인하는 불필요한 코드는 제거하고,
    # 모든 연결을 닫는 함수만 호출합니다.
    await connections.close_all()
    print("DB 연결 종료.")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])