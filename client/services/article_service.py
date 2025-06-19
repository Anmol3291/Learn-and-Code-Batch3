import requests
from config.settings import Config
from models.user import User


class ArticleService:
    def __init__(self, user: User):
        self.user = user
        self.base_url = Config.BASE_URL

    def get_articles_today(self, category: str = None) -> dict:
        try:
            endpoint = Config.ENDPOINTS["articles_today"]
            if category and category != "All":
                endpoint += f"/{category}"

            response = requests.get(
                f"{self.base_url}{endpoint}", headers=self.user.get_headers()
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch articles: {str(e)}"}

    def get_articles_by_date_range(
        self, start_date: str, end_date: str, category: str = None
    ) -> dict:
        try:
            endpoint = (
                f"{Config.ENDPOINTS['articles_date_range']}/{start_date}/{end_date}"
            )
            if category and category != "All":
                endpoint += f"/{category}"

            response = requests.get(
                f"{self.base_url}{endpoint}", headers=self.user.get_headers()
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch articles: {str(e)}"}

    def save_article(self, article_id: int) -> dict:
        try:
            response = requests.post(
                f"{self.base_url}{Config.ENDPOINTS['save_article']}",
                json={"username": self.user.username, "article_id": article_id},
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to save article: {str(e)}"}

    def get_saved_articles(self) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}{Config.ENDPOINTS['saved_articles']}/{self.user.username}",
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to fetch saved articles: {str(e)}"}

    def delete_saved_article(self, article_id: int) -> dict:
        try:
            response = requests.delete(
                f"{self.base_url}{Config.ENDPOINTS['saved_articles']}",
                json={"username": self.user.username, "article_id": article_id},
                headers=self.user.get_headers(),
            )
            return response.json()
        except Exception as e:
            return {"error": f"Failed to delete article: {str(e)}"}
