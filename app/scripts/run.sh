#!/bin/bash
set -e

# 스크립트 자체에 실행 권한 부여 (런타임에)
chmod +x "$0" 2>/dev/null || true

echo "Starting FastAPI application..."

# 데이터베이스가 준비될 때까지 대기
echo "Waiting for database..."
while ! nc -z db 5432; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready!"

# Aerich가 설치되어 있는지 확인
if command -v aerich >/dev/null 2>&1; then
    echo "Aerich is available"

    # Aerich 초기화 (처음 실행할 때만)
    if [ ! -f "migrations/models/0_initial.py" ]; then
        echo "Initializing aerich..."
        aerich init -t app.database.TORTOISE_ORM || echo "Aerich init failed, continuing..."
        aerich init-db || echo "Aerich init-db failed, continuing..."
    fi

    # 마이그레이션 실행
    echo "Running migrations..."
    aerich upgrade || echo "Migration failed, continuing..."
else
    echo "Aerich not found, skipping migrations"
fi

# FastAPI 서버 실행
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload