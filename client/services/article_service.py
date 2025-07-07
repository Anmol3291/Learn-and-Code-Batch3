from typing import Dict, Any, Optional, List
from services.api_service import ApiService
from config.settings import DEFAULT_PAGE_SIZE


class ArticleService:
    """Service for handling article-related operations and API interactions."""
    
    def __init__(self, token: str, username: str):
        self.api_service = ApiService(token)
        self.username = username
    
    def get_articles(self, category: str, date_type: str, 
                    start: Optional[str] = None, end: Optional[str] = None,
                    page: int = 1, limit: int = DEFAULT_PAGE_SIZE) -> Dict[str, Any]:
        """Retrieve articles filtered by category and date range."""
        params = {"page": page, "limit": limit}
        endpoint = self._build_articles_endpoint(category, date_type, start, end)
        return self.api_service.get(endpoint, params)
    
    def get_saved_articles(self, page: int = 1, limit: int = DEFAULT_PAGE_SIZE) -> Dict[str, Any]:
        """Retrieve user's saved articles with pagination."""
        params = {"page": page, "limit": limit}
        return self.api_service.get(f"/saved-articles/{self.username}", params)
    
    def save_article(self, article_id: str) -> Dict[str, Any]:
        """Save an article to user's collection."""
        data = {"username": self.username, "article_id": article_id}
        return self.api_service.post("/save-article", data)
    
    def delete_saved_article(self, article_id: str) -> Dict[str, Any]:
        """Remove an article from user's saved collection."""
        return self.api_service.delete(f"/saved-articles/{self.username}/{article_id}")
    
    def like_article(self, article_id: str) -> Dict[str, Any]:
        """Mark an article as liked by the user."""
        data = {"username": self.username, "article_id": article_id}
        return self.api_service.post("/articles/like", data)
    
    def dislike_article(self, article_id: str) -> Dict[str, Any]:
        """Mark an article as disliked by the user."""
        data = {"username": self.username, "article_id": article_id}
        return self.api_service.post("/articles/dislike", data)
    
    def unlike_article(self, article_id: str) -> Dict[str, Any]:
        """Remove like from an article."""
        data = {"username": self.username, "article_id": article_id}
        return self.api_service.delete("/articles/like", data)
    
    def remove_dislike(self, article_id: str) -> Dict[str, Any]:
        """Remove dislike from an article."""
        data = {"username": self.username, "article_id": article_id}
        return self.api_service.delete("/articles/dislike", data)
    
    def get_liked_articles(self, page: int = 1, limit: int = DEFAULT_PAGE_SIZE) -> Dict[str, Any]:
        """Retrieve user's liked articles with pagination."""
        params = {"page": page, "limit": limit}
        return self.api_service.get(f"/articles/liked/{self.username}", params)
    
    def get_disliked_articles(self, page: int = 1, limit: int = DEFAULT_PAGE_SIZE) -> Dict[str, Any]:
        """Retrieve user's disliked articles with pagination."""
        params = {"page": page, "limit": limit}
        return self.api_service.get(f"/articles/disliked/{self.username}", params)
    
    def get_article_stats(self, article_id: str) -> Dict[str, Any]:
        """Retrieve article engagement statistics."""
        return self.api_service.get(f"/articles/{article_id}/stats")
    
    def get_categories(self) -> List[str]:
        """Retrieve all available article categories."""
        result = self.api_service.get("/categories")
        return result.get("categories", [])
    
    def search_articles(self, search_data: Dict[str, Any], page: int = 1, 
                       limit: int = DEFAULT_PAGE_SIZE) -> Dict[str, Any]:
        """Search articles using specified filters and criteria."""
        params = {"page": page, "limit": limit}
        return self.api_service.post("/search", search_data, params)
    
    def _build_articles_endpoint(self, category: str, date_type: str, 
                                start: Optional[str], end: Optional[str]) -> str:
        """Build the appropriate endpoint URL based on filters."""
        if date_type == "today":
            return f"/articles/today/{category}" if category != "All" else "/articles/today"
        else:
            base_endpoint = f"/articles/date-range/{start}/{end}"
            return f"{base_endpoint}/{category}" if category != "All" else base_endpoint 