## 목차
- [Service Information](#service-information)
- [Server Environment](#server-environment)
  - [기술스택](#기술스택)
  - [프로젝트 구조](#프로젝트-구조)
- [Base Setting](#base-setting)
  - [환경변수](#환경변수)
  - [환경설정](#환경설정)
- [Docker](#docker)
- [Execution](#execution)
  - [애플리케이션 실행](#애플리케이션-실행)
  - [테스트 실행](#테스트-실행)

--- 

# Service Information
**본 프로젝트는 '경조사비 기록 앱'을 개발하기 위한 사이드 프로젝트입니다.**

현대인들이 경조사비용을 고민할 때 가장 큰 걱정은 **“내가 준 만큼 다시 받을 수 있을까?”** 라는 질문입니다.
이 프로젝트는 그 의문을 해소하고자 시작되었습니다.
앱과 웹 두 가지 플랫폼을 통해, 앱에서는 **빠르고 간편한 기록 기능**을, 웹에서는 **엑셀 기반의 대량 관리 및 호환성을**
제공하여 사용자들이 더욱 체계적으로 경조사비를 관리할 수 있도록 돕습니다.

# Server Environment
### 기술스택

| 항목       | 구성 요소              |
|------------|------------------------|
| 언어       | Python 3.11            |
| 프레임워크 | FastAPI 0.115.8        |
| 서버       | Uvicorn 0.34.0         |
| 데이터베이스 | MariaDB 9.2.0         |
| ORM        | SQLAlchemy 2.0.38      |
| 테스트     | Pytest 8.3.5, Faker 36.1.0 |
| 배포       | CloudType, Docker      |

### 프로젝트 구조
```
app
│── core               # 설정 및 핵심 로직
│   ├── config.py
│   ├── container.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── security.py
│── model              # 데이터베이스 모델
│   ├── base_model.py
│   ├── calendar.py
│   ├── excels.py
│   ├── records.py
│   └── users.py
│── schema             # Pydantic 스키마 정의
│   ├── auth.py
│   ├── base.py
│   ├── calendar.py
│   ├── event.py
│   ├── records.py
│   ├── relation.py
│   └── user.py
│── services           # 서비스 로직
│   ├── auth_service.py
│   ├── event_service.py
│   ├── record_service.py
│   ├── relation_service.py
│   └── user_service.py
│── util               # 유틸리티 모듈
│   └── limit_checker.py
│── main.py            # FastAPI 실행 진입점
```
# Base Setting
### 환경변수
```env
DB_ENGINE=mariadb+pymysql
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
DATA_BASE=<your_db_base>

KAKAO_API_KEY=<your_kakao_api_key>
KAKAO_REDIRECT_URI=http://127.0.0.1:8080/auth/kakao/callback # 테스트용

SECRET_KEY=<your_secret_key>
REFRESH_SECRET_KEY=<your_refresh_secret_key>
ALGORITHM=HS256

MAX_RELATION_COUNT=15
MAX_EVENTTYPE_COUNT=15

```
### 환경설정
```bash
# 가상 환경 생성 및 활성화 (Poetry 사용)
poetry install
poetry shell
```

# Docker
```bash
docker-compose up --build -d
```
# execution
### 애플리케이션 실행

```bash
uvicorn app.main:app --port 8080 --reload
```

### 테스트 실행

```bash
pytest
```
