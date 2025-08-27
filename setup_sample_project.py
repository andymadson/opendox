# Create setup_sample_project.py
"""Setup a sample multi-language project for testing."""
from pathlib import Path

sample_project = Path("sample_app")
sample_project.mkdir(exist_ok=True)

# Backend (Python)
backend = sample_project / "backend"
backend.mkdir(exist_ok=True)

(backend / "app.py").write_text('''
"""Main application module."""
from flask import Flask, jsonify
from typing import Dict, Any

app = Flask(__name__)

class UserService:
    """Service for managing users."""
    
    def __init__(self):
        self.users = []
    
    def add_user(self, name: str, email: str) -> Dict[str, Any]:
        """Add a new user to the system.
        
        Args:
            name: User's full name
            email: User's email address
            
        Returns:
            Dictionary containing user data
        """
        user = {"id": len(self.users) + 1, "name": name, "email": email}
        self.users.append(user)
        return user
    
    def get_all_users(self) -> list:
        """Get all users in the system."""
        return self.users

@app.route('/api/users')
def get_users():
    """API endpoint to get all users."""
    service = UserService()
    return jsonify(service.get_all_users())
''')

# Frontend (JavaScript/TypeScript)
frontend = sample_project / "frontend"
frontend.mkdir(exist_ok=True)

(frontend / "api.js").write_text('''
/**
 * API client for backend communication
 */
class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    /**
     * Fetch all users from the API
     * @returns {Promise<Array>} List of users
     */
    async getUsers() {
        const response = await fetch(`${this.baseUrl}/api/users`);
        return response.json();
    }
    
    /**
     * Create a new user
     * @param {Object} userData - User data to create
     * @returns {Promise<Object>} Created user
     */
    async createUser(userData) {
        const response = await fetch(`${this.baseUrl}/api/users`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userData)
        });
        return response.json();
    }
}

export default ApiClient;
''')

(frontend / "components.tsx").write_text('''
import React, { useState, useEffect } from 'react';

interface User {
    id: number;
    name: string;
    email: string;
}

interface UserListProps {
    apiClient: any;
}

/**
 * Component to display a list of users
 */
const UserList: React.FC<UserListProps> = ({ apiClient }) => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadUsers();
    }, []);
    
    const loadUsers = async () => {
        try {
            const data = await apiClient.getUsers();
            setUsers(data);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <h2>Users</h2>
            {users.map(user => (
                <div key={user.id}>
                    {user.name} - {user.email}
                </div>
            ))}
        </div>
    );
};

export default UserList;
''')

# Services (Go)
(sample_project / "auth.go").write_text('''
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
''')

print(f"✅ Created sample project in '{sample_project}/'")
print("\nNow generate documentation for it:")
print(f"  opendox generate {sample_project} --output sample_docs --max-files 20")