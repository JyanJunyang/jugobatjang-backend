# 주고받장 백엔드 

[참고한 아키텍처 : fastapi-clean-architecture](https://github.com/jujumilk3/fastapi-clean-architecture/)

이 프로젝트는 FastAPI를 기반으로 한 경조사비 관리 애플리케이션입니다. 사용자는 경조사 기록을 관리하고, 엑셀 업로드 및 공유 기능을 활용할 수 있습니다.

## 🛠️ 프로젝트 구조

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

## 🚀 실행 방법

### 1️⃣ 환경 설정

```bash
# 가상 환경 생성 및 활성화 (Poetry 사용)
poetry install
poetry shell
```

### 2️⃣ 환경 변수 설정

`.env` 파일을 생성하고 아래 내용을 추가하세요.

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

### 3️⃣ 애플리케이션 실행

```bash
uvicorn app.main:app --port 8080 --reload
```

## 🧪 테스트 실행

```bash
pytest
```

## 📌 주요 기능

- **사용자 인증**: JWT를 활용한 로그인/회원가입
- **경조사 관리**: 경조사 기록 등록, 수정, 삭제
- **엑셀 업로드 및 공유**: 경조사 데이터를 엑셀로 업로드 및 공유 가능
- **RESTful API**: FastAPI 기반으로 설계
