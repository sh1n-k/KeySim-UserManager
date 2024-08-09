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

var (
	baseURL  string
	adminKey string
)

type Response struct {
	Message string `json:"message"`
	Users   []User `json:"users,omitempty"`
}

type User struct {
	UserID string `json:"userId"`
}

func init() {
	if err := godotenv.Load(); err != nil {
		fmt.Fprintln(os.Stderr, "Error loading .env file")
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
	rootCmd.AddCommand(
		&cobra.Command{
			Use:   "create [userId]",
			Short: "Create a new user",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { executeRequest("POST", "/user", args[0]) },
		},
		&cobra.Command{
			Use:   "delete [userId]",
			Short: "Delete a user",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { executeRequest("DELETE", "/user", args[0]) },
		},
		&cobra.Command{
			Use:   "reset [userId]",
			Short: "Reset user key",
			Args:  cobra.ExactArgs(1),
			Run:   func(cmd *cobra.Command, args []string) { executeRequest("PUT", "/user", args[0]) },
		},
		&cobra.Command{
			Use:   "list",
			Short: "List all users",
			Run:   func(cmd *cobra.Command, args []string) { executeRequest("POST", "/users", "") },
		},
	)
	rootCmd.Execute()
}

func executeRequest(method, path, userId string) {
	url := baseURL + path
	requestBody, _ := json.Marshal(map[string]string{
		"userId":  userId,
		"authKey": adminKey,
	})

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
		fmt.Fprintln(os.Stderr, "Error reading response:", err)
		return
	}

	var response Response
	if err := json.Unmarshal(body, &response); err != nil {
		fmt.Fprintln(os.Stderr, "Error parsing response:", err)
		return
	}

	if response.Message != "" {
		fmt.Println("Response:", response.Message)
	}

	if len(response.Users) > 0 {
		fmt.Println("Users:")
		for _, user := range response.Users {
			fmt.Println("\t" + user.UserID)
		}
	}
}
