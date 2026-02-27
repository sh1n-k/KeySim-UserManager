![Go](https://img.shields.io/badge/Go-1.22.6-00ADD8?logo=go&logoColor=white)
![License](https://img.shields.io/github/license/sh1n-k/KeySim-UserManager)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

# User Management CLI Admin Tool

[한국어](#korean) | [English](#english)

<a name="korean"></a>
## 한국어

이 CLI 애플리케이션은 AWS Lambda 기반 인증 시스템과 같은 원격 백엔드 서비스의 사용자를 관리하도록 설계된 관리 도구입니다. 사용자 생명주기 관리를 위한 직관적인 명령줄 기능을 제공합니다.

### 기능

- ✅ **사용자 생성**: 백엔드 시스템에 새로운 사용자를 쉽게 추가합니다.
- ✅ **사용자 목록 조회**: 등록된 모든 사용자의 목록을 확인합니다.
- ✅ **사용자 삭제**: 시스템에서 기존 사용자를 제거합니다.
- ✅ **사용자 재설정**: 특정 사용자의 활성 세션을 무효화하고 로그인 관련 정보를 재설정합니다.

### 사전 요구 사항

- [Go](https://go.dev/doc/install) (버전 1.22.6 이상 권장)

### 백엔드 API 구성

이 CLI 도구는 원격 백엔드 API와 상호 작용합니다. 사용 전, API가 배포되어 접근 가능한지 확인해야 합니다.

- `BASE_URL`: 배포된 API Gateway 엔드포인트
- `ADMIN_KEY`: Lambda 백엔드와 일치하는 관리자 키

### 설정

1. 저장소 클론

```bash
git clone https://github.com/your-repo/keysim-admin.git # 실제 저장소 URL로 교체
cd keysim-admin
```

2. `.env` 파일 생성

```ini
BASE_URL=https://your-lambda-api-gateway-endpoint.execute-api.region.amazonaws.com/
ADMIN_KEY=your_secret_admin_key_matching_lambda
```

3. 종속성 설치 및 빌드

```bash
go mod tidy
go build -o usermanager
```

플랫폼별 빌드:
- Windows: `GOOS=windows GOARCH=amd64 go build -o usermanager.exe`
- macOS (Intel): `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
- macOS (Apple Silicon): `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

### 사용법

- 사용자 생성

```bash
./usermanager create [userId]
```

- 사용자 삭제

```bash
./usermanager delete [userId]
```

- 사용자 재설정

```bash
./usermanager reset [userId]
```

- 사용자 목록 조회

```bash
./usermanager list
```

### 프로젝트 구조

- `main.go`: CLI 명령 정의 및 백엔드 API 연동 로직
- `go.mod` / `go.sum`: Go 모듈 종속성 관리
- `.env`: `BASE_URL`, `ADMIN_KEY` 설정 파일 (Git 제외)

### 기여

기여는 언제나 환영합니다. 이슈 또는 Pull Request를 자유롭게 제출해주세요.

### 라이선스

MIT 라이선스. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

---

<a name="english"></a>
## English

This CLI application is an administrative tool designed to manage users for a remote backend service, such as an AWS Lambda-based authentication system. It provides straightforward command-line functionality for user lifecycle management.

### Features

- ✅ **User Creation**: Add new users to your backend system.
- ✅ **User Listing**: View all registered users.
- ✅ **User Deletion**: Remove existing users from the system.
- ✅ **User Reset**: Invalidate active sessions and reset login-related data for a specific user.

### Prerequisites

- [Go](https://go.dev/doc/install) (version 1.22.6 or later recommended)

### Backend API Configuration

This CLI interacts with a remote backend API. Make sure your API is deployed and reachable before use.

- `BASE_URL`: deployed API Gateway endpoint
- `ADMIN_KEY`: admin key matching the Lambda backend configuration

### Setup

1. Clone repository

```bash
git clone https://github.com/your-repo/keysim-admin.git # Replace with your actual repo URL
cd keysim-admin
```

2. Create `.env`

```ini
BASE_URL=https://your-lambda-api-gateway-endpoint.execute-api.region.amazonaws.com/
ADMIN_KEY=your_secret_admin_key_matching_lambda
```

3. Install dependencies and build

```bash
go mod tidy
go build -o usermanager
```

Platform-specific builds:
- Windows: `GOOS=windows GOARCH=amd64 go build -o usermanager.exe`
- macOS (Intel): `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
- macOS (Apple Silicon): `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

### Usage

- Create user

```bash
./usermanager create [userId]
```

- Delete user

```bash
./usermanager delete [userId]
```

- Reset user

```bash
./usermanager reset [userId]
```

- List users

```bash
./usermanager list
```

### Project Structure

- `main.go`: entry point and CLI/API interaction logic
- `go.mod` / `go.sum`: Go dependency management
- `.env`: environment configuration for `BASE_URL` and `ADMIN_KEY` (gitignored)

### Contributing

Contributions are welcome. Feel free to open issues or pull requests.

### License

MIT License. See [LICENSE](LICENSE) for details.
