from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ArticleInterface(ABC):
    """Interface defining contract for article-related operations."""
    
    @abstractmethod
    def display_articles(self, category: str, date_type: str, 
                        start: Optional[str] = None, end: Optional[str] = None) -> None:
        """Display articles filtered by category and date range."""
        pass
    
    @abstractmethod
    def save_article(self, article_id: str) -> bool:
        """Save an article to user's collection."""
        pass
    
    @abstractmethod
    def delete_article(self, article_id: str) -> bool:
        """Remove an article from user's saved collection."""
        pass
    
    @abstractmethod
    def like_article(self, article_id: str) -> bool:
        """Mark an article as liked by the user."""
        pass
    
    @abstractmethod
    def dislike_article(self, article_id: str) -> bool:
        """Mark an article as disliked by the user."""
        pass
    
    @abstractmethod
    def get_article_stats(self, article_id: str) -> Dict[str, Any]:
        """Retrieve article engagement statistics."""
        pass 