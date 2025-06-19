import requests
from config.settings import Config
from models.user import User


class AdminService:
    def __init__(self, user: User):
        self.user = user
        self.base_url = Config.BASE_URL

    def get_servers_status(self) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}{Config.ENDPOINTS['servers']}",
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch servers: {str(e)}"}

    def get_server_details(self) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}{Config.ENDPOINTS['server_details']}",
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch server details: {str(e)}"}

    def update_server_api(self, server_id: str, api_key: str) -> dict:
        try:
            response = requests.put(
                f"{self.base_url}{Config.ENDPOINTS['update_server']}/{server_id}",
                json={"api_key": api_key},
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to update server: {str(e)}"}

    def add_category(self, name: str) -> dict:
        try:
            response = requests.post(
                f"{self.base_url}{Config.ENDPOINTS['add_category']}",
                json={"name": name},
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to add category: {str(e)}"}
