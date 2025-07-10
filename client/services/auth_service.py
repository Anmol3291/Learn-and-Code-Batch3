from typing import Dict, Any, Optional
from jose import jwt, JWTError
from config.settings import BASE_URL, SECRET_KEY, ALGORITHM
from services.api_service import ApiService


class AuthService:
    """Service for handling user authentication operations."""
    
    def __init__(self):
        self.api_service = ApiService()
    
    def signup(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user account."""
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        return self.api_service.post("/auth/signup", data)
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and retrieve access token."""
        data = {
            "username": username,
            "password": password
        }
        return self.api_service.post("/auth/login", data)
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate JWT token."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            return {"error": f"Invalid token: {str(e)}"}
        except Exception as e:
            return {"error": f"Token processing failed: {str(e)}"} 