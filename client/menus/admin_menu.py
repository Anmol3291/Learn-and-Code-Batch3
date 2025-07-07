from menus.base_menu import BaseMenu
from services.admin_service import AdminService
from utils.display import DisplayUtils


class AdminMenu(BaseMenu):
    """Admin menu providing administrative operations and server management."""
    
    def __init__(self, token: str):
        super().__init__()
        self.admin_service = AdminService(token)
        self.display = DisplayUtils()
    
    def display_menu(self) -> None:
        """Display the admin menu options."""
        print("ADMIN MENU")
        print("=" * 10)
        print("1. View external servers status")
        print("2. View external server details")
        print("3. Update/Edit external server API")
        print("4. View Categories")
        print("5. Add new News Category")
        print("6. View Scheduler Status")
        print("7. Logout")
    
    def handle_choice(self, choice: str) -> bool:
        """Process admin menu choices and route to appropriate actions."""
        menu_actions = {
            "1": self.view_servers_status,
            "2": self.view_server_details,
            "3": self.update_server_api,
            "4": self.view_categories,
            "5": self.add_category,
            "6": self.view_scheduler_status,
            "7": self.logout
        }
        
        action = menu_actions.get(choice)
        if action:
            return action()
        else:
            self.display_error_message("Invalid choice. Please try again.")
            return True
    
    def view_servers_status(self) -> bool:
        """Display external servers status information."""
        self.display_header("EXTERNAL SERVERS STATUS")
        
        result = self.admin_service.get_servers_status()
        if "error" in result:
            self.display_error_message(f"Failed to fetch servers: {result['error']}")
            return True
        
        servers = result.get("servers", [])
        if not servers:
            self.display_info_message("No servers found.")
            return True
        
        for server in servers:
            status = "ACTIVE" if server[2] == "Active" else "INACTIVE"
            print(f"{server[0]}. {server[1]} - {status} - Priority: {server[4]} - Last accessed: {server[3]}")
        
        self.display_footer()
        return True
    
    def view_server_details(self) -> bool:
        """Display detailed information about external servers."""
        self.display_header("EXTERNAL SERVER DETAILS")
        
        result = self.admin_service.get_server_details()
        if "error" in result:
            self.display_error_message(f"Failed to fetch server details: {result['error']}")
            return True
        
        details = result.get("details", [])
        if not details:
            self.display_info_message("No server details found.")
            return True
        
        for detail in details:
            masked_key = f"{detail[2][:10]}..." if detail[2] else "Not set"
            print(f"{detail[0]}. {detail[1]} - API Key: {masked_key} - Priority: {detail[3]}")
        
        self.display_footer()
        return True
    
    def update_server_api(self) -> bool:
        """Update API key for a specific server."""
        self.display_header("UPDATE SERVER API")
        
        server_id = input("Enter server ID: ").strip()
        api_key = input("Enter updated API key: ").strip()
        
        if not server_id or not api_key:
            self.display_error_message("Server ID and API key are required.")
            return True
        
        result = self.admin_service.update_server_api(server_id, api_key)
        if "error" in result:
            self.display_error_message(f"Failed to update server: {result['error']}")
        elif result.get("success") is False:
            self.display_error_message("Server ID not found. Please check the server ID and try again.")
        else:
            self.display_success_message("Server updated successfully.")
        
        return True
    
    def view_categories(self) -> bool:
        """Display all available article categories."""
        self.display_header("CATEGORIES")
        
        result = self.admin_service.get_categories()
        if "error" in result:
            self.display_error_message(f"Failed to fetch categories: {result['error']}")
            return True
        
        categories = result.get("categories", [])
        if not categories:
            self.display_info_message("No categories found.")
            return True
        
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        self.display_footer()
        return True
    
    def add_category(self) -> bool:
        """Add a new article category."""
        self.display_header("ADD NEW CATEGORY")
        
        name = input("Enter new category name: ").strip()
        if not name:
            self.display_error_message("Category name cannot be empty.")
            return True
        
        result = self.admin_service.add_category(name)
        if "error" in result:
            self.display_error_message(f"Failed to add category: {result['error']}")
        else:
            self.display_success_message(result.get("message", "Category added successfully."))
        
        return True
    
    def view_scheduler_status(self) -> bool:
        """View current scheduler status."""
        self.display_header("SCHEDULER STATUS")
        
        result = self.admin_service.get_scheduler_status()
        if "error" in result:
            self.display_error_message(f"Failed to get scheduler status: {result['error']}")
            return True
        else:
            print(f"Scheduler Running: {result.get('is_running', 'Unknown')}")
            print(f"Last Fetch Time: {result.get('last_fetch_time', 'Never')}")
            print(f"Last Notification Time: {result.get('last_notification_time', 'Never')}")
            
            jobs = result.get('jobs', [])
            if jobs:
                print("\nScheduled Jobs:")
                for job in jobs:
                    print(f"  - {job.get('name', 'Unknown')}: {job.get('trigger', 'Unknown')}")
                    print(f"    Next Run: {job.get('next_run', 'Unknown')}")
            else:
                print("\nNo scheduled jobs found.")
            
            stats = result.get('processing_stats', {})
            if stats:
                print(f"\nProcessing Stats:")
                print(f"  - Articles Processed: {stats.get('processed', 0)}")
                print(f"  - Articles Skipped: {stats.get('skipped', 0)}")
                print(f"  - Duplicates Found: {stats.get('duplicates', 0)}")
        
        self.display_footer()
        return True
    
    def logout(self) -> bool:
        """Handle admin logout with confirmation."""
        print(f"\nLogging out admin...")
        print("Thank you for using the News Aggregator!")
        return False 