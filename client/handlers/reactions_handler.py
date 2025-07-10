from services.article_service import ArticleService
from utils.display import DisplayUtils


class ReactionsHandler:
    """Handler for article reactions including likes and dislikes management."""
    
    def __init__(self, token: str, username: str):
        self.article_service = ArticleService(token, username)
        self.username = username
        self.display = DisplayUtils()
    
    def reactions_menu(self) -> None:
        """Display reactions menu for liked and disliked articles."""
        while True:
            print("\nREACTIONS MENU")
            print("=" * 15)
            print("1. View Liked Articles")
            print("2. View Disliked Articles")
            print("3. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.view_liked_articles()
            elif choice == "2":
                self.view_disliked_articles()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_liked_articles(self) -> None:
        """Display user's liked articles with pagination."""
        page = 1
        
        while True:
            print(f"\nLIKED ARTICLES")
            print("=" * 14)
            
            result = self.article_service.get_liked_articles(page)
            
            if "error" in result:
                print(f"Error fetching liked articles: {result['error']}")
                input("Press Enter to continue...")
                break
            
            articles = result.get("articles", [])
            pagination = result.get("pagination", {})
            
            if not articles:
                print("No liked articles found.")
                input("Press Enter to continue...")
                break
            
            for article in articles:
                self.display_article(article)
            
            self._display_pagination_info(pagination)
            self._display_liked_articles_options(pagination, page)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.unlike_article()
            elif choice == "2":
                break
            elif choice == "3" and pagination and pagination.get("has_prev", False):
                page = pagination.get("page", 1) - 1
            elif choice == "4" and pagination and pagination.get("has_next", False):
                page = pagination.get("page", 1) + 1
            else:
                print("Invalid choice.")
    
    def view_disliked_articles(self) -> None:
        """Display user's disliked articles with pagination."""
        page = 1
        
        while True:
            print(f"\nDISLIKED ARTICLES")
            print("=" * 16)
            
            result = self.article_service.get_disliked_articles(page)
            
            if "error" in result:
                print(f"Error fetching disliked articles: {result['error']}")
                input("Press Enter to continue...")
                break
            
            articles = result.get("articles", [])
            pagination = result.get("pagination", {})
            
            if not articles:
                print("No disliked articles found.")
                input("Press Enter to continue...")
                break
            
            for article in articles:
                self.display_article(article)
            
            self._display_pagination_info(pagination)
            self._display_disliked_articles_options(pagination, page)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.remove_dislike()
            elif choice == "2":
                break
            elif choice == "3" and pagination and pagination.get("has_prev", False):
                page = pagination.get("page", 1) - 1
            elif choice == "4" and pagination and pagination.get("has_next", False):
                page = pagination.get("page", 1) + 1
            else:
                print("Invalid choice.")
    
    def display_article(self, article: dict) -> None:
        """Display a single article with reaction information."""
        print(f"\nArticle ID: {article['id']}")
        print(f"Title: {article['title']}")
        print(f"Content: {self.display.truncate_text(article['content'], 150)}...")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        
        if article.get('category'):
            print(f"Category: {article['category']}")
        
        print("-" * self.display.SEPARATOR_LENGTH)
    
    def unlike_article(self) -> None:
        """Remove like from an article."""
        article_id = input("Enter Article ID to unlike: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.unlike_article(article_id)
        if "error" in result:
            print(f"Failed to unlike article: {result['error']}")
        else:
            print("Article unliked successfully.")
        
        input("Press Enter to continue...")
    
    def remove_dislike(self) -> None:
        """Remove dislike from an article."""
        article_id = input("Enter Article ID to remove dislike: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.remove_dislike(article_id)
        if "error" in result:
            print(f"Failed to remove dislike: {result['error']}")
        else:
            print("Dislike removed successfully.")
        
        input("Press Enter to continue...")
    
    def _display_pagination_info(self, pagination: dict) -> None:
        """Display pagination information for reactions."""
        if pagination:
            total_pages = pagination.get("pages", 1)
            current_page = pagination.get("page", 1)
            total_articles = pagination.get("total", 0)
            
            print(f"\nPage {current_page} of {total_pages} (Total: {total_articles} articles)")
    
    def _display_liked_articles_options(self, pagination: dict, current_page: int) -> None:
        """Display available options for liked articles."""
        print("\nOptions:")
        print("1. Unlike Article")
        print("2. Back to Menu")
        
        if pagination:
            if pagination.get("has_prev", False):
                print("3. Previous Page")
            if pagination.get("has_next", False):
                print("4. Next Page")
    
    def _display_disliked_articles_options(self, pagination: dict, current_page: int) -> None:
        """Display available options for disliked articles."""
        print("\nOptions:")
        print("1. Remove Dislike")
        print("2. Back to Menu")
        
        if pagination:
            if pagination.get("has_prev", False):
                print("3. Previous Page")
            if pagination.get("has_next", False):
                print("4. Next Page") 