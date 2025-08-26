FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# aerich 설치 (Tortoise ORM 마이그레이션 도구)
RUN pip install aerich

# 애플리케이션 코드 복사
COPY . .

# app/scripts/run.sh 파일에 실행 권한 설정 (여러 번 시도)
RUN chmod +x app/scripts/run.sh && \
    chmod 755 app/scripts/run.sh && \
    ls -la app/scripts/run.sh

# 포트 노출
EXPOSE 8000

# 실행 명령 (bash로 스크립트 실행)
CMD ["bash", "app/scripts/run.sh"]
