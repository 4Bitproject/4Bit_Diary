import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from app.api.v1.auth import router as auth_router

DATABASE_URL = "sqlite://db.sqlite3"  # DB 주소는 그대로 유지


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB 연결 초기화
    attempt = 0
    max_attempts = 10
    retry_interval = 1

    while attempt < max_attempts:
        try:
            # 이 코드는 이전과 동일합니다.
            await Tortoise.init(
                db_url=DATABASE_URL, modules={"models": ["app.models.user"]}
            )
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

    # DB 연결 종료
    # 'connections' 객체를 사용하지 않고, Tortoise 객체의 메서드를 사용합니다.
    await Tortoise.close_connections()
    print("DB 연결 종료.")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
