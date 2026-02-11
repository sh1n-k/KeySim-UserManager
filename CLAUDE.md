# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KeySim-UserManager는 관리자용 Go CLI 도구:
- **Go CLI** (`main.go`) — DynamoDB 백엔드의 사용자 CRUD를 수행
- Lambda 백엔드 소스는 [KeystrokeSimulator](../KeystrokeSimulator/) 프로젝트의 `_lambda.py`에서 관리

## Build & Run

```bash
# 의존성 설치
go mod tidy

# 빌드
go build -o usermanager

# 크로스 컴파일
GOOS=darwin GOARCH=arm64 go build -o usermanager-arm   # Apple Silicon
GOOS=windows GOARCH=amd64 go build -o usermanager.exe  # Windows

# 실행 (사전에 .env 설정 필요)
./usermanager create <userId>
./usermanager list
./usermanager delete <userId>
./usermanager reset <userId>
```

## Configuration

`.env` 파일 필수 (gitignore 대상):
- `BASE_URL` — API Gateway 엔드포인트 URL
- `ADMIN_KEY` — Lambda 백엔드와 일치하는 관리자 키

## Architecture

### Go CLI (`main.go`)
- `cobra`로 CLI 명령 정의 (create, list, delete, reset)
- `godotenv`로 .env 로드
- 모든 명령은 `executeRequest()`를 통해 Lambda API에 POST 요청
- 관리자 인증은 요청 body에 `adminKey`를 포함하여 전달

## Key Dependencies

- Go 1.22.6, `github.com/spf13/cobra`, `github.com/joho/godotenv`
