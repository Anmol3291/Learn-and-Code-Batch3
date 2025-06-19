from jose import jwt
from config.settings import Config


class User:
    def __init__(self):
        self.token = None
        self.username = None
        self.role = None
        self.is_authenticated = False

    def set_token(self, token: str):
        self.token = token
        try:
            payload = jwt.decode(
                token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM]
            )
            self.username = payload.get("username")
            self.role = payload.get("role")
            self.is_authenticated = True
        except Exception:
            self.clear_session()

    def clear_session(self):
        self.token = None
        self.username = None
        self.role = None
        self.is_authenticated = False

    def get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def is_admin(self):
        return self.role == "admin"
