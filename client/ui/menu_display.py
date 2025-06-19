import datetime


class MenuDisplay:
    """Utility class for displaying menus and headers"""

    @staticmethod
    def show_welcome_header(username: str = None):
        """Display welcome header with current date and time"""
        now = datetime.datetime.now()
        if username:
            print(
                f"\nWelcome to the News Application, {username}! Date: {now.strftime('%d-%b-%Y')} Time:{now.strftime('%I:%M%p')}"
            )
        else:
            print("\nWelcome to the News Aggregator application")

    @staticmethod
    def show_main_menu():
        """Display main menu options"""
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

    @staticmethod
    def show_user_menu():
        """Display user menu options"""
        print("Please choose the options below")
        print("1. Headlines")
        print("2. Saved Articles")
        print("3. Search")
        print("4. Notifications")
        print("5. Logout")

    @staticmethod
    def show_admin_menu():
        """Display admin menu options"""
        print("\nAdmin Menu")
        print("1. View external servers status")
        print("2. View external server details")
        print("3. Update/Edit external server API")
        print("4. Add new News Category")
        print("5. Logout")

    @staticmethod
    def show_headlines_menu():
        """Display headlines menu options"""
        print("Please choose the options below")
        print("1. Today")
        print("2. Date range")
        print("3. Logout")

    @staticmethod
    def show_category_menu():
        """Display category menu options"""
        print("Please choose the options below for Headlines")
        print("1. All")
        print("2. Business")
        print("3. Entertainment")
        print("4. Sports")
        print("5. Technology")

    @staticmethod
    def show_articles_menu():
        """Display articles menu options"""
        print("H E A D L I N E S")
        print("1. Back")
        print("2. Logout")
        print("3. Save Article")

    @staticmethod
    def show_saved_articles_menu():
        """Display saved articles menu options"""
        print("S A V E D")
        print("1. Back")
        print("2. Logout")
        print("3. Delete Article")

    @staticmethod
    def display_article(article):
        """Display a single article with consistent formatting"""
        print(f"\nArticle Id: {article[0]}")
        print(f"{article[1]}")
        print(f"{article[2][:150]}...")
        print(f"source: {article[3]}")
        print(f"URL: {article[4]}")
        print(f"Category: {article[5]}")
        if len(article) > 7:
            print(f"Likes: {article[7]}, Dislikes: {article[8]}")

    @staticmethod
    def display_server_status(server):
        """Display server status information"""
        print(f"{server[0]}. {server[1]} - {server[2]} - last accessed: {server[3]}")

    @staticmethod
    def display_server_details(server):
        """Display server details"""
        print(f"{server[0]}. {server[1]} - {server[2]}")
