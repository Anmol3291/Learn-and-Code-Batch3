from typing import Optional
from services.article_service import ArticleService
from utils.display import DisplayUtils
from datetime import datetime
from services.api_service import ApiService


class SearchHandler:
    """Handler for article search operations with advanced filtering capabilities."""
    
    def __init__(self, token: str, username: str):
        self.article_service = ArticleService(token, username)
        self.username = username
        self.display = DisplayUtils()
    
    def search_menu(self) -> bool:
        """Display search menu with navigation options."""
        while True:
            print("\nSEARCH MENU")
            print("=" * 11)
            print("1. Search Articles")
            print("2. Advanced Search")
            print("3. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.simple_search()
            elif choice == "2":
                self.advanced_search()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        
        return True  # Return to user menu
    
    def simple_search(self) -> None:
        """Perform simple keyword-based search."""
        print("\nSIMPLE SEARCH")
        print("=" * 13)
        query = input("Enter search query: ").strip()
        
        if not query:
            print("Search query cannot be empty.")
            input("Press Enter to continue...")
            return
        
        self.perform_search(query)
    
    def advanced_search(self) -> None:
        """Perform advanced search with multiple filters."""
        print("\nADVANCED SEARCH")
        print("=" * 15)
        
        query = input("Enter search query: ").strip()
        if not query:
            print("Search query cannot be empty.")
            input("Press Enter to continue...")
            return
        
        category = self.get_category_choice()
        date_from = input("Date from (YYYY-MM-DD, optional): ").strip()
        date_to = input("Date to (YYYY-MM-DD, optional): ").strip()
        
        if date_from and not self.is_valid_date(date_from):
            print("Invalid date format for 'Date from'. Use YYYY-MM-DD format.")
            input("Press Enter to continue...")
            return
            
        if date_to and not self.is_valid_date(date_to):
            print("Invalid date format for 'Date to'. Use YYYY-MM-DD format.")
            input("Press Enter to continue...")
            return
        
        self.perform_search(query, category, date_from, date_to)
    
    def is_valid_date(self, date_string: str) -> bool:
        """Validate date format YYYY-MM-DD."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def get_category_choice(self) -> Optional[str]:
        """Get category choice from user input."""
        print("\nChoose Category (optional):")
        
        api_service = ApiService()
        categories_result = api_service.get("/categories")
        if "error" in categories_result:
            print(f"Failed to fetch categories: {categories_result['error']}")
            return None
        categories_raw = categories_result.get("categories", [])
        categories = [cat[1] for cat in categories_raw]  # Extract just the name
        
        print("1. All Categories")
        for idx, category in enumerate(categories, 2):
            print(f"{idx}. {category}")
        
        choice = input(f"Enter choice (1-{len(categories)+1}): ").strip()
        try:
            choice_num = int(choice)
            if choice_num == 1:
                return None  # All Categories
            elif 2 <= choice_num <= len(categories) + 1:
                return categories[choice_num - 2]
            else:
                print("Invalid choice. Using 'All Categories'.")
                return None
        except ValueError:
            print("Invalid choice. Using 'All Categories'.")
            return None
    
    def perform_search(self, query: str, category: Optional[str] = None, 
                      date_from: Optional[str] = None, date_to: Optional[str] = None) -> None:
        """Perform search with pagination and result display."""
        page = 1
        
        while True:
            print(f"\nSEARCH RESULTS - \"{query}\"")
            print("=" * (20 + len(query)))
            
            search_data = {
                "query": query,
                "category": category,
                "date_from": date_from if date_from else None,
                "date_to": date_to if date_to else None
            }
            
            result = self.article_service.search_articles(search_data, page)
            
            if "error" in result:
                print(f"Search failed: {result['error']}")
                input("Press Enter to continue...")
                break
            
            articles = result.get("articles", [])
            pagination = result.get("pagination", {})
            
            if not articles:
                print("No articles found matching your search.")
                print("Suggestions:")
                print("   - Use different keywords")
                print("   - Check spelling")
                print("   - Use broader terms")
                print("   - Try advanced search with different filters")
                input("Press Enter to continue...")
                break
            
            for article in articles:
                self.display_article(article)
            
            self._display_pagination_info(pagination)
            self._display_search_options(pagination, page)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.save_article()
            elif choice == "2":
                break
            elif choice == "3" and pagination and pagination.get("has_prev", False):
                page = pagination.get("page", 1) - 1
            elif choice == "4" and pagination and pagination.get("has_next", False):
                page = pagination.get("page", 1) + 1
            else:
                print("Invalid choice.")
    
    def display_article(self, article: dict) -> None:
        """Display a single article with formatted output."""
        print(f"\nArticle ID: {article['id']}")
        print(f"Title: {article['title']}")
        print(f"Content: {self.display.truncate_text(article['content'], 150)}...")
        print(f"Source: {article['source']}")
        
        if article.get('category'):
            print(f"Category: {article['category']}")
        if article.get('published_date'):
            print(f"Published: {article['published_date']}")
            
        print(f"URL: {article['url']}")
        print("-" * self.display.SEPARATOR_LENGTH)
    
    def save_article(self) -> None:
        """Save an article from search results."""
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
    
    def _display_pagination_info(self, pagination: dict) -> None:
        """Display pagination information for search results."""
        if pagination:
            total_pages = pagination.get("pages", 1)
            current_page = pagination.get("page", 1)
            total_articles = pagination.get("total", 0)
            
            print(f"\nPage {current_page} of {total_pages} (Total: {total_articles} articles)")
    
    def _display_search_options(self, pagination: dict, current_page: int) -> None:
        """Display available options for search results."""
        print("\nOptions:")
        print("1. Save Article")
        print("2. Back to Search")
        
        if pagination:
            if pagination.get("has_prev", False):
                print("3. Previous Page")
            if pagination.get("has_next", False):
                print("4. Next Page") 