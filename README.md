# Edu Agents

Streamlit Web 서비스와 AI Agent 서비스를 함께 관리하는 모노레포 프로젝트입니다.

## 프로젝트 구조

```
edu-agents/
├── services/
│   ├── web/                # Streamlit Web 서비스 (Port: 8501)
│   │   ├── app.py          # 메인 앱
│   │   ├── pages/          # 멀티페이지
│   │   └── components/     # UI 컴포넌트
│   │
│   └── agent/              # AI Agent 서비스 (Port: 8000)
│       ├── main.py         # FastAPI 엔트리포인트
│       ├── agents/         # Agent 정의
│       └── tools/          # Agent 도구
│
├── scripts/
│   └── dev.sh              # 개발 스크립트
├── docker-compose.yml      # 통합 실행
└── .env.example            # 환경변수 템플릿
```

## 요구사항

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (패키지 관리자)

## 시작하기

### 1. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env
# .env 파일 편집하여 API 키 설정
```

### 2. 로컬 개발 환경 설정

```bash
# 모든 서비스 설정
./scripts/dev.sh setup

# 또는 개별 서비스 설정
./scripts/dev.sh setup-web
./scripts/dev.sh setup-agent
```

### 3. 서비스 실행

```bash
# Web 서비스만 실행
./scripts/dev.sh run-web

# Agent 서비스만 실행
./scripts/dev.sh run-agent
```

### 4. Docker로 실행

```bash
# 모든 서비스 시작
./scripts/dev.sh docker-up

# 서비스 중지
./scripts/dev.sh docker-down
```

### 5. 환경 정리

```bash
# 가상환경 삭제
./scripts/dev.sh clean
```

## 사용 가능한 명령어

```bash
./scripts/dev.sh help
```

| 명령어 | 설명 |
|--------|------|
| `setup` | 모든 서비스 환경 설정 |
| `setup-web` | Web 서비스만 설정 |
| `setup-agent` | Agent 서비스만 설정 |
| `run-web` | Web 서비스 실행 |
| `run-agent` | Agent 서비스 실행 |
| `docker-up` | Docker로 전체 서비스 시작 |
| `docker-down` | Docker 서비스 중지 |
| `clean` | 가상환경 삭제 |
| `help` | 도움말 표시 |

## 서비스 접속

- **Web Service**: http://localhost:8501
- **Agent Service**: http://localhost:8000
- **Agent API Docs**: http://localhost:8000/docs

## 개발 가이드

### 새로운 페이지 추가 (Web)

`services/web/pages/` 디렉토리에 새로운 `.py` 파일을 추가합니다.

### 새로운 Agent 추가

`services/agent/agents/` 디렉토리에 Agent 클래스를 정의합니다.

### 새로운 Tool 추가

`services/agent/tools/` 디렉토리에 Tool 함수를 정의합니다.
