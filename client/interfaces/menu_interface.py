from abc import ABC, abstractmethod
from typing import Optional


class MenuInterface(ABC):
    """Base interface for all menu components in the application."""
    
    @abstractmethod
    def run(self) -> None:
        """Execute the menu loop."""
        pass
    
    @abstractmethod
    def display_menu(self) -> None:
        """Display the menu options to the user."""
        pass
    
    @abstractmethod
    def handle_choice(self, choice: str) -> bool:
        """Process user choice and return continuation status."""
        pass
    
    def get_user_input(self, prompt: str = "Enter your choice: ") -> str:
        """Get user input with consistent prompt formatting."""
        return input(prompt)
    
    def display_header(self, title: str) -> None:
        """Display a formatted header with title."""
        print(f"\n{title}")
        print("=" * len(title))
    
    def display_footer(self, message: str = "Press Enter to continue...") -> None:
        """Display a formatted footer with optional message."""
        print(f"\n{message}")
        input() 