#!/bin/bash
set -e

chmod +x "$0" 2>/dev/null || true

echo "Starting FastAPI application..."

echo "Waiting for database..."
while ! nc -z db 5432; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready!"

if command -v aerich >/dev/null 2>&1; then
    echo "Aerich is available"

    if [ ! -f "migrations/models/0_initial.py" ]; then
        echo "Initializing aerich..."
        # -t 옵션에서 app.database를 app.core.config로 수정
        aerich init -t app.core.config.TORTOISE_ORM || echo "Aerich init failed, continuing..."
        aerich init-db || echo "Aerich init-db failed, continuing..."
    fi

    echo "Running migrations..."
    aerich upgrade || echo "Migration failed, continuing..."
else
    echo "Aerich not found, skipping migrations"
fi

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload