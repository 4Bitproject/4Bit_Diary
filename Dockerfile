# 파이썬 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
# `gcc`는 psycopg2-binary, `netcat-openbsd`는 wait-for-it 스크립트에 필요합니다.
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN pip install uv

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

# aerich 설치 (requirements.txt에 포함되지 않은 경우)
RUN uv pip install aerich

# 애플리케이션 코드 복사
COPY . .

# app/scripts/run.sh 파일에 실행 권한 설정
# chmod +x만으로도 충분합니다.
RUN chmod +x app/scripts/run.sh

# 포트 노출
EXPOSE 8000

# 실행 명령
CMD ["bash", "app/scripts/run.sh"]