import requests
from config.settings import Config
from models.user import User


class AuthService:
    def __init__(self, user: User):
        self.user = user
        self.base_url = Config.BASE_URL

    def signup(self, username: str, email: str, password: str) -> dict:
        try:
            response = requests.post(
                f"{self.base_url}{Config.ENDPOINTS['signup']}",
                json={"username": username, "email": email, "password": password},
            )
            return response.json()
        except Exception as e:
            return {"error": f"Signup failed: {str(e)}"}

    def login(self, username: str, password: str) -> tuple[bool, dict]:
        try:
            response = requests.post(
                f"{self.base_url}{Config.ENDPOINTS['login']}",
                json={"username": username, "password": password},
            )
            data = response.json()

            if response.status_code == 200:
                self.user.set_token(data["access_token"])
                return True, {"message": "Login successful"}
            else:
                return False, data
        except Exception as e:
            return False, {"detail": f"Login failed: {str(e)}"}
