package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
)

const appVersion = "3.0"

var (
	baseURL  string
	adminKey string
)

// Response - API 응답을 위한 범용 구조체
type Response struct {
	Message string `json:"message"`
	Users   []User `json:"users,omitempty"`
}

// User - 사용자 정보를 담는 구조체
type User struct {
	UserID string `json:"userId"`
}

func init() {
	if err := godotenv.Load(); err != nil {
		fmt.Fprintln(os.Stderr, "Error loading .env file:", err)
	}

	baseURL = os.Getenv("BASE_URL")
	adminKey = os.Getenv("ADMIN_KEY")

	if baseURL == "" || adminKey == "" {
		fmt.Fprintln(os.Stderr, "BASE_URL and ADMIN_KEY must be set in .env file")
		os.Exit(1)
	}
}

func main() {
	rootCmd := &cobra.Command{Use: "usermanager"}

	// 명령어 정의
	rootCmd.AddCommand(
		&cobra.Command{
			Use:   "create [userId]",
			Short: "Create a new user",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { createUser(args[0]) },
		},
		&cobra.Command{
			Use:   "list",
			Short: "List all users",
			Run:   func(cmd *cobra.Command, args []string) { listUsers() },
		},
		&cobra.Command{
			Use:   "delete [userId]",
			Short: "Delete a user",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { deleteUser(args[0]) },
		},
		&cobra.Command{
			Use:   "reset [userId]",
			Short: "Reset user session and login info",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { resetUser(args[0]) },
		},
		&cobra.Command{
			Use:   "cleanup-logs",
			Short: "Remove old authentication logs",
			Run:   func(cmd *cobra.Command, args []string) { cleanupLogs() },
		},
		&cobra.Command{
			Use:   "clear-logs",
			Short: "Clear all logs and sessions",
			Run:   func(cmd *cobra.Command, args []string) { clearLogs() },
		},
	)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

// --- 명령어 실행 함수들 ---

func createUser(userId string) {
	payload := map[string]string{
		"adminKey": adminKey,
		"userId":   userId,
	}
	executeRequest("POST", "/admin/users/create", payload)
}

func listUsers() {
	payload := map[string]string{
		"adminKey": adminKey,
	}
	executeRequest("POST", "/admin/users/list", payload)
}

func deleteUser(userId string) {
	payload := map[string]string{
		"adminKey": adminKey,
		"userId":   userId,
	}
	executeRequest("POST", "/admin/users/delete", payload)
}

func resetUser(userId string) {
	payload := map[string]string{
		"adminKey": adminKey,
		"userId":   userId,
	}
	executeRequest("POST", "/admin/users/reset", payload)
}

func cleanupLogs() {
	payload := map[string]string{
		"adminKey":   adminKey,
		"appVersion": appVersion,
		"userId":     "admin",
	}
	executeRequest("POST", "/cleanup-logs", payload)
}

func clearLogs() {
	payload := map[string]string{
		"adminKey":   adminKey,
		"appVersion": appVersion,
		"userId":     "admin",
	}
	executeRequest("POST", "/clear-logs", payload)
}

// --- 핵심 요청 로직 (리팩토링하여 통합) ---
func executeRequest(method, path string, payload interface{}) {
	url := baseURL + path

	requestBody, err := json.Marshal(payload)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating request body:", err)
		return
	}

	req, err := http.NewRequest(method, url, bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating request:", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error executing request:", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error reading response body:", err)
		return
	}

	if resp.StatusCode >= 400 {
		fmt.Fprintf(os.Stderr, "Error from server (HTTP %d): %s\n", resp.StatusCode, string(body))
		return
	}

	var response Response
	if err := json.Unmarshal(body, &response); err != nil {
		fmt.Fprintln(os.Stderr, "Error parsing response JSON:", err)
		fmt.Println("Raw response:", string(body)) // 디버깅을 위해 원본 응답 출력
		return
	}

	// 결과 출력
	if response.Message != "" {
		fmt.Println("Message:", response.Message)
	}

	if len(response.Users) > 0 {
		fmt.Println("Users:")
		for _, user := range response.Users {
			fmt.Println("  -", user.UserID)
		}
	}
}
