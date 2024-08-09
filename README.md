# User Management CLI

This CLI application provides user management functionality, including creating users, deleting users, resetting user keys, and listing all users.

## Setup

1. Ensure Go is installed on your system.
2. Clone this repository.
3. Create a `.env` file in the project root with the following content:
   ```
   BASE_URL=your_api_base_url
   ADMIN_KEY=your_admin_key
   ```
4. Build the application using the appropriate command for your system:
   - Windows: `go build -o usermanager.exe`
   - macOS (Intel): `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
   - macOS (Apple Silicon): `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

## Usage

- Create a user: `./usermanager create [userId]`
- Delete a user: `./usermanager delete [userId]`
- Reset a user's key: `./usermanager reset [userId]`
- List all users: `./usermanager list`

---

# 사용자 관리 CLI

이 CLI 애플리케이션은 사용자 생성, 삭제, 키 재설정 및 모든 사용자 나열 등의 사용자 관리 기능을 제공합니다.

## 설정

1. 시스템에 Go가 설치되어 있는지 확인하세요.
2. 이 저장소를 클론하세요.
3. 프로젝트 루트에 다음 내용으로 `.env` 파일을 생성하세요:
   ```
   BASE_URL=your_api_base_url
   ADMIN_KEY=your_admin_key
   ```
4. 시스템에 맞는 명령어로 애플리케이션을 빌드하세요:
   - Windows: `go build -o usermanager.exe`
   - macOS (Intel): `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
   - macOS (Apple Silicon): `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

## 사용법

- 사용자 생성: `./usermanager create [userId]`
- 사용자 삭제: `./usermanager delete [userId]`
- 사용자 키 재설정: `./usermanager reset [userId]`
- 모든 사용자 나열: `./usermanager list`