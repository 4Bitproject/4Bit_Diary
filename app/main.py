import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

# 환경 변수 로드
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    attempt = 0
    max_attempts = 10
    retry_interval = 1

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")

    while attempt < max_attempts:
        try:
            print(f"[{attempt + 1}/{max_attempts}] 데이터베이스 연결을 시도합니다...")
            # Tortoise 초기화: DB 연결 및 모델 로드
            await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.models"]})
            print("데이터베이스 연결 성공.")

            # 스키마 생성 (개발 환경 전용)
            await Tortoise.generate_schemas()
            print("데이터베이스 스키마 생성 완료.")
            break
        except DBConnectionError as e:
            attempt += 1
            if attempt < max_attempts:
                print(f"DB 연결 실패: {e}. {retry_interval}초 후 재시도합니다.")
                await asyncio.sleep(retry_interval)
            else:
                print(
                    f"최대 재시도 횟수({max_attempts}) 초과. 데이터베이스 연결에 실패했습니다."
                )
                raise RuntimeError(
                    "데이터베이스 연결 실패, 애플리케이션을 시작할 수 없습니다."
                ) from e

    yield
    if Tortoise.is_init():
        print("애플리케이션 종료. 데이터베이스 연결을 닫습니다.")
        await Tortoise.close_connections()
    else:
        print("데이터베이스가 초기화되지 않아 닫을 연결이 없습니다.")


app = FastAPI(lifespan=lifespan)
