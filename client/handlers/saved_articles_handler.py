from services.article_service import ArticleService
from utils.display import DisplayUtils


class SavedArticlesHandler:
    """Handler for saved articles operations and management."""
    
    def __init__(self, token: str, username: str):
        self.article_service = ArticleService(token, username)
        self.username = username
        self.display = DisplayUtils()
    
    def saved_articles_menu(self) -> None:
        """Display saved articles menu with pagination."""
        page = 1
        
        while True:
            print(f"\nSAVED ARTICLES")
            print("=" * 14)
            
            result = self.article_service.get_saved_articles(page)
            
            if "error" in result:
                print(f"Error fetching saved articles: {result['error']}")
                input("Press Enter to continue...")
                break
            
            articles = result.get("articles", [])
            pagination = result.get("pagination", {})
            
            if not articles:
                print("No saved articles found.")
                input("Press Enter to continue...")
                break
            
            for article in articles:
                self.display_article(article)
            
            self._display_pagination_info(pagination)
            self._display_saved_articles_options(pagination, page)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.delete_saved_article()
            elif choice == "2":
                break
            elif choice == "3" and pagination and pagination.get("has_prev", False):
                page = pagination.get("page", 1) - 1
            elif choice == "4" and pagination and pagination.get("has_next", False):
                page = pagination.get("page", 1) + 1
            else:
                print("Invalid choice.")
    
    def display_article(self, article: dict) -> None:
        """Display a single saved article."""
        print(f"\nArticle ID: {article['id']}")
        print(f"Title: {article['title']}")
        print(f"Content: {self.display.truncate_text(article['content'], 150)}...")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        
        if article.get('category'):
            print(f"Category: {article['category']}")
        
        print("-" * self.display.SEPARATOR_LENGTH)
    
    def delete_saved_article(self) -> None:
        """Delete a saved article from user's collection."""
        article_id = input("Enter Article ID to delete: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.delete_saved_article(article_id)
        if "error" in result:
            print(f"Failed to delete article: {result['error']}")
        else:
            print("Article deleted successfully.")
        
        input("Press Enter to continue...")
    
    def _display_pagination_info(self, pagination: dict) -> None:
        """Display pagination information for saved articles."""
        if pagination:
            total_pages = pagination.get("pages", 1)
            current_page = pagination.get("page", 1)
            total_articles = pagination.get("total", 0)
            
            print(f"\nPage {current_page} of {total_pages} (Total: {total_articles} articles)")
    
    def _display_saved_articles_options(self, pagination: dict, current_page: int) -> None:
        """Display available options for saved articles."""
        print("\nOptions:")
        print("1. Delete Article")
        print("2. Back to Menu")
        
        if pagination:
            if pagination.get("has_prev", False):
                print("3. Previous Page")
            if pagination.get("has_next", False):
                print("4. Next Page") 