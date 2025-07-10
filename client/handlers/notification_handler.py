from typing import Dict, Any, List
from services.api_service import ApiService
from utils.display import DisplayUtils


class NotificationHandler:
    """Handler for notification operations and configuration management."""
    
    def __init__(self, token: str, username: str):
        self.api_service = ApiService(token)
        self.username = username
        self.display = DisplayUtils()
    
    def notifications_menu(self) -> bool:
        """Display notifications menu with navigation options."""
        while True:
            print("\nNOTIFICATIONS MENU")
            print("=" * 19)
            print("1. View Notifications")
            print("2. Configure Notifications")
            print("3. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                self.configure_notifications()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        
        return True  # Return to user menu
    
    def view_notifications(self) -> None:
        """Display user notifications with management options."""
        while True:
            print("\nVIEW NOTIFICATIONS")
            print("=" * 18)
            
            result = self.api_service.get(f"/notifications/{self.username}")
            
            if "error" in result:
                print(f"Failed to fetch notifications: {result['error']}")
                input("Press Enter to continue...")
                return
            
            notifications = result.get("notifications", [])
            
            if not notifications:
                print("No notifications found.")
                input("Press Enter to continue...")
                return
            
            for i, notification in enumerate(notifications, 1):
                print(f"\n{i}. {notification['notification_type'].upper()} NOTIFICATION")
                print(f"   {notification['message']}")
                if notification.get('article_title'):
                    print(f"   Article: {notification['article_title']}")
                if notification.get('article_category'):
                    print(f"   Category: {notification['article_category']}")
                print(f"   Sent: {self.display.format_datetime(notification['sent_at'])}")
                print("-" * self.display.SHORT_SEPARATOR_LENGTH)
            
            print("\nOptions:")
            print("1. Delete All Notifications")
            print("2. Back to Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.delete_all_notifications()
                break
            elif choice == "2":
                break
            else:
                print("Invalid choice.")
    
    def configure_notifications(self) -> None:
        """Configure notification settings for categories and keywords."""
        while True:
            print("\nCONFIGURE NOTIFICATIONS")
            print("=" * 23)
            
            config_result = self.api_service.get(f"/notifications/config/{self.username}")
            
            if "error" in config_result:
                print(f"Failed to fetch notification config: {config_result['error']}")
                input("Press Enter to continue...")
                break
            
            config = config_result.get("config", [])
            # Ensure config is a list of (category, enabled) pairs
            config_dict = {cat: enabled for cat, enabled in config}
            
            categories_result = self.api_service.get("/categories")
            if "error" in categories_result:
                print(f"Failed to fetch categories: {categories_result['error']}")
                input("Press Enter to continue...")
                break
            
            # categories is a list of (id, name, created_at) tuples
            categories_raw = categories_result.get("categories", [])
            categories = [cat[1] for cat in categories_raw]  # Extract just the name
            
            for i, category in enumerate(categories, 1):
                enabled = config_dict.get(category, False)
                status = "Enabled" if enabled else "Disabled"
                print(f"{i}. {category} - {status}")
            
            print(f"{len(categories) + 1}. Keywords - Configured")
            print(f"{len(categories) + 2}. Back")
            
            choice = input("Enter your option: ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    selected_category = categories[choice_num - 1]
                    current_status = config_dict.get(selected_category, False)
                    self.toggle_category_notification(selected_category, not current_status)
                elif choice_num == len(categories) + 1:
                    self.configure_keywords()
                elif choice_num == len(categories) + 2:
                    break
            else:
                print("Invalid choice. Please enter a number.")
    
    def toggle_category_notification(self, category: str, enabled: bool) -> None:
        """Toggle category notification setting."""
        print(f"\nCONFIGURE - {category.upper()}")
        print("=" * (15 + len(category)))
        
        status = "enable" if enabled else "disable"
        print(f"Do you want to {status} notifications for {category}?")
        print("1. Yes")
        print("2. No")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            data = {
                "username": self.username,
                "category": category,
                "enabled": enabled
            }
            
            result = self.api_service.post("/notifications/config", data)
            
            if "error" in result:
                print(f"Failed to update {category} notifications: {result['error']}")
            else:
                status_text = "enabled" if enabled else "disabled"
                print(f"{category} notifications {status_text} successfully.")
            
            input("Press Enter to continue...")
        else:
            print("Configuration cancelled.")
            input("Press Enter to continue...")
    
    def configure_keywords(self) -> None:
        """Configure notification keywords for personalized alerts."""
        print("\nCONFIGURE KEYWORDS")
        print("=" * 18)
        print("Enter keywords separated by commas (e.g., Tesla, AI, Technology):")
        
        keywords_input = input("Keywords: ").strip()
        
        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
            
            data = {
                "username": self.username,
                "keywords": keywords
            }
            
            result = self.api_service.post("/keywords", data)
            
            if "error" in result:
                print(f"Failed to update keywords: {result['error']}")
            else:
                print(f"Keywords updated successfully: {', '.join(keywords)}")
            
            input("Press Enter to continue...")
        else:
            print("No keywords entered. Configuration cancelled.")
            input("Press Enter to continue...")
    
    def delete_all_notifications(self) -> None:
        """Delete all notifications for the user with confirmation."""
        print("\nDELETE ALL NOTIFICATIONS")
        print("=" * 24)
        print("Are you sure you want to delete all notifications?")
        print("1. Yes, delete all")
        print("2. No, cancel")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            result = self.api_service.delete(f"/notifications/{self.username}")
            
            if "error" in result:
                print(f"Failed to delete notifications: {result['error']}")
            else:
                print("All notifications deleted successfully.")
            
            input("Press Enter to continue...")
        else:
            print("Deletion cancelled.")
            input("Press Enter to continue...") 