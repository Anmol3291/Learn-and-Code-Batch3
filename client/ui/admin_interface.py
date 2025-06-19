from models.user import User
from services.admin_service import AdminService
from ui.menu_display import MenuDisplay


class AdminInterface:
    """Admin interface controller"""

    def __init__(self, user: User):
        self.user = user
        self.admin_service = AdminService(user)

    def show_admin_menu(self):
        """Display admin menu"""
        while True:
            MenuDisplay.show_admin_menu()
            choice = input("Enter choice: ")

            if choice == "1":
                self.show_servers_status()
            elif choice == "2":
                self.show_server_details()
            elif choice == "3":
                self.handle_update_server()
            elif choice == "4":
                self.handle_add_category()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def show_servers_status(self):
        """Display servers status"""
        result = self.admin_service.get_servers_status()

        if "error" in result:
            print(result["error"])
        else:
            servers = result.get("servers", [])
            for server in servers:
                MenuDisplay.display_server_status(server)

    def show_server_details(self):
        """Display server details"""
        result = self.admin_service.get_server_details()

        if "error" in result:
            print(result["error"])
        else:
            details = result.get("details", [])
            for detail in details:
                MenuDisplay.display_server_details(detail)

    def handle_update_server(self):
        """Handle server update"""
        server_id = input("Enter server ID: ")
        api_key = input("Enter updated API key: ")

        result = self.admin_service.update_server_api(server_id, api_key)
        print(result)

    def handle_add_category(self):
        """Handle adding new category"""
        name = input("Enter new category name: ")

        result = self.admin_service.add_category(name)
        print(result)
