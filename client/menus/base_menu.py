from datetime import datetime
from interfaces.menu_interface import MenuInterface
from utils.display import DisplayUtils


class BaseMenu(MenuInterface):
    """Base menu class providing common functionality for all menus."""
    
    def __init__(self, username: str = ""):
        self.username = username
        self.display = DisplayUtils()
    
    def run(self) -> None:
        """Execute the menu loop with proper error handling."""
        try:
            while True:
                self.display_header()
                self.display_menu()
                choice = self.get_user_input()
                
                if not self.handle_choice(choice):
                    break
        except KeyboardInterrupt:
            print("\nExiting menu...")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def display_header(self, title: str = None) -> None:
        """Display the menu header with timestamp and optional title."""
        now = self.display.get_current_datetime()
        
        if self.username:
            print(f"\nWelcome to the News Aggregator application, {self.username}! Date: {now}")
        else:
            print(f"\nWelcome to the News Aggregator application! Date: {now}")
        
        if title:
            print(f"\n{title}")
            print("=" * len(title))
    
    def display_menu(self) -> None:
        """Display the menu options - to be implemented by subclasses."""
        raise NotImplementedError
    
    def handle_choice(self, choice: str) -> bool:
        """Handle user choice - to be implemented by subclasses."""
        raise NotImplementedError
    
    def display_success_message(self, message: str) -> None:
        """Display a success message with footer."""
        print(self.display.format_success_message(message))
        self.display_footer()
    
    def display_error_message(self, message: str) -> None:
        """Display an error message with footer."""
        print(self.display.format_error_message(message))
        self.display_footer()
    
    def display_info_message(self, message: str) -> None:
        """Display an info message with footer."""
        print(self.display.format_info_message(message))
        self.display_footer() 