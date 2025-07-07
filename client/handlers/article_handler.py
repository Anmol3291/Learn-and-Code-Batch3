from typing import Optional
from services.article_service import ArticleService
from utils.display import DisplayUtils
from config.settings import DEFAULT_PAGE_SIZE
from services.api_service import ApiService


class ArticleHandler:
    """Handler for article-related operations including headlines and basic interactions."""
    
    def __init__(self, token: str, username: str):
        self.article_service = ArticleService(token, username)
        self.username = username
        self.display = DisplayUtils()
    
    def headlines_menu(self) -> bool:
        """Display headlines menu with navigation options."""
        while True:
            print("\nHEADLINES MENU")
            print("=" * 14)
            print("1. Today's Headlines")
            print("2. Date range")
            print("3. Back")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.display_articles("All", "today")
            elif choice == "2":
                self.date_range_menu()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        
        return True  # Return to user menu
    
    def date_range_menu(self) -> None:
        """Handle date range selection for article filtering."""
        print("\nDATE RANGE SELECTION")
        print("=" * 20)
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        
        if not start or not end:
            print("Both start and end dates are required.")
            return
            
        self.show_category_menu("range", start, end)
    
    def show_category_menu(self, date_type: str, start: Optional[str] = None, 
                          end: Optional[str] = None) -> None:
        """Show category selection menu for article filtering."""
        print("\nCATEGORY SELECTION")
        print("=" * 18)
        
        api_service = ApiService()
        categories_result = api_service.get("/categories")
        if "error" in categories_result:
            print(f"Failed to fetch categories: {categories_result['error']}")
            return
        categories_raw = categories_result.get("categories", [])
        categories = [cat[1] for cat in categories_raw]  # Extract just the name
        
        print("1. All")
        for idx, category in enumerate(categories, 2):
            print(f"{idx}. {category}")
        
        choice = input("Enter choice: ").strip()
        try:
            choice_num = int(choice)
            if choice_num == 1:
                category = "All"
            elif 2 <= choice_num <= len(categories) + 1:
                category = categories[choice_num - 2]
            else:
                print("Invalid category choice.")
                return
            self.display_articles(category, date_type, start, end)
        except ValueError:
            print("Invalid category choice.")
    
    def display_articles(self, category: str, date_type: str, 
                        start: Optional[str] = None, end: Optional[str] = None) -> None:
        """Display articles with pagination and interaction options."""
        page = 1
        
        while True:
            print(f"\nHEADLINES - {category.upper()}")
            print("=" * (20 + len(category)))
            
            result = self.article_service.get_articles(category, date_type, start, end, page)
            
            if "error" in result:
                print(f"Error fetching articles: {result['error']}")
                input("Press Enter to continue...")
                break
            
            articles = result.get("articles", [])
            pagination = result.get("pagination", {})
            
            if not articles:
                print("No articles found.")
                input("Press Enter to continue...")
                break
            
            for article in articles:
                self.display_article(article)
            
            self._display_pagination_info(pagination)
            self._display_article_options(pagination, page)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.save_article()
            elif choice == "2":
                self.like_article()
            elif choice == "3":
                self.dislike_article()
            elif choice == "4":
                break
            elif choice == "5" and pagination and pagination.get("has_prev", False):
                page = pagination.get("page", 1) - 1
            elif choice == "6" and pagination and pagination.get("has_next", False):
                page = pagination.get("page", 1) + 1
            else:
                print("Invalid choice.")
    
    def display_article(self, article: dict) -> None:
        """Display a single article with formatted output."""
        print(f"\nArticle ID: {article['id']}")
        print(f"Title: {article['title']}")
        print(f"Content: {self.display.truncate_text(article['content'], 150)}...")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        
        if article.get('category'):
            print(f"Category: {article['category']}")
        
        stats = self.article_service.get_article_stats(article['id'])
        if "error" not in stats:
            likes = stats.get("likes", 0)
            dislikes = stats.get("dislikes", 0)
            print(f"Likes: {likes} | Dislikes: {dislikes}")
        
        print("-" * self.display.SEPARATOR_LENGTH)
    
    def save_article(self) -> None:
        """Save an article to user's collection."""
        article_id = input("Enter Article ID to save: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.save_article(article_id)
        if "error" in result:
            print(f"Failed to save article: {result['error']}")
        else:
            print("Article saved successfully.")
        
        input("Press Enter to continue...")
    
    def like_article(self) -> None:
        """Like an article."""
        article_id = input("Enter Article ID to like: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.like_article(article_id)
        if "error" in result:
            print(f"Failed to like article: {result['error']}")
        else:
            print("Article liked successfully.")
        
        input("Press Enter to continue...")
    
    def dislike_article(self) -> None:
        """Dislike an article."""
        article_id = input("Enter Article ID to dislike: ").strip()
        
        if not article_id:
            print("Article ID is required.")
            return
            
        result = self.article_service.dislike_article(article_id)
        if "error" in result:
            print(f"Failed to dislike article: {result['error']}")
        else:
            print("Article disliked successfully.")
        
        input("Press Enter to continue...")
    
    def _display_pagination_info(self, pagination: dict) -> None:
        """Display pagination information."""
        if pagination:
            total_pages = pagination.get("pages", 1)
            current_page = pagination.get("page", 1)
            total_articles = pagination.get("total", 0)
            
            print(f"\nPage {current_page} of {total_pages} (Total: {total_articles} articles)")
    
    def _display_article_options(self, pagination: dict, current_page: int) -> None:
        """Display available article interaction options."""
        print("\nOptions:")
        print("1. Save Article")
        print("2. Like Article")
        print("3. Dislike Article")
        print("4. Back to Menu")
        
        if pagination:
            if pagination.get("has_prev", False):
                print("5. Previous Page")
            if pagination.get("has_next", False):
                print("6. Next Page")
    
    def saved_articles_menu(self) -> bool:
        """Delegate to SavedArticlesHandler."""
        from handlers.saved_articles_handler import SavedArticlesHandler
        handler = SavedArticlesHandler(self.article_service.api_service.headers.get("Authorization").split()[1], self.username)
        handler.saved_articles_menu()
        return True  # Return to user menu
    
    def reactions_menu(self) -> bool:
        """Delegate to ReactionsHandler."""
        from handlers.reactions_handler import ReactionsHandler
        handler = ReactionsHandler(self.article_service.api_service.headers.get("Authorization").split()[1], self.username)
        handler.reactions_menu()
        return True  # Return to user menu 