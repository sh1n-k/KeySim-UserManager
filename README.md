# User Management CLI Admin Tool

This CLI application is a powerful administrative tool designed to manage users for a remote backend service, such as an AWS Lambda-based authentication system. It provides straightforward command-line functionalities for user lifecycle management.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Backend API Configuration](#backend-api-configuration)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

<h2 id="features">Features</h2>

- ✅ **User Creation**: Easily add new users to your backend system.
- ✅ **User Listing**: View a comprehensive list of all registered users.
- ✅ **User Deletion**: Remove existing users from the system.
- ✅ **User Reset**: Invalidate all active sessions and reset login-related information for a specific user, ensuring their next login requires re-authentication.

<h2 id="prerequisites">Prerequisites</h2>

Before you begin, ensure you have the following installed on your system:
- [Go](https://go.dev/doc/install) (version 1.22.6 or later recommended)

<h2 id="backend-api-configuration">Backend API Configuration</h2>

This CLI tool interacts with a remote backend API. Before using it, ensure your API is deployed and accessible.
You will need the `BASE_URL` of your deployed API Gateway endpoint and the `ADMIN_KEY` that matches the `ADMIN_KEY` configured in your Lambda backend.

<h2 id="setup">Setup</h2>

Follow these steps to set up the CLI application locally:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/keysim-admin.git # Replace with your actual repo URL
    cd keysim-admin
    ```

2.  **Create a `.env` file**:
    In the project root directory, create a file named `.env` and populate it with your backend API details:
    ```ini
    BASE_URL=https://your-lambda-api-gateway-endpoint.execute-api.region.amazonaws.com/
    ADMIN_KEY=your_secret_admin_key_matching_lambda
    ```
    *Replace the placeholder values with your actual API URL and admin key.*

3.  **Install dependencies and build the application**:
    Navigate to the `keysim-admin` directory and run the following commands:
    ```bash
    go mod tidy
    go build -o usermanager
    ```
    For platform-specific builds (e.g., for cross-compilation):
    -   **Windows**: `GOOS=windows GOARCH=amd64 go build -o usermanager.exe`
    -   **macOS (Intel)**: `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
    -   **macOS (Apple Silicon)**: `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

<h2 id="usage">Usage</h2>

Once built, you can run the `usermanager` executable from your terminal. All commands follow a similar structure:

-   **Create a user**:
    ```bash
    ./usermanager create [userId]
    ```
    Example: `./usermanager create newuser123`

-   **Delete a user**:
    ```bash
    ./usermanager delete [userId]
    ```
    Example: `./usermanager delete olduser`

-   **Reset a user**:
    ```bash
    ./usermanager reset [userId]
    ```
    *This command invalidates existing sessions and clears login-related data for the specified user, requiring them to re-authenticate.*
    Example: `./usermanager reset compromiseduser`

-   **List all users**:
    ```bash
    ./usermanager list
    ```

<h2 id="project-structure">Project Structure</h2>

-   `main.go`: The main application entry point, containing the CLI command definitions and logic for interacting with the backend API.
-   `go.mod` & `go.sum`: Go module dependency management files.
-   `.env`: Environment variable configuration for `BASE_URL` and `ADMIN_KEY`. (Ignored by Git for security)

<h2 id="contributing">Contributing</h2>

Contributions are welcome! Please feel free to submit issues or pull requests.

<h2 id="license">License</h2>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 사용자 관리 CLI 관리 도구

이 CLI 애플리케이션은 AWS Lambda 기반 인증 시스템과 같은 원격 백엔드 서비스의 사용자를 관리하도록 설계된 강력한 관리 도구입니다. 사용자 생명주기 관리를 위한 직관적인 명령줄 기능을 제공합니다.

## 목차
- [기능](#기능)
- [사전 요구 사항](#사전-요구-사항)
- [백엔드 API 구성](#백엔드-api-구성)
- [설정](#설정)
- [사용법](#사용법)
- [프로젝트 구조](#프로젝트-구조)
- [기여](#기여)
- [라이선스](#라이선스)

<h2 id="기능">기능</h2>

- ✅ **사용자 생성**: 백엔드 시스템에 새로운 사용자를 쉽게 추가합니다.
- ✅ **사용자 목록 조회**: 등록된 모든 사용자의 포괄적인 목록을 확인합니다.
- ✅ **사용자 삭제**: 시스템에서 기존 사용자를 제거합니다.
- ✅ **사용자 재설정**: 특정 사용자의 모든 활성 세션을 무효화하고 로그인 관련 정보를 재설정하여, 다음 로그인 시 다시 인증하도록 합니다.

<h2 id="사전-요구-사항">사전 요구 사항</h2>

시작하기 전에 시스템에 다음이 설치되어 있는지 확인하세요:
- [Go](https://go.dev/doc/install) (버전 1.22.6 이상 권장)

<h2 id="백엔드-api-구성">백엔드 API 구성</h2>

이 CLI 도구는 원격 백엔드 API와 상호 작용합니다. 사용하기 전에 API가 배포되어 접근 가능한지 확인하세요.
배포된 API Gateway 엔드포인트의 `BASE_URL`과 Lambda 백엔드에 구성된 `ADMIN_KEY`와 일치하는 `ADMIN_KEY`가 필요합니다.

<h2 id="설정">설정</h2>

CLI 애플리케이션을 로컬에 설정하려면 다음 단계를 따르세요:

1.  **저장소 클론**:
    ```bash
    git clone https://github.com/your-repo/keysim-admin.git # 실제 저장소 URL로 교체하세요
    cd keysim-admin
    ```

2.  **`.env` 파일 생성**:
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 백엔드 API 세부 정보로 채웁니다:
    ```ini
    BASE_URL=https://your-lambda-api-gateway-endpoint.execute-api.region.amazonaws.com/
    ADMIN_KEY=your_secret_admin_key_matching_lambda
    ```
    *플레이스홀더 값을 실제 API URL과 관리자 키로 교체하세요.*

3.  **종속성 설치 및 애플리케이션 빌드**:
    `keysim-admin` 디렉토리로 이동하여 다음 명령을 실행합니다:
    ```bash
    go mod tidy
    go build -o usermanager
    ```
    플랫폼별 빌드 (예: 교차 컴파일용):
    -   **Windows**: `GOOS=windows GOARCH=amd64 go build -o usermanager.exe`
    -   **macOS (Intel)**: `GOOS=darwin GOARCH=amd64 go build -o usermanager-intel`
    -   **macOS (Apple Silicon)**: `GOOS=darwin GOARCH=arm64 go build -o usermanager-arm`

<h2 id="사용법">사용법</h2>

빌드 후 터미널에서 `usermanager` 실행 파일을 실행할 수 있습니다. 모든 명령은 유사한 구조를 따릅니다:

-   **사용자 생성**:
    ```bash
    ./usermanager create [userId]
    ```
    예시: `./usermanager create newuser123`

-   **사용자 삭제**:
    ```bash
    ./usermanager delete [userId]
    ```
    예시: `./usermanager delete olduser`

-   **사용자 재설정**:
    ```bash
    ./usermanager reset [userId]
    ```
    *이 명령은 지정된 사용자의 기존 세션을 무효화하고 로그인 관련 데이터를 지워, 다시 인증하도록 요구합니다.*
    예시: `./usermanager reset compromiseduser`

-   **모든 사용자 목록 조회**:
    ```bash
    ./usermanager list
    ```

<h2 id="프로젝트-구조">프로젝트 구조</h2>

-   `main.go`: 주 애플리케이션 진입점이며, CLI 명령 정의 및 백엔드 API와의 상호 작용 로직을 포함합니다.
-   `go.mod` & `go.sum`: Go 모듈 종속성 관리 파일.
-   `.env`: `BASE_URL` 및 `ADMIN_KEY`에 대한 환경 변수 구성 파일. (보안을 위해 Git에 의해 무시됨)

<h2 id="기여">기여</h2>

기여는 언제나 환영합니다! 문제 제기 또는 Pull Request를 자유롭게 제출해주세요.

<h2 id="라이선스">라이선스</h2>

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.