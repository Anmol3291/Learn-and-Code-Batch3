from handlers.auth_handler import AuthHandler


class NewsAggregatorApp:
    def __init__(self):
        self.auth_handler = AuthHandler()

    def run(self):
        """Main application entry point"""
        try:
            while True:
                self._display_main_menu()
                choice = input("Enter your choice: ")
                self._handle_main_menu_choice(choice)
        except KeyboardInterrupt:
            self._handle_exit()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self._handle_exit()

    def _display_main_menu(self):
        """Display the main application menu"""
        print("\nWelcome to the News Aggregator application")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

    def _handle_main_menu_choice(self, choice: str):
        """Handle user's main menu choice"""
        if choice == "1":
            self.auth_handler.login()
        elif choice == "2":
            self.auth_handler.signup()
        elif choice == "3":
            self._handle_exit()
        else:
            print("Invalid choice. Try again.")

    def _handle_exit(self):
        """Handle application exit"""
        print("Thank you for using our Application, Goodbye!")
        exit(0)


def main():
    app = NewsAggregatorApp()
    app.run()


if __name__ == "__main__":
    main()
