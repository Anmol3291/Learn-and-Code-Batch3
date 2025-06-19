import sys
from models.user import User
from services.auth_service import AuthService
from ui.menu_display import MenuDisplay
from ui.admin_interface import AdminInterface
from utils.input_validator import InputValidator
from utils.data_utils import DateUtils
from services.article_service import ArticleService
from config.settings import Config


class UserInterface:
    """Main user interface controller"""

    def __init__(self):
        self.user = User()
        self.auth_service = AuthService(self.user)
        self.article_service = ArticleService(self.user)
        self.admin_interface = AdminInterface(self.user)
        self.validator = InputValidator()

    def start(self):
        """Start the application"""
        self.show_home()

    def show_home(self):
        """Display home menu"""
        while True:
            MenuDisplay.show_welcome_header()
            MenuDisplay.show_main_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_signup()
            elif choice == "3":
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def handle_login(self):
        """Handle user login"""
        print("\n--- Login ---")
        username = input("Username: ")
        password = input("Password: ")

        success, result = self.auth_service.login(username, password)

        if success:
            print("Login successful")
            if self.user.is_admin():
                self.admin_interface.show_admin_menu()
            else:
                self.show_user_menu()
        else:
            print(result.get("detail", "Login failed"))

    def handle_signup(self):
        """Handle user signup"""
        print("\n--- Sign Up ---")

        while True:
            username = input("Username: ")
            is_valid, error_msg = self.validator.validate_username(username)
            if is_valid:
                break
            print(f"{error_msg}")

        while True:
            email = input("Email: ")
            is_valid, error_msg = self.validator.validate_email(email)
            if is_valid:
                break
            print(f"{error_msg}")

        while True:
            password = input("Password: ")
            is_valid, error_msg = self.validator.validate_password(password)
            if is_valid:
                break
            print(f"{error_msg}")

        result = self.auth_service.signup(username, email, password)
        print(result)

    def show_user_menu(self):
        """Display user menu"""
        while True:
            MenuDisplay.show_welcome_header(self.user.username)
            MenuDisplay.show_user_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.show_headlines_menu()
            elif choice == "2":
                self.show_saved_articles_menu()
            elif choice == "3" or choice == "4":
                print("WILL IMPLEMENT SOON")
            elif choice == "5":
                self.user.clear_session()
                self.show_home()
                break
            else:
                print("Invalid choice. Please try again.")

    def show_headlines_menu(self):
        """Display headlines menu"""
        while True:
            MenuDisplay.show_welcome_header(self.user.username)
            MenuDisplay.show_headlines_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.show_articles("All", "today")
            elif choice == "2":
                self.handle_date_range()
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")

    def handle_date_range(self):
        """Handle date range input"""
        print("\nEnter date range:")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")

        if DateUtils.validate_date_format(
            start_date
        ) and DateUtils.validate_date_format(end_date):
            self.show_category_menu("range", start_date, end_date)
        else:
            print("Invalid date format. Please use YYYY-MM-DD format.")

    def show_category_menu(self, date_type, start_date=None, end_date=None):
        """Display category selection menu"""
        while True:
            MenuDisplay.show_welcome_header(self.user.username)
            MenuDisplay.show_category_menu()
            choice = input("Enter your choice: ")

            if choice in Config.CATEGORIES:
                category = Config.CATEGORIES[choice]
                self.show_articles(category, date_type, start_date, end_date)
            else:
                print("Invalid choice. Please try again.")

    def show_articles(self, category, date_type, start_date=None, end_date=None):
        """Display articles"""
        try:
            if date_type == "today":
                result = self.article_service.get_articles_today(category)
            else:
                result = self.article_service.get_articles_by_date_range(
                    start_date, end_date, category
                )

            if "error" in result:
                print(result["error"])
                return

            articles = result.get("articles", [])

            if not articles:
                print(f"\nNo articles found for {category} category.")
                input("Press Enter to continue...")
                return

            self.display_articles_menu(articles)

        except Exception as e:
            print(f"Error fetching articles: {e}")

    def display_articles_menu(self, articles):
        """Display articles with menu options"""
        while True:
            MenuDisplay.show_welcome_header(self.user.username)
            MenuDisplay.show_articles_menu()

            for article in articles:
                MenuDisplay.display_article(article)

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.show_user_menu()
            elif choice == "2":
                self.show_home()
            elif choice == "3":
                self.handle_save_article()
            else:
                print("Invalid choice. Please try again.")

    def handle_save_article(self):
        """Handle saving an article"""
        article_id = input("Enter article ID to save: ")

        if self.validator.validate_integer(article_id):
            result = self.article_service.save_article(int(article_id))
            print(result.get("message", result.get("error", "Unknown error")))
        else:
            print("Invalid article ID. Please enter a number.")

        input("Press Enter to continue...")

    def show_saved_articles_menu(self):
        """Display saved articles menu"""
        try:
            result = self.article_service.get_saved_articles()

            if "error" in result:
                print(result["error"])
                return

            articles = result.get("articles", [])

            if not articles:
                print("\nNo saved articles found.")
                input("Press Enter to continue...")
                return

            self.display_saved_articles_menu(articles)

        except Exception as e:
            print(f"Error fetching saved articles: {e}")

    def display_saved_articles_menu(self, articles):
        """Display saved articles with menu options"""
        while True:
            MenuDisplay.show_welcome_header(self.user.username)
            MenuDisplay.show_saved_articles_menu()

            for article in articles:
                MenuDisplay.display_article(article)

            choice = input("\nEnter your choice: ")

            if choice == "1":
                return
            elif choice == "2":
                self.show_home()
            elif choice == "3":
                self.handle_delete_article()
                result = self.article_service.get_saved_articles()
                articles = result.get("articles", [])
                if not articles:
                    print("\nNo more saved articles.")
                    input("Press Enter to continue...")
                    return
            else:
                print("Invalid choice. Please try again.")

    def handle_delete_article(self):
        """Handle deleting a saved article"""
        article_id = input("Enter article ID to delete: ")

        if self.validator.validate_integer(article_id):
            result = self.article_service.delete_saved_article(int(article_id))
            print(result.get("message", result.get("error", "Unknown error")))
        else:
            print("Invalid article ID. Please enter a number.")

        input("Press Enter to continue...")
