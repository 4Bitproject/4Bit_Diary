# app/tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer
from app.main import app

@pytest.fixture(scope="module")
def client():
    # 테스트용 파일 DB
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "test_db.sqlite3")
    db_url = f"sqlite:///{db_path}"

    initializer(
        ["app.models.diaries"],
        db_url=db_url,
        app_label="models"
    )
    with TestClient(app) as c:
        yield c
    finalizer()
    if os.path.exists(db_path):
        os.remove(db_path)
