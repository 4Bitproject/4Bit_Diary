# main.py 또는 해당 Python 파일
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise import Tortoise, fields
from tortoise.models import Model

app = FastAPI()

# Tortoise ORM 모델 예시
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

# Pydantic 모델 예시
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

# FastAPI 엔드포인트 예시
@app.get("/users", response_model=List[UserResponse])
async def get_users():
    users = await User.all()
    return users

@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    try:
        user = await User.create(**user_data.dict())
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 데이터베이스 초기화
@app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["__main__"]}  # 현재 모듈의 모델들을 등록
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()