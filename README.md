# 💽 4Bit_Diary API

## 🎙️ 프로젝트 소개
**4Bit_Diary API** 는 **FastAPI 기반 일기 관리서비스**입니다.  

- Google **Gemini 2.5-flash** API를 이용해 일기 본문을 분석 → ai_summary를 이용해 컨텐츠 요약
 
=====================================================================================


## 📽️ 주요 기능
- **회원 관리**: 회원가입 / 로그인 / 로그아웃  
- **인증**: JWT 기반 인증  
- **일기 관리**: CRUD (생성, 조회 (전체,단일), 수정, 삭제)  
- **검색 & 선택**: 일기 내용 검색(제목별, 태그별, 컨텐츠별)  
- **감정 분석 Gemini(2.5-flash) API를 활용한 내용 정리

=====================================================================================

## ⚙️ 기술 스택
| 구분 | 기술 |
|------|------|
| **백엔드** | FastAPI, Pydantic |
| **AI** | Google Gemini 2.5-flash (API Key 기반) |
| **ORM** | Tortoise ORM |
| **데이터베이스** | PostgreSQL |
| **DevOps** | Docker, Docker Compose, Aerich (DB Migration) |
| **보안** | JWT 인증 |


=====================================================================================


## 📂 프로젝트 구조
```bash
app/
 ├── api/
 │     ├─__init__.py
 │     └─ v1
 │       ├── api.py
 │       ├── prompts.py
 │       ├── schema.py
 │       ├── service.py
 │       ├── test_gemini.py
 │       └── __init__.py
 ├── core/
 │   ├── config.py
 │   ├── logging.py
 │   ├── security.py
 │   └── __init__.py
 ├── db/
 │   ├── base.py
 │   ├── migration.py
 │   ├── session.py
 │   └── __init__.py
 ├── models/
 │   ├── diary.py
 │   ├── diary_emotion_keywords.py
 │   ├── emotion_keyword.py
 │   ├── tag.py
 │   ├── token_blacklist.py
 │   ├── user.py
 │   └── __init__.py
 ├── repositories/
 │   ├── diary_repo.py
 │   ├── tag_repo.py
 │   ├── user_repo.py
 │   └── __init__.py
 ├── schemas/
 │   ├── ai.py
 │   ├── diary.py
 │   ├── schemas.py
 │   ├── tag.py
 │   ├── user.py
 │   └── __init__.py
 ├── scripts/
 │   └── run.sh
 ├── services/
 │   ├── ai_service.py
 │   ├── diary_service.py
 │   ├── search_service.py
 │   ├── user_service.py
 │   └── __init__.py
 ├── tests/
 │   ├── conftest.py
 │   ├── test_auth_api.py
 │   ├── test_diary.py
 │   └── test_main.py
 ├── utils/
 │   └── security.py
 ├── __init__.py
 └── main.py
```
 
=====================================================================================

## 🗄 ERD

<img width="1098" height="484" alt="Fast_API ERD " src="https://github.com/user-attachments/assets/0bcdfbb0-a9f9-4da3-9f1c-34f82bef84b1" />
