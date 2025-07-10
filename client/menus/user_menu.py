from menus.base_menu import BaseMenu
from handlers.article_handler import ArticleHandler
from handlers.search_handler import SearchHandler
from handlers.notification_handler import NotificationHandler


class UserMenu(BaseMenu):
    """User menu providing access to all user-specific features."""
    
    def __init__(self, token: str, username: str):
        super().__init__(username)
        self.article_handler = ArticleHandler(token, username)
        self.search_handler = SearchHandler(token, username)
        self.notification_handler = NotificationHandler(token, username)
    
    def display_menu(self) -> None:
        """Display the user menu options."""
        print("USER MENU")
        print("=" * 9)
        print("1. Headlines")
        print("2. Saved Articles")
        print("3. Liked/Disliked Articles")
        print("4. Search")
        print("5. Notifications")
        print("6. Logout")
    
    def handle_choice(self, choice: str) -> bool:
        """Process user menu choices and route to appropriate handlers."""
        menu_actions = {
            "1": self.article_handler.headlines_menu,
            "2": self.article_handler.saved_articles_menu,
            "3": self.article_handler.reactions_menu,
            "4": self.search_handler.search_menu,
            "5": self.notification_handler.notifications_menu,
            "6": self.logout
        }
        
        action = menu_actions.get(choice)
        if action:
            return action()
        else:
            self.display_error_message("Invalid choice. Please try again.")
            return True
    
    def logout(self) -> bool:
        """Handle user logout with confirmation."""
        print(f"\nLogging out {self.username}...")
        print("Thank you for using the News Aggregator!")
        return False 