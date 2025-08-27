
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
