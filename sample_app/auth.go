
package auth

import (
    "crypto/sha256"
    "encoding/hex"
)

// User represents an authenticated user
type User struct {
    ID       int
    Username string
    Email    string
}

// AuthService handles authentication
type AuthService struct {
    users map[string]*User
}

// NewAuthService creates a new authentication service
func NewAuthService() *AuthService {
    return &AuthService{
        users: make(map[string]*User),
    }
}

// HashPassword creates a SHA256 hash of the password
func HashPassword(password string) string {
    hash := sha256.Sum256([]byte(password))
    return hex.EncodeToString(hash[:])
}

// Authenticate verifies user credentials
func (s *AuthService) Authenticate(username, password string) (*User, bool) {
    user, exists := s.users[username]
    return user, exists
}
